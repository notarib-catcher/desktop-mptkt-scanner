from typing import Optional

import keyring
import requests


class ServerBridge:
    """
    Pull local data from system secure storage (if present). If `need_init` is True after this, then enrollment is
    needed before passes can be scanned. Otherwise, check if `self.assignment` is not None. If assignment exists,
    everything is good. If assignment doesn't exist, call `get_assignment()` every few seconds until either the
    assignment is received. Or a conflict forces the client to reset.
    """

    def __init__(self):
        self.need_init = True

        self.assignment = None

        kiosk_token: Optional[str] = None
        kiosk_name: Optional[str] = None

        server_ip = keyring.get_password('mp.ticketing.service', 'mp.server')
        if server_ip is not None:
            kiosk_token = keyring.get_password('mp.ticketing.service', server_ip)
            kiosk_name = keyring.get_password('mp.ticketing.service', 'mp.kiosk.name')

        if kiosk_token is None:
            try:
                keyring.delete_password('mp.ticketing.service', 'mp.server')
                keyring.delete_password('mp.ticketing.service', 'mp.kiosk.name')
            except:
                print("Exception while deleting, continuing")

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
        """Utility function used to clear all stored credentials."""

        if not self.need_init:
            keyring.delete_password('mp.ticketing.service', self.server_ip)
            keyring.delete_password('mp.ticketing.service', 'mp.server')
            keyring.delete_password('mp.ticketing.service', 'mp.kiosk.name')

            self.server_ip = None
            self.kiosk_token = None
            self.kiosk_name = None
            self.assignment = None
            self.need_init = True

    def enroll(self, address: str, code: str, name: str):
        """
        Register with the server and store credentials for future use. Credentials received are stored into system
        keystore and are persisted across restarts.
        """
        if not self.need_init:
            return

        payload: dict = {
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

    def get_assignment(self):
        """
        Updates assignment, Might cause the entire cache and all stored credentials for this app to be reset. If the
        server sends a 409 (CONFLICT), 401 (INVALID TOKEN) or 404 (NO ENTRY FOUND).

        Note:
        If the assignment ID is "!ALL!" then DO NOT ENABLE THE MARK ATTENDANCE BUTTON EVEN IF THE PASS IS VALID.
        Assignments with an ID "!ALL!" allow the kiosk to verify passes passively but not to mark attendance on them.
        Attempting to mark attendance when your own assignment is "!ALL!" will result in a fail (409 conflict).
        """

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
        """
        Verifies a pass. Returns an object, which contains status, text (to be displayed front and center) and subtext.
        Subtext is only populated if a "Reason" attribute is present in the response. If the status is 200, then the
        pass is either a valid pass, or a staff pass. If the pass is valid, then enable the "mark attendance" button.
        If the pass is staff, don't enable the button, instead show a popup saying "verified staff – allow to proceed".
        For all other status codes, disable the mark attendance button.
        """

        default_res = {
            'status': 200,
            'text': 'valid',
            'subtext': ''
        }

        if self.assignment is None:
            return None

        response = requests.get(self.server_ip + '/verify?token=' + token_string + '&event=' + self.assignment['a_id'])

        if response.status_code == 200:
            if 'staff' in response.text:
                default_res['subtext'] = 'STAFF'

            return default_res

        else:
            default_res['status'] = response.status_code

            rsplit = response.text.upper().split('REASON:', 1)
            default_res['text'] = rsplit[0]

            if len(rsplit) > 1:
                default_res['subtext'] = rsplit[1]

            return default_res

    def mark_attendance(self, token) -> bool:
        """
        Marks attendance. If a conflict status is received, it may call get_assignment(). Returns True if attendance
        was marked, False otherwise.
        """

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
