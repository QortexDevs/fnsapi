import os
import zeep
import base64
import time
from lxml import etree
from fnsapi.storage.env import Storage


class FNSApi:

    def get_master_token(self):
        return os.environ.get('FNS_API_MASTER_TOKEN')

    def get_base_url(self):
        return os.environ.get('FNS_API_BASE_URL', default='https://openapi.nalog.ru:8090/')

    def get_session_token(self):
        master_token = self.get_master_token()
        base_url = self.get_base_url()
        wsdl = base_url + 'open-api/AuthService/0.1?wsdl'
        xml = '<tns:AuthRequest xmlns:tns="urn://x-artefacts-gnivc-ru/ais3/kkt/AuthService/types/1.0"><tns:AuthAppInfo><tns:MasterToken>' + \
            master_token + '</tns:MasterToken></tns:AuthAppInfo></tns:AuthRequest>'
        root = etree.fromstring(xml)
        client = zeep.Client(wsdl=wsdl)
        response = client.service.GetMessage(Message={'_value_1': root})
        tag = response[0].tag
        token = None
        expire_time = None
        result = {
            'status': 'error',
            'message': '',
            'token': None,
            'expire_time': None
        }
        if tag == '{urn://x-artefacts-gnivc-ru/ais3/kkt/AuthService/types/1.0}Fault':
            result['message'] = response[0][0].text
        elif tag == '{urn://x-artefacts-gnivc-ru/ais3/kkt/AuthService/types/1.0}Result':
            result['status'] = 'success'
            result['message'] = 'Токен выдан'
            result['token'] = response[0][0].text
            result['expire_time'] = response[0][1].text
        return result

    def process_ticket(self, request_type, session_token, user_id, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign):
        base_url = self.get_base_url()
        wsdl = base_url + 'open-api/ais3/KktService/0.1?wsdl'
        xml = """
        <tns:{request_type}TicketRequest xmlns:tns="urn://x-artefacts-gnivc-ru/ais3/kkt/KktTicketService/types/1.0">
            <tns:{request_type}TicketInfo>
                <tns:Sum>{sum}</tns:Sum>
                <tns:Date>{timestamp}</tns:Date>
                <tns:Fn>{fiscal_number}</tns:Fn>
                <tns:TypeOperation>{operation_type}</tns:TypeOperation>
                <tns:FiscalDocumentId>{fiscal_document_id}</tns:FiscalDocumentId>
                <tns:FiscalSign>{fiscal_sign}</tns:FiscalSign>
            </tns:{request_type}TicketInfo>
        </tns:{request_type}TicketRequest>
        """.format(
            request_type=request_type,
            sum=sum,
            timestamp=timestamp,
            fiscal_number=fiscal_number,
            operation_type=operation_type,
            fiscal_document_id=fiscal_document_id,
            fiscal_sign=fiscal_sign
        )
        root = etree.fromstring(xml)

        client = zeep.Client(wsdl=wsdl)

        client.transport.session.headers.update({
            'FNS-OpenApi-Token': session_token,
            'FNS-OpenApi-UserToken': base64.b64encode(user_id.encode('ascii'))
        })
        messageId = client.service.SendMessage(Message={'_value_1': root})
        wait_count = 0
        while True:
            time.sleep(2)
            wait_count += 2
            response = client.service.GetMessage(MessageId=messageId)
            if (response['ProcessingStatus'] == 'COMPLETED'):
                break
        response = response['Message']['_value_1']
        result = {
            'status': 'error',
            'message': '',
            'code': None,
        }
        tag = response[0].tag
        if tag == '{urn://x-artefacts-gnivc-ru/ais3/kkt/KktTicketService/types/1.0}Fault':
            result['message'] = response[0][0].text
        elif tag == '{urn://x-artefacts-gnivc-ru/ais3/kkt/KktTicketService/types/1.0}Result':
            result['status'] = 'success'
            result['code'] = response[0][0].text
            result['message'] = response[0][1].text
        return result

    def check_ticket(self, session_token, user_id, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign):
        return self.process_ticket('Check', session_token, user_id, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign)

    def get_ticket(self, session_token, user_id, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign):
        return self.process_ticket('Get', session_token, user_id, sum, timestamp, fiscal_number, operation_type, fiscal_document_id, fiscal_sign)
