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


# 2. 测试用户登录
def test_user_login():
    url = f"{base_url}/api/user/login/"
    data = {
        "id": "001",
        "password": "mypassword"
    }
    response = requests.post(url, json=data)
    print("登录响应:", response.json())


# 执行测试
if __name__ == "__main__":
    print("---- 用户注册测试 ----")
    test_user_register()
    print("\n---- 用户登录测试 ----")
    test_user_login()
