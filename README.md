# Коннектор к апи ФНС для проверки чеков от ОФД в ФНС

Проверяет данные чеков, полученных от оператора фискальных данных в Федерельной налоговой службе.

## Установка и настройка

[Получите](https://www.nalog.ru/files/kkt/pdf/%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.pdf) `master token` в Федеральной налоговой службе.
<br>
<br>
Установите пакет
```sh
pip install fnsapi
```

<br>

Добавьте переменную окружения в своё виртуально окружение
```sh
FNS_API_MASTER_TOKEN=master_token_from_fns
```

<br>

Если базовый адрес апи ФНС отличается от `https://openapi.nalog.ru:8090/`, то укажите его через перменную окружения
```sh
FNS_API_BASE_URL=https://openapi.nalog.ru:8090/
```

## Принцип работы

Чтобы запросить информацию о чеке в ФНС, нужно
1. Получить токен сессии
2. Сгенерерировать имя пользователя в вашей системе, от имени которого осуществляется запрос
3. Вызвать функцию проверки чека или получения информации о чеке

## Пример использования

<br>

Например, данные получены из qr-кода: 
```
t=20201225T1016&s=1113.99&fn=9282440300829880&i=10556&fp=189504453&n=1
```

<br>

```
t — timestamp, нужно переформатировать в %Y-%m-%dT%H:%M:%S — 2020-12-25T10:16:00
s — sum, нужно умножить на 100 — 1111399
fn - fiscal_number — 9282440300829880
i - fiscal_document_id — 10556
fp - fiscal_sign — 189504453
n - operation_type — 1
```

<br>

```python
from fnsapi.api import FNSApi

fns_api = FNSApi()

# получение сессионного токена
session_token = fns_api.get_session_token()
user_id = 'ofd_user' # любое текстовое значение на ваш вкус

# проверка существования чека
result = fns_api.check_ticket(
    session_token, 
    user_id, 
    sum, # сумма чека в формате РРРКК, 12 рублей 23 копейки передавайте как 1223
    timestamp, # дата и время в формате %Y-%m-%dT%H:%M:%S
    fiscal_number, # код ККТ
    operation_type, # тип операции
    fiscal_document_id, # номер фискального документа
    fiscal_sign # фискальный признак
)

# в результате придёт структура
status = result['status'] # success, если апи фНС отработало запрос, еrror, если нет.
code = result['code'] # код ошибки от апи ФНС.
message= result['message'] # сообщение от ФНС.


# получение информации о чеке
result = fns_api.get_ticket(
    session_token, 
    user_id, 
    sum, # сумма чека в формате РРРКК, 12 рублей 23 копейки передавайте как 1223
    timestamp, # дата и время в формате %Y-%m-%dT%H:%M:%S
    fiscal_number, # код ККТ
    operation_type, # тип операции
    fiscal_document_id, # номер фискального документа
    fiscal_sign # фискальный признак
)

# в результате придёт структура
status = result['status'] # success, если апи фНС отработало запрос, еrror, если нет.
code = result['code'] # код ошибки от апи ФНС.
message= result['message'] # сообщение от ФНС в случае ошибки или JSON-строка с информацией о чеке.
```