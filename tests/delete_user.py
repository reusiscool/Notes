from api_tests import login, del_user


if __name__ == '__main__':
    data = login('ADMIN', 'ADMIN')
    if data['status'] == 'failed':
        data = login('ADMIN', 'ADMIN_NEW')
        ans = del_user(data['id'], 'ADMIN_NEW')
        print(ans)
    else:
        ans = del_user(data['id'], 'ADMIN')
        print(ans)
