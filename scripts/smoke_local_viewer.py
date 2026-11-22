"""Exercise only a newly generated synthetic CT; never enumerate patient studies."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import struct
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import uuid

BASE = 'http://127.0.0.1:8042'
PATIENT_ID = 'SYNTHETIC_LOCAL_SMOKE'


def element(group, tag, vr, value):
    if isinstance(value, str):
        value = value.encode('ascii')
    if len(value) % 2:
        value += b'\0' if vr in ('UI', 'OB', 'OW') else b' '
    prefix = struct.pack('<HH', group, tag) + vr.encode()
    if vr in ('OB', 'OW', 'SQ', 'UN', 'UT'):
        return prefix + b'\0\0' + struct.pack('<I', len(value)) + value
    return prefix + struct.pack('<H', len(value)) + value


def dicom(study_uid, series_uid, frame_uid, index):
    uid = '2.25.' + str(uuid.uuid4().int)
    sop = '1.2.840.10008.5.1.4.1.1.2'
    meta = b''.join([
        element(2, 1, 'OB', b'\0\1'), element(2, 2, 'UI', sop),
        element(2, 3, 'UI', uid), element(2, 0x10, 'UI', '1.2.840.10008.1.2.1'),
        element(2, 0x12, 'UI', '2.25.135791357913579'),
    ])
    entries = [
        (8, 8, 'CS', 'ORIGINAL\\PRIMARY\\AXIAL'), (8, 0x16, 'UI', sop),
        (8, 0x18, 'UI', uid), (8, 0x20, 'DA', '20261122'), (8, 0x30, 'TM', '120000'),
        (8, 0x50, 'SH', 'SYNTHETIC'), (8, 0x60, 'CS', 'CT'),
        (8, 0x1030, 'LO', 'SYNTHETIC TEST - NOT A PATIENT'),
        (8, 0x103E, 'LO', 'Synthetic geometric phantom'),
        (0x10, 0x10, 'PN', 'SYNTHETIC^VIEWER TEST'), (0x10, 0x20, 'LO', PATIENT_ID),
        (0x18, 0x50, 'DS', '2'), (0x20, 0xD, 'UI', study_uid),
        (0x20, 0xE, 'UI', series_uid), (0x20, 0x10, 'SH', 'SYNTHETIC'),
        (0x20, 0x11, 'IS', '1'), (0x20, 0x13, 'IS', str(index + 1)),
        (0x20, 0x32, 'DS', f'0\\0\\{index * 2}'),
        (0x20, 0x37, 'DS', '1\\0\\0\\0\\1\\0'), (0x20, 0x52, 'UI', frame_uid),
        (0x28, 2, 'US', struct.pack('<H', 1)), (0x28, 4, 'CS', 'MONOCHROME2'),
        (0x28, 0x10, 'US', struct.pack('<H', 64)), (0x28, 0x11, 'US', struct.pack('<H', 64)),
        (0x28, 0x30, 'DS', '1\\1'), (0x28, 0x100, 'US', struct.pack('<H', 16)),
        (0x28, 0x101, 'US', struct.pack('<H', 16)), (0x28, 0x102, 'US', struct.pack('<H', 15)),
        (0x28, 0x103, 'US', struct.pack('<H', 0)),
        (0x28, 0x1050, 'DS', '0'), (0x28, 0x1051, 'DS', '1500'),
        (0x28, 0x1052, 'DS', '-1024'), (0x28, 0x1053, 'DS', '1'),
    ]
    pixels = b''.join(struct.pack('<H', 1024 + index * 30 if (x-32)**2 + (y-32)**2 < 400 else 0)
                      for y in range(64) for x in range(64))
    body = b''.join(element(*entry) for entry in entries) + element(0x7FE0, 0x10, 'OW', pixels)
    return b'\0' * 128 + b'DICM' + element(2, 0, 'UL', struct.pack('<I', len(meta))) + meta + body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--action', choices=['create', 'verify', 'cleanup'], default='create')
    args = parser.parse_args()
    users = json.loads((args.data_root / 'secrets/orthanc-users.json').read_text())['RegisteredUsers']
    token = base64.b64encode(f"local:{users['local']}".encode()).decode()

    def request(path, data=None, method=None, authorization=token):
        headers = {'Content-Type': 'application/dicom'}
        if authorization is not None:
            headers['Authorization'] = 'Basic ' + authorization
        with urlopen(Request(BASE + path, data=data, headers=headers, method=method), timeout=20) as response:
            return response.read()

    state_file = args.data_root / 'synthetic-test/state.json'
    if args.action == 'create':
        if state_file.exists():
            raise RuntimeError('Existing synthetic test: verify/cleanup it first; refusing overwrite.')
        for auth in (None, base64.b64encode(b'orthanc:orthanc').decode()):
            try:
                request('/system', authorization=auth)
            except HTTPError as error:
                assert error.code == 401
            else:
                raise AssertionError('Unauthenticated or default-account request was accepted')
        state_file.parent.mkdir(parents=True, exist_ok=True)
        study_uid, series_uid, frame_uid = ['2.25.' + str(uuid.uuid4().int) for _ in range(3)]
        state = {'study_uid': study_uid, 'instances': []}
        for index in range(3):
            payload = dicom(study_uid, series_uid, frame_uid, index)
            (state_file.parent / f'synthetic-{index}.dcm').write_bytes(payload)
            result = json.loads(request('/instances', payload, 'POST'))
            assert result['Status'] == 'Success'
            state['study_id'] = result['ParentStudy']
            saved = request('/instances/' + result['ID'] + '/file')
            state['instances'].append({'id': result['ID'], 'sha256': hashlib.sha256(saved).hexdigest()})
            state_file.write_text(json.dumps(state, indent=2))
        print('PASS: unauthorized/default login rejected; 3 synthetic instances imported.')
    state = json.loads(state_file.read_text())
    study = json.loads(request('/studies/' + state['study_id']))
    if study['PatientMainDicomTags']['PatientID'] != PATIENT_ID or study['MainDicomTags']['StudyInstanceUID'] != state['study_uid']:
        raise RuntimeError('Ownership mismatch: refusing to touch this study.')
    if args.action == 'cleanup':
        for item in state['instances']:
            saved = request('/instances/' + item['id'] + '/file')
            if hashlib.sha256(saved).hexdigest() != item['sha256']:
                raise RuntimeError('Synthetic contents changed: refusing cleanup.')
        for item in state['instances']:
            request('/instances/' + item['id'], method='DELETE')
        state_file.unlink()
        print('PASS: removed only the owned synthetic instances; local fixtures preserved.')
        return
    for item in state['instances']:
        saved = request('/instances/' + item['id'] + '/file')
        assert hashlib.sha256(saved).hexdigest() == item['sha256']
    assert request('/instances/' + state['instances'][0]['id'] + '/preview').startswith(b'\x89PNG')
    results = json.loads(request('/dicom-web/studies?StudyInstanceUID=' + state['study_uid']))
    assert len(results) == 1
    assert request('/ohif/').lstrip().lower().startswith(b'<!doctype html')
    print('PASS: exact stored bytes, preview PNG, DICOMweb study query and OHIF HTML.')


if __name__ == '__main__':
    main()
