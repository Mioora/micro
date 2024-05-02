import requests
from app.settings import settings

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
    return response