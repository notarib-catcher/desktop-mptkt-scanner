from typing import Optional

import keyring
import requests


class ServerBridge:
    def __init__(self):
        self.need_init = True
        self.assignment: Optional[dict[str, str]] = None

        server_ip = keyring.get_password('mp.ticketing.service', 'mp.server')
        kiosk_token: Optional[str] = None
        kiosk_name: Optional[str] = None

        if server_ip is not None:
            kiosk_token = keyring.get_password('mp.ticketing.service', server_ip)
            kiosk_name = keyring.get_password('mp.ticketing.service', 'mp.kiosk.name')

        if kiosk_token is None:
            keyring.delete_password('mp.ticketing.service', 'mp.server')
            keyring.delete_password('mp.ticketing.service', 'mp.kiosk.name')

        else:
            self.need_init = False
            self.server_ip = server_ip
            self.kiosk_token = kiosk_token

            if kiosk_name is None:
                self.kiosk_name = 'Unnamed'
            else:
                self.kiosk_name = kiosk_name

            self.get_assignment()

    def clear_creds(self):
        if not self.need_init:
            keyring.delete_password('mp.ticketing.service', self.server_ip)
            keyring.delete_password('mp.ticketing.service', 'mp.server')
            keyring.delete_password('mp.ticketing.service', 'mp.kiosk.name')

            self.assignment = None
            self.need_init = True

    def enroll(self, address: str, code: int, name: str):
        if not self.need_init:
            self.clear_creds()

        payload = {
            'code': code,
            'name': name
        }

        enroll_response = requests.post(address + '/enroll', json=payload)

        if enroll_response.status_code == 200:
            self.server_ip = address
            self.kiosk_name = name
            self.kiosk_token = enroll_response.text
            self.need_init = False

            keyring.set_password('mp.ticketing.service', 'mp.server', self.server_ip)
            keyring.set_password('mp.ticketing.service', self.server_ip, enroll_response.text)
            keyring.set_password('mp.ticketing.service', 'mp.kiosk.name', name)

    def get_assignment(self) -> bool:
        if self.need_init:
            return False

        assignment_response = requests.get(self.server_ip + '/assignment?kioskToken=' + self.kiosk_token)

        match assignment_response.status_code:
            case 200:
                assignment_string = assignment_response.text
                assignment_split_sting = assignment_string.split('+', 1)

                self.assignment = {
                    'a_name': assignment_split_sting[0],
                    'a_id': assignment_split_sting[1]
                }

                return True

            case 204:
                self.assignment = None
                return False

            case 401 | 404 | 409:
                self.assignment = None
                self.clear_creds()
                return False

    def verify(self, token_string) -> Optional[dict[str, str | int]]:
        default_res = {
            'status': 200,
            'text': 'valid',
            'subtext': ''
        }

        if self.assignment is None:
            return None

        response = requests.get(self.server_ip + '/verify?token=' + token_string + '&event=' + self.assignment['a_id'])

        if response.status_code is 200:
            if 'staff' in response.text:
                default_res['subtext'] = 'STAFF'

            return default_res

        else:
            default_res['status'] = response.status_code

            response_split = response.text.upper().split('REASON:', 1)
            default_res['text'] = response_split[0]

            if response_split[1] != '':
                default_res['subtext'] = response_split[1]

            return default_res

    def mark_attendance(self, token) -> bool:
        if self.assignment is None:
            return False

        payload = {
            'kioskToken': self.kiosk_token,
            'event': self.assignment['a_id'],
            'token': token
        }

        attn_response = requests.put(self.server_ip + '/mark', json=payload)

        match attn_response.status_code:
            case 200:
                return True

            case 409:
                self.get_assignment()
                return False

            case _:
                return False
