from fnsapi.api import FNSApi
from fnsapi.storage.ini import Storage


class FNSQueryRunner:

    def __init__(self):
        self.fns_api = FNSApi()
        self.storage = Storage()

    def get_session_token_from_storage(self):
        return self.storage.get_stored_token()

    def persist_session_token(self, token, expire_time):
        self.storage.store_token(token, expire_time)

    def get_session_token(self):
        token = self.get_session_token_from_storage()
        if token is not None:
            return token
        token_info = self.fns_api.get_session_token()
        if token_info['status'] == 'success':
            token = token_info['token']
            expire_time = token_info['expire_time']
            self.persist_session_token(token, expire_time)
            return token

    def check_ticket(self, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign):
        session_token = self.get_session_token()
        return self.fns_api.check_ticket(session_token, 'ofd_user', sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign)

    def get_ticket(self, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign):
        session_token = self.get_session_token()
        return self.fns_api.get_ticket(session_token, 'ofd_user', sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign)
