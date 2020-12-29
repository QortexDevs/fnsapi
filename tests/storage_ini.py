import os
import pytz

from datetime import datetime, timedelta
from fnsapi.storage.ini import Storage

def test_no_token():
    os.environ['FNS_API_TOKEN_STORAGE_FILE_PATH'] = '/tmp/storage.ini'
    storage = Storage()
    fns_api_session_token_expire_time = storage.get_fns_api_session_token_expire_time()
    fns_api_session_token = storage.get_fns_api_session_token()
    assert fns_api_session_token_expire_time is None
    assert fns_api_session_token is None

def test_set_outdated_token():
    storage = Storage()
    storage.store_token('2b3d3ec0104d4e3597ab8e7fcdee70c9',  '2020-11-27T19:16:05 +03:00')
    assert storage.get_fns_api_session_token() == '2b3d3ec0104d4e3597ab8e7fcdee70c9'
    assert storage.get_fns_api_session_token_expire_time() == datetime.strptime('2020-11-27T19:16:05 +03:00', '%Y-%m-%dT%H:%M:%S %z')
    assert storage.get_stored_token() is None
    assert 'FNS_API_SESSION_TOKEN' not in os.environ
    assert 'FNS_API_SESSION_TOKEN_EXPIRE_TIME' not in os.environ

def test_set_token_string_timestamp():
    storage = Storage()
    expire_time = datetime.now(tz=pytz.utc) + timedelta(hours=1)
    expire_time = expire_time.strftime('%Y-%m-%dT%H:%M:%S %z')
    storage.store_token('2b3d3ec0104d4e3597ab8e7fcdee70c9',  expire_time)
    assert storage.get_fns_api_session_token() == '2b3d3ec0104d4e3597ab8e7fcdee70c9'
    assert storage.get_fns_api_session_token_expire_time() == datetime.strptime(expire_time, '%Y-%m-%dT%H:%M:%S %z')
    assert storage.get_stored_token() == '2b3d3ec0104d4e3597ab8e7fcdee70c9'
    
