from time import sleep
import requests

root = 'http://127.0.0.1:5000'


def register(username, password):
    data = requests.post(root + '/auth/register', json={
        'username': username,
        'password': password
    }).json()
    return data


def login(username, password):
    data = requests.post(root + '/auth/login', json={
        'username': username,
        'password': password
    }).json()
    return data


def reset_password(id_, old, new):
    data = requests.post(root + '/auth/password', json={
        'user_id': id_,
        'old_password': old,
        'new_password': new
    }).json()
    return data


def create_note(id_, title, body):
    data = requests.post(root + '/notes/create', json={
        'user_id': id_,
        'body': body,
        'title': title
    }).json()
    return data


def read_notes(id_):
    data = requests.get(root + f'/notes/{id_}').json()
    return data


def update_note(id_, title, body):
    data = requests.post(root + f'/notes/note/{id_}', json={
        'author_id': id_,
        'body': body,
        'title': title
    }).json()
    return data


def link_tg(user_id, tg_id):
    data = requests.post(root + f'/tg/{tg_id}', json={
        'user_id': user_id
    }).json()
    return data


def get_tg_id(tg_id):
    data = requests.get(root + f'/tg/{tg_id}').json()
    return data


def del_user(id_, password):
    user_del_data = requests.post(root + f'/auth/{id_}', json={
        'password': password
    }).json()
    return user_del_data


def test_whole():
    username = 'ADMIN'
    old = 'ADMIN'
    new = 'ADMIN_NEW'

    dreg = register(username, old)
    print(dreg)
    assert dreg['status'] == 'successful'
    sleep(0.1)

    dlog = login(username, old)
    print(dlog)
    assert dreg['id'] == dlog['id']
    id_ = dreg['id']
    sleep(0.1)

    dchange = reset_password(id_, old, new)
    print(dchange)
    assert dchange['status'] == 'successful'
    sleep(0.1)

    dlog = login(username, new)
    print(dlog)
    assert dlog['status'] == 'successful' and dlog['id'] == id_
    sleep(0.1)

    dcreate = create_note(id_, 'TEST_TITLE', 'TEST_BODY')
    print(dcreate)
    assert dcreate['status'] == 'successful'
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
    assert len(dread) == 1 and dread[0]['title'] == 'TEST_TITLE'\
           and dread[0]['body'] == 'TEST_BODY'
    sleep(0.1)

    dlink = link_tg(id_, 1)
    print(dlink)
    assert dlink['status'] == 'successful'
    sleep(0.1)

    dtg = get_tg_id(1)
    print(dtg)
    assert dtg['id'] == id_
    sleep(0.1)

    delink = link_tg(None, 1)
    print(delink)
    assert dlink['status'] == 'successful'
    sleep(0.1)

    dtg = get_tg_id(1)
    print(dtg)
    assert dtg['status'] == 'failed'
    sleep(0.1)

    ddel = del_user(id_, new)
    print(dcreate)
    assert ddel['status'] == 'successful'
