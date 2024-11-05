import requests
import json

# 设置服务器地址
base_url = 'http://127.0.0.1:8000'  # 如果在其他服务器上运行，请替换为相应IP地址或域名


# 1. 测试用户注册
def test_user_register():
    url = f"{base_url}/api/user/register/"
    data = {
        "id": "001",
        "password": "mypassword",
        "name": "Alice",
        "gender": "女",
        "birth": "1990-01-01",
        "id_number": "123456789012345678",
        "user_type": "1",
        "phone": "12345678901"
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


# 执行测试
if __name__ == "__main__":
    print("---- 用户注册测试 ----")
    test_user_register()
    print("\n---- 用户登录与退出测试 ----")
    test_user_login_and_logout()
