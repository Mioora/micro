import requests

from app.settings import settings


def get_address(order_id: str):
    if settings.for_test is None:
        return 'address'
    try:
        data = requests.get(settings.order_service_url + str(order_id), headers=get_delivery_token())
        return data.json()['address']
    except requests.ConnectionError:
        return None
    
def get_delivery_token():
    username = settings.delivery_login
    password = settings.delivery_password
    token = get_token(username=username, password=password).json()['access_token']
    return {'token': token}


def get_token(username: str, password: str):
    url = f'{settings.keycloak_url}/{settings.keycloak_realm}/protocol/openid-connect/token'
    data = {
    'username': username,
    'password': password,
    'client_id': settings.keycloak_id,
    'client_secret': settings.keycloak_secret,
    'grant_type': 'password',
    'scope': 'openid'
    }
    response = requests.post(url, data=data)

    return response
    

def get_userinfo(token: str):
    header = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{settings.keycloak_url}/{settings.keycloak_realm}/protocol/openid-connect/userinfo', headers=header)
    if response.status_code == 200:
        return response
    else:
        return None