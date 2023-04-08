import requests
import dotenv
import os

dotenv.load_dotenv()
ROOT = os.getenv('API_ROOT')


def get_user(tg_id):
    return requests.get(ROOT + f'/tg/{tg_id}').json()


def get_notes(user_id):
    return requests.get(ROOT + f'/notes/{user_id}').json()


def set_tg_id(tg_id, user_id):
    return requests.post(ROOT + f'/tg/{tg_id}', json={
        'user_id': user_id
    }).json()


def register(username, password):
    return requests.post(ROOT + '/auth/register', json={
        'password': password,
        'username': username
    }).json()


def login(username, password):
    return requests.post(ROOT + '/auth/login', json={
        'password': password,
        'username': username
    }).json()


def create(title, body, user_id):
    return requests.post(ROOT + '/notes/create', json={
        'title': title,
        'body': body,
        'user_id': user_id
    }).json()

