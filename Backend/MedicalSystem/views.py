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


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_appointment_info(request):
    # 确保当前用户已登录
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取 relationship 参数
    relationship = request.GET.get('relation')
    if not relationship:
        return JsonResponse({'status': 'error', 'message': '缺少 relation 参数'}, status=400)

    # 查询当前用户和指定 relationship 的预约信息
    appointments = Appointment.objects.filter(user=request.user, relationship=relationship).select_related(
        'schedule__doctor')

    # 构建返回的数据结构
    appointment_data = []
    for appointment in appointments:
        schedule = appointment.schedule
        doctor = schedule.doctor if schedule else None
        appointment_info = {
            'appointment_id': appointment.appointment_id,
            'doctor_name': doctor.name if doctor else None,
            'schedule_time': schedule.schedule_time if schedule else None,
            'state': appointment.state
        }
        appointment_data.append(appointment_info)

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': appointment_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def appointment_reserve(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    schedule_id = data.get('schedule_id')
    relationship = data.get('relationship')

    if not schedule_id:
        return JsonResponse({'status': 'error', 'message': '排班 ID 不能为空'}, status=400)
    if not relationship:
        return JsonResponse({'status': 'error', 'message': '与用户关系不能为空'}, status=400)

    # 查询 Schedule 是否存在
    try:
        schedule = Schedule.objects.get(schedule_id=schedule_id)
    except Schedule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的排班 ID'}, status=404)

    # 生成新的 appointment_id
    appointment_id = Appointment.generate_incremental_appointment_id()

    # 创建新的预约记录
    Appointment.objects.create(
        appointment_id=appointment_id,
        relationship=relationship,
        schedule=schedule,
        user=request.user,
        state='未开始'  # 设置初始状态
    )

    return JsonResponse({'status': 'success', 'message': '预约成功'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def appointment_cancel(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取请求体数据
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    # 提取必要的字段
    appointment_id = data.get('appointment_id')
    relationship = data.get('relation')

    if not appointment_id:
        return JsonResponse({'status': 'error', 'message': '预约 ID 不能为空'}, status=400)
    if not relationship:
        return JsonResponse({'status': 'error', 'message': '与用户关系不能为空'}, status=400)

    try:
        # 查找 Appointment 记录
        appointment = Appointment.objects.get(
            appointment_id=appointment_id,
            relationship=relationship,
            user=request.user
        )
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '未找到匹配的预约记录'}, status=404)

    # 更新状态为 "已取消"
    appointment.state = '已取消'
    appointment.save()

    return JsonResponse({'status': 'success', 'message': '预约已取消'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_examination_info(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取所有 ExaminationArrangement 实例
    examination_arrangements = get_instances(ExaminationArrangement)

    # 构建 JSON 数据结构
    examination_data = []
    for exam in examination_arrangements:
        # 获取医生的信息
        doctor = exam.doctor
        doctor_info = {
            'name': doctor.name,
            'gender': doctor.gender,
            'title': doctor.title,
            'image_id': doctor.image_id
        } if doctor else None

        # 构建体检安排的信息
        exam_info = {
            'examination_id': exam.examination_id,
            'examination': exam.examination,
            'examination_date': exam.examination_date,
            'doctor': doctor_info
        }
        examination_data.append(exam_info)

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': examination_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_examination_info(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 查询 ExaminationInfo 表中 user 为当前用户的记录
    examination_info_list = ExaminationInfo.objects.filter(user=request.user)

    # 构建 JSON 数据结构
    examination_data = []
    for exam_info in examination_info_list:
        # 获取相关的 ExaminationArrangement 信息
        arrangement = exam_info.examination_arrangement
        if arrangement:
            doctor = arrangement.doctor
            # 构建医生的信息
            doctor_info = {
                'name': doctor.name if doctor else None
            }

            # 构建体检安排的信息
            arrangement_info = {
                'examination': arrangement.examination,
                'examination_date': arrangement.examination_date,
                'doctor': doctor_info
            }
        else:
            arrangement_info = None

        # 构建体检信息的数据
        info = {
            'exam_appointment_id': exam_info.exam_appointment_id,
            'examination_arrangement': arrangement_info,
            'examination_result': exam_info.examination_result,
            'state': exam_info.state
        }
        examination_data.append(info)

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': examination_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def examination_reserve(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    examination_id = data.get('examination_id')

    if not examination_id:
        return JsonResponse({'status': 'error', 'message': '体检项目 ID 不能为空'}, status=400)

    # 查询 ExaminationArrangement 是否存在
    try:
        arrangement = ExaminationArrangement.objects.get(examination_id=examination_id)
    except ExaminationArrangement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的体检项目 ID'}, status=404)

    # 生成唯一的 exam_appointment_id
    exam_appointment_id = ExaminationInfo.generate_incremental_exam_appointment_id()

    # 添加记录到 ExaminationInfo 表
    ExaminationInfo.objects.create(
        exam_appointment_id=exam_appointment_id,
        examination_arrangement=arrangement,
        examination_result=None,
        user=request.user,
        state="未开始"
    )
    return JsonResponse({'status': 'success', 'message': '预约成功'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def examination_cancel(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    exam_appointment_id = data.get('exam_appointment_id')

    if not exam_appointment_id:
        return JsonResponse({'status': 'error', 'message': '预约 ID 不能为空'}, status=400)

    try:
        # 查找对应的预约信息
        examination_info = ExaminationInfo.objects.get(exam_appointment_id=exam_appointment_id)

        # 检查当前用户是否与预约信息中的用户一致
        if examination_info.user != request.user:
            return JsonResponse({'status': 'error', 'message': '权限错误，无法取消他人预约'}, status=403)

        # 更新预约状态为 "已取消"
        examination_info.state = "已取消"
        examination_info.save()

        return JsonResponse({'status': 'success', 'message': '预约已取消'})

    except ExaminationInfo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '预约记录不存在'}, status=404)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_family_members(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_teacher(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 查询当前用户的所有家属信息
    family_members = FamilyMember.objects.filter(user=request.user)

    # 构建返回的 JSON 数据结构
    family_data = [
        {
            'family_id': member.family_id,
            'relationship': member.relationship,
            'name': member.name,
            'gender': member.gender,
            'birth': member.birth.strftime('%Y-%m-%d'),
            'id_number': member.id_number,
        }
        for member in family_members
    ]

    return JsonResponse({'status': 'success', 'data': family_data})


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
