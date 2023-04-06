from time import sleep

import requests


def register():
    data = requests.post('http://127.0.0.1:5000/auth/register', json={
        'username': 'ADMIN',
        'password': 'ADMIN'
    }).json()
    return data


def login():
    data = requests.post('http://127.0.0.1:5000/auth/login', json={
        'username': 'ADMIN',
        'password': 'ADMIN'
    }).json()
    return data


def create_note(id_, title, body):
    data = requests.post('http://127.0.0.1:5000/notes/create', json={
        'user_id': id_,
        'body': body,
        'title': title
    }).json()
    return data


def read_notes(id_):
    data = requests.get(f'http://127.0.0.1:5000/notes/{id_}').json()
    return data


def update_note(id_, title, body):
    data = requests.post(f'http://127.0.0.1:5000/notes/note/{id_}', json={
        'author_id': id_,
        'body': body,
        'title': title
    }).json()
    return data


def del_user(id_):
    user_del_data = requests.post(f'http://127.0.0.1:5000/user/{id_}', json={
        'password': 'ADMIN'
    }).json()
    return user_del_data


def test_whole():
    dreg = register()
    print(dreg)
    assert dreg['status'] == 'successful'
    sleep(0.1)

    dlog = login()
    print(dlog)
    id_ = dreg['id']
    sleep(0.1)

    dcreate = create_note(id_, 'TEST_TITLE', 'TEST_BODY')
    print(dcreate)
    sleep(0.1)

    dupdate = update_note(id_, 'TEST_TITLE_2', 'TEST_BODY')
    print(dupdate)
    assert dupdate['status'] == 'successful'
    sleep(0.1)

    dread = read_notes(id_)
    assert len(dread) == 1 and dread[0]['title'] == 'TEST_TITLE_2'
    sleep(0.1)

    update_note(id_, 'TEST_TITLE', 'TEST_BODY')
    dread = read_notes(id_)
    print(dread)
    sleep(0.1)

    ddel = del_user(id_)
    print(dcreate)
    sleep(0.1)

    assert dreg['id'] == dlog['id']
    assert dcreate['status'] == 'successful'
    assert len(dread) == 1 and dread[0]['title'] == 'TEST_TITLE'\
           and dread[0]['body'] == 'TEST_BODY'
    assert ddel['status'] == 'successful'
