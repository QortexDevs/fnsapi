import configparser
import pytz
import subprocess

from datetime import datetime
from os import path, environ


class Storage:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = None
        self.storage_file_path = environ.get(
            'FNS_API_TOKEN_STORAGE_FILE_PATH') if not None else path.abspath(__file__)
        if not path.isfile(self.storage_file_path):
            open(self.storage_file_path, 'w').close()
        self.config.read(self.storage_file_path)
        if not self.config.has_section('FNSAPISessionToken'):
            self.config.add_section('FNSAPISessionToken')

    def get_section_option(self, section_name, option_name):
        if self.config.has_option(section_name, option_name):
            return self.config.get(section_name, option_name)
        return None

    def get_fns_api_session_token_expire_time(self):
        fns_api_session_token_expire_time= self.get_section_option('FNSAPISessionToken', 'ExpireTime')
        if fns_api_session_token_expire_time is not None:
            return datetime.strptime(fns_api_session_token_expire_time, '%Y-%m-%dT%H:%M:%S %z')
        return None

    def get_fns_api_session_token(self):
        return self.get_section_option('FNSAPISessionToken', 'Token')

    def set_section_option(self, option_name, value):
        self.config.set('FNSAPISessionToken', option_name, value)
        self.config_file=open(self.storage_file_path, 'w')
        self.config.write(self.config_file)
        self.config_file.close()

    def set_fns_api_session_token_expire_time(self, expire_time):
        self.set_section_option('ExpireTime', expire_time)

    def set_fns_api_session_token(self, token):
        self.set_section_option('Token', token)

    def delete_section_option(self, section_name, option_name):
        self.config.remove_option(section_name, option_name)
        self.config_file=open(self.storage_file_path, 'w')
        self.config.write(self.config_file)
        self.config_file.close()

    def delete_fns_api_session_token_expire_time(self):
        self.delete_section_option('FNSAPISessionToken', 'ExpireTime')

    def delete_fns_api_session_token(self):
        self.delete_section_option('FNSAPISessionToken', 'Token')

    def delete_outdated_token(self):
        fns_api_session_token_expire_time=self.get_fns_api_session_token_expire_time()
        fns_api_session_token=self.get_fns_api_session_token()
        can_delete=False
        if fns_api_session_token_expire_time is not None and fns_api_session_token_expire_time < datetime.now(tz=fns_api_session_token_expire_time.tzinfo):
            self.delete_fns_api_session_token_expire_time()
            can_delete=True
        if can_delete and fns_api_session_token is not None:
            self.delete_fns_api_session_token()

    def get_stored_token(self):
        self.delete_outdated_token()
        return self.get_fns_api_session_token()

    def store_token(self, token, expire_time):
        self.set_fns_api_session_token(token)
        self.set_fns_api_session_token_expire_time(expire_time)
