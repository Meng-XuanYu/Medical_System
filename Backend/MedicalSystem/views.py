from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import DataError
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import FieldError
from MedicalSystem.auth_backends import *
from MedicalSystem.view_funcs.base_user_funcs import *
from MedicalSystem.view_funcs.menus import *
from MedicalSystem.view_funcs.appointment_funcs import *
import json

from .view_funcs.base_user_funcs import *
from .view_funcs.table_funcs import *

home_url = "login/"


@require_GET
def homepage(request):
    return render(request, 'homepage.html')


@require_GET
def page_register_user(request):
    return render(request, "register_user.html")


@require_GET
def page_register_doctor(request):
    return render(request, "register_doctor.html")


@require_GET
def page_admin_register(request):
    return render(request, "register_admin.html")


@require_GET
def page_login_user(request):
    return render(request, "login_user.html")


@require_GET
def page_login_doctor(request):
    return render(request, "login_doctor.html")


@require_GET
def page_login_admin(request):
    return render(request, "login_admin.html")


@require_GET
def view_doctors_page(request):
    return render(request, "view_doctors.html")


@require_GET
def edit_doctor_page(request):
    return render(request, "edit_doctor.html")


@require_GET
def view_appointments_page(request):
    return render(request, "view_appointments.html")


@require_GET
def edit_appointment_page(request):
    return render(request, "edit_appointment.html")


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def menu_page(request):
    user_type = request.GET.get('user_type')

    # 根据 userType 返回相应菜单数据
    if user_type in menus:
        return JsonResponse(menus[user_type], safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的 user_type 字段'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def register_user(request):
    try:
        data = json.loads(request.body)  # 从请求体解析 JSON 数据

        check_return = fields_check(User, data, True)
        if check_return is not None:
            return check_return

        # 在创建用户前检查是否已存在
        if User.objects.filter(user_id=data['user_id']).exists():
            return JsonResponse({'status': 'error', 'message': '用户已存在'}, status=400)

        # 尝试插入数据
        User.objects.create_base_user(
            base_user_type="user",
            id=data['user_id'],
            password=data['password'],
            name=data['name'],
            gender=data['gender'],
            birth=data['birth'],
            id_number=data['id_number'],
            user_type=data['user_type'],
            phone=data['phone']
        )
        return JsonResponse({'status': 'success', 'message': '用户注册成功'})
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:  # 捕获字段溢出或类型错误
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def register_doctor(request):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        data = json.loads(request.body)  # 从请求体解析 JSON 数据

        check_return = fields_check(Doctor, data, True)
        if check_return is not None:
            return check_return

        # 在创建医师前检查是否已存在
        if Doctor.objects.filter(doctor_id=data['doctor_id']).exists():
            return JsonResponse({'status': 'error', 'message': '医师已存在'}, status=400)

        # 尝试插入数据
        Doctor.objects.create_base_user(
            base_user_type="doctor",
            id=data['doctor_id'],
            password=data['password'],
            name=data['name'],
            gender=data['gender'],
            title=data['title'],
            image_id=data['image_id'],
            introduction=data['introduction']
        )
        return JsonResponse({'status': 'success', 'message': '医师注册成功'})
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:  # 捕获字段溢出或类型错误
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def register_admin(request):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        data = json.loads(request.body)  # 从请求体解析 JSON 数据

        check_return = fields_check(Admin, data, True)
        if check_return is not None:
            return check_return

        # 在创建管理员前检查是否已存在
        if Admin.objects.filter(admin_id=data['admin_id']).exists():
            return JsonResponse({'status': 'error', 'message': '管理员已存在'}, status=400)

        # 尝试插入数据
        Admin.objects.create_superuser(
            base_user_type="admin",
            id=data['admin_id'],
            name=data['name'],
            password=data['password'],
        )
        return JsonResponse({'status': 'success', 'message': '管理员注册成功'})
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:  # 捕获字段溢出或类型错误
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def login(request):
    # 检查当前用户是否已登录
    if is_logged(request.user):
        return JsonResponse({'status': 'error', 'message': '当前已登录'}, status=400)

    try:
        data = json.loads(request.body)  # 从请求体解析 JSON 数据

        match data['user_type']:
            case 's' | 't':
                return login_user(request, data)
            case 'd':
                return login_doctor(request, data)
            case 'a':
                return login_admin(request, data)
            case _:
                return JsonResponse({'status': 'error', 'message': '无效的 user_type 字段'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def logout(request):
    # 检查用户是否已登录
    if not is_logged(request.user):
        return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

    # 执行退出登录操作
    auth_logout(request)
    return JsonResponse({'status': 'success', 'message': '成功退出登录'}, status=200)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def get_all_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return JsonResponse({'status': 'error', 'message': '无效的表名'}, status=400)

    instances = get_instances(model_class)
    return JsonResponse([instance_to_dict(instance) for instance in instances], safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def get_single_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return JsonResponse({'status': 'error', 'message': '无效的表名'}, status=400)

    try:
        data = json.loads(request.body)

        filters = data.get('filters', {})
        instance = get_instance(model_class, **filters)
        return JsonResponse(instance_to_dict(instance), safe=False)
    except model_class.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
    except model_class.MultipleObjectsReturned:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def update_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return JsonResponse({'status': 'error', 'message': '无效的表名'}, status=400)

    try:
        data = json.loads(request.body)

        check_return = fields_check(model_class, data, True)
        if check_return is not None:
            return check_return

        filters = data.get('filters', {})
        updates = data.get('updates', {})
        update_instance(model_class, filters, **updates)
        return JsonResponse({'status': 'success', 'message': f'{model_class.get_chinese_name()}更新成功'})
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:  # 捕获字段溢出或类型错误
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def add_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return JsonResponse({'status': 'error', 'message': '无效的表名'}, status=400)

    try:
        data = json.loads(request.body)

        check_return = fields_check(model_class, data, True)
        if check_return is not None:
            return check_return

        add_instance(model_class, data)
        return JsonResponse({'status': 'success', 'message': f'{model_class.get_chinese_name()}添加成功'})
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:  # 捕获字段溢出或类型错误
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def delete_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return JsonResponse({'status': 'error', 'message': '无效的表名'}, status=400)

    try:
        data = json.loads(request.body)

        filters = data.get('filters', {})
        delete_instance(model_class, **filters)
        return JsonResponse({'success': '记录删除成功'})
    except model_class.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
    except model_class.MultipleObjectsReturned:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_appointment_info(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    departments = get_instances(Department)

    # 构建最终的 JSON 数据结构
    department_data = []
    for department in departments:
        department_info = {
            'department_id': department.department_id,
            'department_name': department.department_name,
            'doctors': get_schedules_by_department(department)
        }
        department_data.append(department_info)

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': department_data}, safe=False)


# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_GET
# def view_doctor(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     doctor_id = request.GET.get('doctor_id')
#     if not doctor_id:
#         return JsonResponse({'status': 'error', 'message': '缺少医工号'}, status=400)
#
#     try:
#         doctor = Doctor.objects.get(doctor_id=doctor_id)
#         data = doctor.get_view_dic()
#         data['status'] = 'success'
#         return JsonResponse(data)
#     except Doctor.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': '医师不存在'}, status=404)
#
#
# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_GET
# def view_doctors(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     doctors = Doctor.objects.all()
#     doctors_list = [doctor.get_view_dic() for doctor in doctors]
#     return JsonResponse({'status': 'success', 'doctors': doctors_list})
#
#
# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_POST
# def edit_doctor(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     try:
#         data = json.loads(request.body)  # 从请求体解析 JSON 数据
#
#         check_return = fields_check(Doctor, data)
#         if check_return is not None:
#             return check_return
#
#         doctor_id = data.get('doctor_id')
#         doctor = Doctor.objects.get(doctor_id=doctor_id)
#
#         # 更新医师信息
#         doctor.name = data.get('name', doctor.name)
#         doctor.gender = data.get('gender', doctor.gender)
#         doctor.title = data.get('title', doctor.title)
#         doctor.image_id = data.get('image_id', doctor.image_id)
#         doctor.introduction = data.get('introduction', doctor.introduction)
#         doctor.save()
#
#         return JsonResponse({'status': 'success', 'message': '医师信息已更新'})
#     except Doctor.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': '医师不存在'}, status=404)
#     except json.JSONDecodeError:
#         return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
#
#
# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_GET
# def view_appointment(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     appointment_id = request.GET.get('appointment_id')
#     if not appointment_id:
#         return JsonResponse({'status': 'error', 'message': '缺少预约号'}, status=400)
#
#     try:
#         appointment = Appointment.objects.get(appointment_id=appointment_id)
#         data = appointment.get_view_dic()
#         data['status'] = 'success'
#         return JsonResponse(data)
#     except Appointment.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': '预约不存在'}, status=404)
#
#
# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_GET
# def view_appointments(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     appointments = Appointment.objects.all()
#     appointments_list = [appointment.get_view_dic() for appointment in appointments]
#     return JsonResponse({'status': 'success', 'appointments': appointments_list})
#
#
# @csrf_exempt  # 临时禁用 CSRF 检查
# @require_POST
# def edit_appointment(request):
#     # 确保当前用户已登录，并且用户类型是 Admin
#     if not is_admin(request.user):
#         return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
#
#     try:
#         data = json.loads(request.body)
#
#         check_return = fields_check(Appointment, data)
#         if check_return is not None:
#             return check_return
#
#         appointment_id = data.get('appointment_id')
#         appointment = Appointment.objects.get(appointment_id=appointment_id)
#
#         # 更新预约信息
#         appointment.relationship = data.get('relationship', appointment.relationship)
#         appointment.schedule_id = data.get('schedule_id', appointment.schedule_id)
#         appointment.user_id = data.get('student_id', appointment.user_id)
#         appointment.save()
#
#         return JsonResponse({'status': 'success', 'message': '预约信息已更新'})
#     except Appointment.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': '预约不存在'}, status=404)
#     except json.JSONDecodeError:
#         return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


# 测试用函数
@require_GET
def get_user_info(request):
    # 检查用户是否已登录
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': '当前未登录'}, status=400)

    user = request.user
    if getattr(user, 'user_id', None) is not None:
        user_info = {
            "base_user_type": "user",
            "id": user.user_id,
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
    else:
        raise ValueError("不存在的基础用户类型")
