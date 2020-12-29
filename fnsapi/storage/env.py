import os
import pytz
import subprocess

from datetime import datetime


class Storage:

    def get_fns_api_session_token_expire_time(self):
        fns_api_session_token_expire_time = os.environ.get(
            'FNS_API_SESSION_TOKEN_EXPIRE_TIME')
        if fns_api_session_token_expire_time is not None:
            return datetime.strptime(fns_api_session_token_expire_time, '%Y-%m-%dT%H:%M:%S %z')
        return None

    def get_fns_api_session_token(self):
        return os.environ.get('FNS_API_SESSION_TOKEN')

    def set_and_export_environment_variable(self, name, value):
        os.environ[name] = value
        print('export ' + name + '="' + value + '"')
        subprocess.call('export ' + name + '="' + value + '"', shell=True)

    def set_fns_api_session_token_expire_time(self, expire_time):
        self.set_and_export_environment_variable(
            'FNS_API_SESSION_TOKEN_EXPIRE_TIME', expire_time)

    def set_fns_api_session_token(self, token):
        self.set_and_export_environment_variable(
            'FNS_API_SESSION_TOKEN', token)

    def delete_fns_api_session_token_expire_time(self):
        del os.environ['FNS_API_SESSION_TOKEN_EXPIRE_TIME']

    def delete_fns_api_session_token(self):
        del os.environ['FNS_API_SESSION_TOKEN']

    def delete_outdated_token(self):
        fns_api_session_token_expire_time = self.get_fns_api_session_token_expire_time()
        fns_api_session_token = self.get_fns_api_session_token()
        can_delete = False
        if fns_api_session_token_expire_time is not None and fns_api_session_token_expire_time < datetime.now(tz=fns_api_session_token_expire_time.tzinfo):
            self.delete_fns_api_session_token_expire_time()
            can_delete = True
        if can_delete and fns_api_session_token is not None:
            self.delete_fns_api_session_token()

    def get_stored_token(self):
        self.delete_outdated_token()
        return self.get_fns_api_session_token()

    def store_token(self, token, expire_time):
        self.set_fns_api_session_token(token)
        self.set_fns_api_session_token_expire_time(expire_time)
