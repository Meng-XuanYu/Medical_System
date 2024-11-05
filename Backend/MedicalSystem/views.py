from django.shortcuts import render, redirect
from django.http import HttpResponse
from MedicalSystem.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.db import IntegrityError, DataError
from django.contrib.auth.hashers import make_password, check_password
import json


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("psw")
        if username == "admin" and password == "123456":
            # return HttpResponse("登录成功")
            return redirect("https://buaa.edu.cn/")
        else:
            return render(request, "login.html", {"error_msg": "用户名或密码错误！"})


def orm(request):
    pass


@csrf_exempt  # 临时禁用 CSRF 检查
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            # 获取必填字段及其长度限制
            required_fields = User.get_required_fields()

            # 检查所有必填字段是否存在且不为空
            for field, max_length in required_fields.items():
                if field not in data or not data[field]:
                    return JsonResponse({'status': 'error', 'message': f'缺少必填字段：{field}'}, status=400)
                if max_length and len(data[field]) > max_length:
                    return JsonResponse({'status': 'error', 'message': f'{field}长度不能超过{max_length}个字符'},
                                        status=400)

            # 在创建用户前检查是否已存在
            if User.objects.filter(id=data['id']).exists():
                return JsonResponse({'status': 'error', 'message': '用户已存在'}, status=400)

            # 尝试插入数据
            User.objects.create_user(
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
        try:
            data = json.loads(request.body)  # 从请求体解析 JSON 数据

            # 检查是否提供了学工号和密码
            if 'id' not in data or not data['id']:
                return JsonResponse({'status': 'error', 'message': '缺少学工号'}, status=400)
            if 'password' not in data or not data['password']:
                return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

            # 验证用户信息
            try:
                user = User.objects.get(id=data['id'])
                if check_password(data['password'], user.password):  # 使用 check_password 进行验证
                    return JsonResponse({'status': 'success', 'message': '登录成功'})
                else:
                    return JsonResponse({'status': 'error', 'message': '密码错误'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)