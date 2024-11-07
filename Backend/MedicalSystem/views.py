from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import DataError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .auth_backends import *
import json

home_url = "login/"


def homepage(request):
    return render(request, 'homepage.html')


def user_register_page(request):
    if request.method == "GET":
        return render(request, "user_register.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def doctor_register_page(request):
    if request.method == "GET":
        return render(request, "doctor_register.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def admin_register_page(request):
    if request.method == "GET":
        return render(request, "admin_register.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def user_login_page(request):
    if request.method == "GET":
        return render(request, "user_login.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def doctor_login_page(request):
    if request.method == "GET":
        return render(request, "doctor_login.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def admin_login_page(request):
    if request.method == "GET":
        return render(request, "admin_login.html")

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)


def orm(request):
    pass


@csrf_exempt  # 临时禁用 CSRF 检查
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            fields_check(User, data)

            # 在创建用户前检查是否已存在
            if User.objects.filter(id=data['id']).exists():
                return JsonResponse({'status': 'error', 'message': '用户已存在'}, status=400)

            # 尝试插入数据
            User.objects.create_base_user(
                base_user_type="user",
                id=data['id'],
                password=data['password'],
                name=data['name'],
                gender=data['gender'],
                birth=data['birth'],
                id_number=data['id_number'],
                user_type=data['user_type'],
                phone=data['phone']
            )
            return JsonResponse({'status': 'success', 'message': '注册成功'})
        except DataError:  # 捕获字段溢出或类型错误
            return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
def user_login(request):
    if request.method == 'POST':
        # 检查当前用户是否已登录
        if request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前已登录'}, status=400)

        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            # 检查是否提供了学工号和密码
            if 'id' not in data or not data['id']:
                return JsonResponse({'status': 'error', 'message': '缺少学工号'}, status=400)
            if 'password' not in data or not data['password']:
                return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

            # 使用 Django 的 authenticate 来验证用户凭据
            user = authenticate(request, username=data['id'], password=data['password'], base_user_type='user')
            if user is not None:
                login(request, user)  # 登录并创建会话
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '学工号或密码错误'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
# @login_required
def user_logout(request):
    if request.method == 'POST':
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

        # 执行退出登录操作
        logout(request)
        return JsonResponse({'status': 'success', 'message': '成功退出登录'}, status=200)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
def doctor_register(request):
    if request.method == 'POST':
        # 确保当前用户已登录，并且用户类型是 Admin
        if not request.user.is_authenticated or getattr(request.user, 'admin_id', None) is None:
            return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            fields_check(Doctor, data)

            # 在创建医生前检查是否已存在
            if Doctor.objects.filter(staff_id=data['staff_id']).exists():
                return JsonResponse({'status': 'error', 'message': '医生已存在'}, status=400)

            # 尝试插入数据
            Doctor.objects.create_base_user(
                base_user_type="doctor",
                id=data['staff_id'],
                password=data['password'],
                name=data['name'],
                gender=data['gender'],
                title=data['title'],
                image_id=data['image_id'],
                introduction=data['introduction']
            )
            return JsonResponse({'status': 'success', 'message': '医生注册成功'})
        except DataError:  # 捕获字段溢出或类型错误
            return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
def doctor_login(request):
    if request.method == 'POST':
        # 检查当前用户是否已登录
        if request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前已登录'}, status=400)

        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            # 检查是否提供了医工号和密码
            if 'staff_id' not in data or not data['staff_id']:
                return JsonResponse({'status': 'error', 'message': '缺少医工号'}, status=400)
            if 'password' not in data or not data['password']:
                return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

            # 使用 Django 的 authenticate 来验证医生凭据
            doctor = authenticate(request, username=data['staff_id'], password=data['password'],
                                  base_user_type='doctor')
            if doctor is not None:
                login(request, doctor)  # 登录并创建会话
                return JsonResponse({'status': 'success', 'message': '医生登录成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '医工号或密码错误'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
# @login_required
def doctor_logout(request):
    if request.method == 'POST':
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

        # 执行退出登录操作
        logout(request)
        return JsonResponse({'status': 'success', 'message': '医生成功退出登录'}, status=200)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
def admin_register(request):
    if request.method == 'POST':
        # 确保当前用户已登录，并且用户类型是 Admin
        if not request.user.is_authenticated or getattr(request.user, 'admin_id', None) is None:
            return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            fields_check(Admin, data)

            # 在创建管理员前检查是否已存在
            if Admin.objects.filter(admin_id=data['admin_id']).exists():
                return JsonResponse({'status': 'error', 'message': '管理员已存在'}, status=400)

            # 尝试插入数据
            Admin.objects.create_base_user(
                base_user_type="admin",
                id=data['admin_id'],
                name=data['name'],
                password=data['password'],
            )
            return JsonResponse({'status': 'success', 'message': '管理员注册成功'})
        except DataError:  # 捕获字段溢出或类型错误
            return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
def admin_login(request):
    if request.method == 'POST':
        # 检查当前用户是否已登录
        if request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前已登录'}, status=400)

        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            # 检查是否提供了管理员号和密码
            if 'admin_id' not in data or not data['admin_id']:
                return JsonResponse({'status': 'error', 'message': '缺少管理员号'}, status=400)
            if 'password' not in data or not data['password']:
                return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

            # 使用 Django 的 authenticate 来验证管理员凭据
            admin = authenticate(request, username=data['admin_id'], password=data['password'], base_user_type='admin')
            if admin is not None:
                login(request, admin)  # 登录并创建会话
                return JsonResponse({'status': 'success', 'message': '管理员登录成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '管理员号或密码错误'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt  # 临时禁用 CSRF 检查
# @login_required
def admin_logout(request):
    if request.method == 'POST':
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

        # 执行退出登录操作
        logout(request)
        return JsonResponse({'status': 'success', 'message': '管理员退出登录成功'}, status=200)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)


def fields_check(model_class, data):
    # 获取必填字段及其长度限制
    required_fields = model_class.get_required_fields()

    # 检查所有必填字段是否存在且不为空
    for field, max_length in required_fields.items():
        if field not in data or not data[field]:
            return JsonResponse({'status': 'error', 'message': f'缺少必填字段：{field}'}, status=400)
        if max_length and len(data[field]) > max_length:
            return JsonResponse({'status': 'error', 'message': f'{field}长度不能超过{max_length}个字符'},
                                status=400)

    # 检查可选字段
    optional_fields = model_class.get_optional_fields()
    for field, max_length in optional_fields.items():
        if field in data and data[field]:  # 字段存在且不为空
            if max_length and len(data[field]) > max_length:
                return JsonResponse({'status': 'error', 'message': f'{field}长度不能超过{max_length}个字符'},
                                    status=400)


# 测试用函数
def get_user_info(request):
    if request.method == "GET":
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

        user = request.user
        if getattr(user, 'id', None) is not None:
            user_info = {
                "base_user_type": "user",
                "id": user.id,
                "name": user.name
            }
            return JsonResponse(user_info)
        elif getattr(user, 'doctor_id', None) is not None:
            user_info = {
                "base_user_type": "doctor",
                "id": user.doctor_id,
                "name": user.name
            }
            return JsonResponse(user_info)
        elif getattr(user, 'admin_id', None) is not None:
            user_info = {
                "base_user_type": "admin",
                "id": user.admin_id,
                "name": user.name
            }
            return JsonResponse(user_info)

    return JsonResponse({'status': 'error', 'message': '仅支持 GET 请求'}, status=405)
