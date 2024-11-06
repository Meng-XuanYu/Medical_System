import requests
import json

# 设置服务器地址
base_url = 'http://127.0.0.1:8000'  # 如果在其他服务器上运行，请替换为相应IP地址或域名


# 1. 测试用户注册
def test_user_register():
    url = f"{base_url}/api/user/register/"
    data = {
        "id": "1",
        "password": "1",
        "name": "mxy",
        "gender": "畜",
        "birth": "2024-11-05",
        "id_number": "11451420241105J8J8",
        "user_type": "S",
        "phone": "11451419198"
    }
    response = requests.post(url, json=data)
    print("注册响应:", response.json())


# 2. 测试用户登录并退出
def test_user_login_and_logout():
    # 创建会话
    session = requests.Session()

    # 登录
    url_login = f"{base_url}/api/user/login/"
    data_login = {
        "id": "001",
        "password": "mypassword"
    }
    response_login = session.post(url_login, json=data_login)
    print("登录响应:", response_login.json())

    # 检查登录是否成功
    if response_login.json().get('status') == 'success':
        # 从响应的 cookies 中获取 CSRF token
        csrf_token = session.cookies.get('csrftoken')

        # 退出
        url_logout = f"{base_url}/api/user/logout/"
        headers = {
            "X-CSRFToken": csrf_token  # 设置 CSRF token 头
        }
        response_logout = session.post(url_logout, headers=headers)
        print("退出响应:", response_logout.json())
    else:
        print("登录失败，无法测试退出功能。")


# 测试医生注册
def test_doctor_register():
    url = f"{base_url}/api/doctor/register/"
    data = {
        "staff_id": "1001",
        "password": "password123",
        "name": "Dr. Li",
        "gender": "M",
        "title": "Chief",
        "image_id": None,
        "introduction": "Experienced doctor in surgery."
    }
    response = requests.post(url, json=data)
    print("医生注册响应:", response.json())


# 测试医生登录并退出
def test_doctor_login_and_logout():
    session = requests.Session()

    # 登录
    url_login = f"{base_url}/api/doctor/login/"
    data_login = {
        "staff_id": "1001",
        "password": "password123"
    }
    response_login = session.post(url_login, json=data_login)
    print("医生登录响应:", response_login.json())

    if response_login.json().get('status') == 'success':
        csrf_token = session.cookies.get('csrftoken')

        # 退出
        url_logout = f"{base_url}/api/doctor/logout/"
        headers = {
            "X-CSRFToken": csrf_token
        }
        response_logout = session.post(url_logout, headers=headers)
        print("医生退出响应:", response_logout.json())
    else:
        print("医生登录失败，无法测试退出功能。")


# Admin 注册、登录和退出的测试函数
def test_admin_register():
    url = f"{base_url}/api/admin/register/"
    data = {
        "admin_id": "001",
        "password": "adminpassword",
        "name": "Admin Zhang"
    }
    response = requests.post(url, json=data)
    print("管理员注册响应:", response.json())


def test_admin_login_and_logout():
    session = requests.Session()

    # 登录
    url_login = f"{base_url}/api/admin/login/"
    data_login = {
        "admin_id": "001",
        "password": "adminpassword"
    }
    response_login = session.post(url_login, json=data_login)
    print("管理员登录响应:", response_login.json())

    if response_login.json().get('status') == 'success':
        csrf_token = session.cookies.get('csrftoken')

        # 退出
        url_logout = f"{base_url}/api/admin/logout/"
        headers = {
            "X-CSRFToken": csrf_token
        }
        response_logout = session.post(url_logout, headers=headers)
        print("管理员退出响应:", response_logout.json())
    else:
        print("管理员登录失败，无法测试退出功能。")


# 执行测试
if __name__ == "__main__":
    print("---- 用户注册测试 ----")
    test_user_register()
    print("\n---- 用户登录与退出测试 ----")
    test_user_login_and_logout()
    print("---- 医生注册测试 ----")
    test_doctor_register()
    print("\n---- 医生登录与退出测试 ----")
    test_doctor_login_and_logout()
    print("\n---- 管理员注册测试 ----")
    test_admin_register()
    print("\n---- 管理员登录与退出测试 ----")
    test_admin_login_and_logout()
