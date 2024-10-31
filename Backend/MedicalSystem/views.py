from django.shortcuts import render, redirect
from django.http import HttpResponse
from MedicalSystem.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.db import IntegrityError
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
            user_id = data.get('id')
            password = data.get('password')
            name = data.get('name')
            gender = data.get('gender')
            birth = data.get('birth')
            id_number = data.get('id_number')
            user_type = data.get('user_type')
            phone = data.get('phone')

            if not all([user_id, password, name, gender, birth, id_number, user_type, phone]):
                return JsonResponse({'status': 'error', 'message': '请填写所有必填字段'}, status=400)

            User.objects.create(
                id=user_id,
                password=password,
                name=name,
                gender=gender,
                birth=birth,
                id_number=id_number,
                user_type=user_type,
                phone=phone
            )
            return JsonResponse({'status': 'success', 'message': '注册成功'})
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': '用户已存在'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)
