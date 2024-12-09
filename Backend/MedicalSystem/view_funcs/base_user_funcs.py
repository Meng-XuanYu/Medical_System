from django.http import JsonResponse
from django.contrib.auth import authenticate, login


def is_logged(user):
    return user.is_authenticated


def is_user(user):
    return user.is_authenticated and hasattr(user, 'user_id')


def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'user_id') and getattr(user, 'user_type') == 't'


def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'doctor_id')


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'admin_id')


def fields_check(model_class, data, integrity_check=False):
    # 检查必填字段
    required_fields = model_class.get_required_fields()
    if integrity_check is False:
        for field, max_length in required_fields.items():
            if field in data and data[field]:  # 字段存在且不为空
                if max_length and len(data[field]) > max_length:
                    return JsonResponse({'status': 'error', 'message': f'{field}字段长度不能超过{max_length}个字符'},
                                        status=400)
    else:
        for field, max_length in required_fields.items():
            if field not in data or not data[field]:
                return JsonResponse({'status': 'error', 'message': f'缺少必填字段：{field}'}, status=400)
            if type(data[field]) is not int and max_length and len(data[field]) > max_length:
                return JsonResponse({'status': 'error', 'message': f'{field}字段长度不能超过{max_length}个字符'},
                                    status=400)
    # 检查可选字段
    optional_fields = model_class.get_optional_fields()
    for field, max_length in optional_fields.items():
        if field in data and data[field]:  # 字段存在且不为空
            if max_length and len(data[field]) > max_length:
                return JsonResponse({'status': 'error', 'message': f'{field}字段长度不能超过{max_length}个字符'},
                                    status=400)

    # # 检查不存在的字段
    # model_fields = {field.name for field in model_class.get_fields()}
    # for field, value in data.items():
    #     if field not in model_fields:
    #         return JsonResponse({'status': 'error', 'message': f'{field}字段不存在'}, status=400)

    return None


def login_user(request, data):
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


def login_doctor(request, data):
    # 检查是否提供了医工号和密码
    if 'id' not in data or not data['id']:
        return JsonResponse({'status': 'error', 'message': '缺少医工号'}, status=400)
    if 'password' not in data or not data['password']:
        return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

    # 使用 Django 的 authenticate 来验证医师凭据
    doctor = authenticate(request, username=data['id'], password=data['password'],
                          base_user_type='doctor')
    if doctor is not None:
        login(request, doctor)  # 登录并创建会话
        return JsonResponse({'status': 'success', 'message': '医师登录成功'})
    else:
        return JsonResponse({'status': 'error', 'message': '医工号或密码错误'}, status=400)


def login_admin(request, data):
    # 检查是否提供了管理员号和密码
    if 'id' not in data or not data['id']:
        return JsonResponse({'status': 'error', 'message': '缺少管理员号'}, status=400)
    if 'password' not in data or not data['password']:
        return JsonResponse({'status': 'error', 'message': '缺少密码'}, status=400)

    # 使用 Django 的 authenticate 来验证管理员凭据
    admin = authenticate(request, username=data['id'], password=data['password'], base_user_type='admin')
    if admin is not None:
        login(request, admin)  # 登录并创建会话
        return JsonResponse({'status': 'success', 'message': '管理员登录成功'})
    else:
        return JsonResponse({'status': 'error', 'message': '管理员号或密码错误'}, status=400)
