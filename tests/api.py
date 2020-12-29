from fnsapi.api import FNSApi

fns_api = FNSApi()
result = fns_api.get_session_token()
print(result)



def test_get_token(self):
    fns_api = FNSApi()
    result = fns_api.get_session_token()