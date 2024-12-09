from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import DataError
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import FieldError
from MedicalSystem.view_funcs.menus import *
from MedicalSystem.view_funcs.appointment_funcs import *
import json
import time

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

        data = request.POST.dict()
        image_file = request.FILES.get('image')
        if image_file is None:
            return JsonResponse({'status': 'error', 'message': '未上传头像'}, status=400)
        image = Image.objects.create(image=image_file)
        # 在创建用户前检查是否已存在
        if User.objects.filter(user_id=data['username']).exists():
            return JsonResponse({'status': 'error', 'message': '用户已存在'}, status=400)

        # 尝试插入数据
        User.objects.create_base_user(
            base_user_type="user",
            id=data['username'],
            password=data['password'],
            name=data['name'],
            gender=data['gender'],
            birth=data['borndate'],
            id_number=data['identity'],
            user_type=data['usertype'],
            phone=data['phone'],
            image=image
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
        # 在创建医师前检查是否已存在
        if Doctor.objects.filter(doctor_id=request.POST.get('doctor_id')).exists():
            return JsonResponse({'status': 'error', 'message': '医师已存在'}, status=400)

        # 尝试插入数据
        image_file = request.FILES.get('image')
        if image_file is None:
            return JsonResponse({'status': 'error', 'message': '未上传医师头像'}, status=400)
        image = Image.objects.create(image=image_file)
        Doctor.objects.create_base_user(
            base_user_type="doctor",
            id=request.POST.get('doctor_id'),
            password=request.POST.get('password'),
            name=request.POST.get('name'),
            gender=request.POST.get('gender'),
            title=request.POST.get('title'),
            image=image,
            introduction=request.POST.get('introduction')
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
    # if not is_admin(request.user):
    #   return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

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
@require_GET
def get_base_user_profile(request):
    # 确保当前用户已登录
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': '用户未登录'}, status=403)

    # 获取当前登录用户
    user = request.user

    try:
        # 判断用户类型并获取对应信息
        if hasattr(user, 'user_id'):  # 普通用户
            user_instance = User.objects.get(user_id=user.user_id)
            user_data = {
                'user_type': 'User',
                'user_id': user_instance.user_id,
                'name': user_instance.name,
                'gender': user_instance.gender,
                'birth': user_instance.birth,
                'image_url': request.build_absolute_uri(user_instance.image.image.url),
                'id_number': user_instance.id_number,
                'phone': user_instance.phone,
            }
        elif hasattr(user, 'doctor_id'):  # 医师
            doctor_instance = Doctor.objects.get(doctor_id=user.doctor_id)
            user_data = {
                'user_type': 'Doctor',
                'doctor_id': doctor_instance.doctor_id,
                'name': doctor_instance.name,
                'gender': doctor_instance.gender,
                'title': doctor_instance.title,
                'image_id': doctor_instance.image_id,
                'introduction': doctor_instance.introduction,
            }
        elif hasattr(user, 'admin_id'):  # 管理员
            admin_instance = Admin.objects.get(admin_id=user.admin_id)
            user_data = {
                'user_type': 'Admin',
                'admin_id': admin_instance.admin_id,
                'name': admin_instance.name,
            }
        else:
            return JsonResponse({'status': 'error', 'message': '无法识别的用户类型'}, status=400)

        # 返回用户详细信息
        return JsonResponse({'status': 'success', 'data': user_data}, status=200)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'获取用户信息失败: {str(e)}'}, status=500)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def get_all_record(request, model_name):
    # 确保当前用户已登录，并且用户类型是 Admin

    if model_name != 'examinations':
        if not is_admin(request.user):
            return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)
    else:
        model_name = 'examination'

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

        # 获取主键字段名称
        primary_key_field = model_class.get_primary_key_field()
        primary_key_value = data.get(primary_key_field)
        if not primary_key_value:
            return JsonResponse({'status': 'error', 'message': f'{primary_key_field} 不能为空'}, status=400)

        # 按主键查询记录
        instance = model_class.objects.get(pk=primary_key_value)

        # 更新其他属性
        updates = {key: value for key, value in data.items() if key != primary_key_field}
        for attr, value in updates.items():
            setattr(instance, attr, value)
        instance.save()

        return JsonResponse({'status': 'success', 'message': f'{model_class.get_chinese_name()}更新成功'})
    except model_class.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
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

        # 获取主键字段名称
        primary_key_field = model_class.get_primary_key_field()
        primary_key_value = data.get(primary_key_field)
        if not primary_key_value:
            return JsonResponse({'status': 'error', 'message': f'{primary_key_field} 不能为空'}, status=400)

        # 按主键删除记录
        instance = model_class.objects.get(pk=primary_key_value)
        instance.delete()

        return JsonResponse({'status': 'success', 'message': f'{model_class.get_chinese_name()}删除成功'})
    except model_class.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'{model_class.get_chinese_name()}不存在'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def notice(request):
    # 管理员发布公告
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        data = json.loads(request.body)
        user = User.objects.get(user_id=data.get('user'))
        Notification.objects.create(
            user=user,
            notification=data.get('notification'),
            notification_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        )
        return JsonResponse({'status': 'success', 'message': '发布成功'}, status=200)
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


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
            'department': department.department_name,
            'doctors': get_schedules_by_department(department)
        }
        department_data.append(department_info)

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': department_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
def user_comment(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        data = json.loads(request.body)
        print(data)
        doctor = Doctor.objects.get(doctor_id=data.get('doctor_id'))
        evaluation = Evaluation.objects.create(
            user=request.user,
            doctor=doctor,
            evaluation=data.get('evaluation'),
            evaluation_star=data.get('star'),
            evaluation_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        )
        return JsonResponse({'status': 'success',
                             'user_image': request.build_absolute_uri(request.user.image.image.url),
                             'evaluation_id': evaluation.evaluation_id,
                             'time': evaluation.evaluation_time,
                             'star': evaluation.evaluation_star,
                             'evaluation': evaluation.evaluation,
                             'user_id': evaluation.user.user_id
                             }, status=200)
    except FieldError:
        return JsonResponse({'status': 'error', 'message': '存在非法字段'}, status=400)
    except DataError:
        return JsonResponse({'status': 'error', 'message': '数据超出字段限制或无效'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)


@csrf_exempt  # 临时禁用 CSRF 检查
def get_doctors_comments(request):
    # 获取所有医生的信息及评价
    doctors = get_instances(Doctor)
    doctor_data = []
    for doctor in doctors:
        evaluations = Evaluation.objects.filter(doctor_id=doctor.doctor_id)
        evaluation_data = []
        for evaluation in evaluations:
            evaluation_info = {
                'user_image': request.build_absolute_uri(evaluation.user.image.image.url),
                'user_id': evaluation.user.user_id,
                'evaluation': evaluation.evaluation,
                'time': evaluation.evaluation_time.strftime('%Y-%m-%d %H:%M:%S'),
                'star': evaluation.evaluation_star
            }
            evaluation_data.append(evaluation_info)
        doctor_info = {
            'doctor_id': doctor.doctor_id,
            'name': doctor.name,
            'title': doctor.title,
            'image_id': request.build_absolute_uri(doctor.image.image.url),
            'introduction': doctor.introduction,
            'evaluations': evaluation_data
        }
        doctor_data.append(doctor_info)
    return JsonResponse({'status': 'success', 'doctors': doctor_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_appointment_info(request):
    # 确保当前用户已登录
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取 relationship 参数
    relationship = request.GET.get('relation')
    if not relationship:
        return JsonResponse({'status': 'error', 'message': 'relation 不能为空'}, status=400)

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
            'doctor_id': doctor.doctor_id if doctor else None,
            'doctor_name': doctor.name if doctor else None,
            'doctor_image': request.build_absolute_uri(doctor.image.image.url) if doctor else None,
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
    relationship = data.get('relation')

    if not schedule_id:
        return JsonResponse({'status': 'error', 'message': 'schedule_id 不能为空'}, status=400)
    if not relationship:
        return JsonResponse({'status': 'error', 'message': 'relation 不能为空'}, status=400)

    # 查询 Schedule 是否存在
    try:
        schedule = Schedule.objects.get(schedule_id=schedule_id)
    except Schedule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的排班 schedule_id'}, status=404)
    # 当存在未完成的预约时，不允许重复预约
    if Appointment.objects.filter(user=request.user, relationship=relationship, state='未开始').exists():
        return JsonResponse({'status': 'error', 'message': '存在未完成的预约'}, status=400)
    # 创建新的预约记录
    Appointment.objects.create(
        appointment_id=Appointment.generate_incremental_appointment_id(),
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
        return JsonResponse({'status': 'error', 'message': 'appointment_id 不能为空'}, status=400)
    if not relationship:
        return JsonResponse({'status': 'error', 'message': 'relation 不能为空'}, status=400)

    try:
        # 查找 Appointment 记录
        appointment = Appointment.objects.get(
            appointment_id=appointment_id,
            relationship=relationship,
            user=request.user
        )
    except Appointment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的 appointment_id'}, status=404)

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
        return JsonResponse({'status': 'error', 'message': 'examination_id 不能为空'}, status=400)

    # 查询 ExaminationArrangement 是否存在
    try:
        arrangement = ExaminationArrangement.objects.get(examination_id=examination_id)
    except ExaminationArrangement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的 examination_id'}, status=404)

    # 添加记录到 ExaminationInfo 表
    ExaminationInfo.objects.create(
        exam_appointment_id=ExaminationInfo.generate_incremental_exam_appointment_id(),
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
        return JsonResponse({'status': 'error', 'message': 'exam_appointment_id 不能为空'}, status=400)

    try:
        # 查找对应的预约信息
        examination_info = ExaminationInfo.objects.get(exam_appointment_id=exam_appointment_id)

        # 检查当前用户是否与预约信息中的用户一致
        if examination_info.user != request.user:
            return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

        # 更新预约状态为 "已取消"
        examination_info.state = "已取消"
        examination_info.save()

        return JsonResponse({'status': 'success', 'message': '预约已取消'})

    except ExaminationInfo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '预约记录不存在'}, status=404)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_wait(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录用户
    user = request.user

    try:
        # 查询用户未完成的预约
        appointment = (
            Appointment.objects.filter(user=user, state="未开始")
            .order_by('schedule__schedule_time', 'appointment_id')
            .first()
        )

        if not appointment:
            return JsonResponse({'status': 'success', 'data': ""}, status=200)

        # 获取对应的排班信息
        schedule = appointment.schedule

        # 统计该时间段前方未完成人数
        wait_count = Appointment.objects.filter(
            schedule=schedule,
            state="未开始",
            appointment_id__lt=appointment.appointment_id  # 按预约号顺序计算
        ).count()

        # 返回预约详情和等待人数
        response_data = {
            'appointment_id': appointment.appointment_id,
            'relationship': appointment.relationship,
            'schedule_id': schedule.schedule_id,
            'schedule_time': schedule.schedule_time,
            'doctor_id': schedule.doctor.doctor_id,
            'doctor_name': schedule.doctor.name,
            'department_id': schedule.department.department_id,
            'department_name': schedule.department.name,
            'state': appointment.state,
            'wait_count': wait_count,
        }

        return JsonResponse({'status': 'success', 'data': response_data}, status=200)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'查询失败: {str(e)}'}, status=500)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_prescriptions(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录用户
    user = request.user

    # 查询与用户相关的所有预约记录
    appointments = Appointment.objects.filter(user=user)

    # 查询这些预约关联的诊断记录
    diagnoses = Diagnosis.objects.filter(appointment__in=appointments)

    # 查询与诊断关联的处方记录
    prescriptions = Prescription.objects.filter(diagnosis__in=diagnoses).select_related('drug', 'diagnosis')

    # 构建返回数据
    prescriptions_list = []
    for prescription in prescriptions:
        prescriptions_list.append({
            'prescription_id': prescription.prescription_id,
            'diagnosis_id': prescription.diagnosis.diagnosis_id,
            'drug_id': prescription.drug.drug_id,
            'drug_name': prescription.drug.drug_name,
            'drug_amount': prescription.drug_amount,
            'usage': prescription.usage,
            'precautions': prescription.precautions,
        })

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': prescriptions_list})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_ill_history(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录用户
    user = request.user

    # 查询与用户相关的所有预约记录
    appointments = Appointment.objects.filter(user=user).select_related('schedule')

    # 查询这些预约关联的诊断记录
    diagnoses = Diagnosis.objects.filter(appointment__in=appointments).select_related('doctor', 'appointment')

    # 构建返回数据
    ill_history = []
    for diagnosis in diagnoses:
        schedule = diagnosis.appointment.schedule
        ill_history.append({
            'diagnosis_id': diagnosis.diagnosis_id,
            'examination': diagnosis.examination,
            'examination_result': diagnosis.examination_result,
            'reference': diagnosis.reference,
            'clinical_diagnosis': diagnosis.clinical_diagnosis,
            'diagnosis_time': diagnosis.diagnosis_time.strftime('%Y-%m-%d %H:%M:%S'),
            'doctor_name': diagnosis.doctor.name if diagnosis.doctor else None,
            'department_name': schedule.department.department_name if schedule.department else None,
            'appointment_id': diagnosis.appointment.appointment_id
        })

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': ill_history})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_payments(request):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前用户
    user = request.user

    # 查询当前用户的支付记录
    payments = Payment.objects.filter(user=user).order_by('-payment_id')

    # 构建支付信息列表
    payment_data = [
        {
            'payment_id': payment.payment_id,
            'payment_name': payment.payment_name,
            'payment_description': payment.payment_description,
            'money': payment.money,
            'is_paid': payment.is_paid,
        }
        for payment in payments
    ]

    # 返回支付记录
    return JsonResponse({
        'status': 'success',
        'data': payment_data
    }, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_user_payment_check(request, payment_id):
    # 确保当前用户已登录，并且用户类型是 User
    if not is_user(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前用户
    user = request.user

    try:
        # 查询对应支付记录
        payment = Payment.objects.get(payment_id=payment_id)

        # 验证支付记录是否属于当前用户
        if payment.user != user:
            return JsonResponse({'status': 'error', 'message': '权限错误：无法访问他人支付信息'}, status=403)

        # 检查是否已支付
        if payment.is_paid:
            return JsonResponse({'status': 'success', 'message': '支付已完成', 'is_paid': True})
        else:
            return JsonResponse({'status': 'success', 'message': '支付未完成', 'is_paid': False})

    except Payment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '支付记录不存在'}, status=404)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_family_members(request):
    # 确保当前用户已登录，并且用户为教师
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


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def update_family_members(request):
    # 确保当前用户已登录，并且用户为教师
    if not is_teacher(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    family_id = data.get('family_id')
    if not family_id:
        return JsonResponse({'status': 'error', 'message': 'family_id 不能为空'}, status=400)

    # 查找指定 family_id 且属于当前用户的家属记录
    try:
        family_member = FamilyMember.objects.get(user=request.user, family_id=family_id)
    except FamilyMember.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的 family_id'}, status=404)

    check_return = fields_check(Admin, data, False)
    if check_return is not None:
        return check_return

    # 更新字段
    for field in FamilyMember.allowed_update_fields():
        if field in data:
            setattr(family_member, field, data[field])

    # 保存更新
    family_member.save()

    return JsonResponse({'status': 'success', 'message': '家属信息更新成功'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def add_family_members(request):
    # 确保当前用户已登录，并且用户为教师
    if not is_teacher(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    fields_check(FamilyMember, data, True)

    # 创建新的家属记录
    FamilyMember.objects.create(
        family_id=FamilyMember.generate_incremental_family_id(),
        user=request.user,
        relationship=data['relationship'],
        name=data['name'],
        gender=data['gender'],
        birth=data['birth'],
        id_number=data['id_number']
    )

    return JsonResponse({'status': 'success', 'message': '家属添加成功'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def delete_family_members(request):
    # 确保当前用户已登录，并且用户为教师
    if not is_teacher(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    try:
        # 获取传入的参数
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    family_id = data.get('family_id')
    if not family_id:
        return JsonResponse({'status': 'error', 'message': 'family_id 不能为空'}, status=400)

    # 查找家属记录
    try:
        family_member = FamilyMember.objects.get(user=request.user, family_id=family_id)
    except FamilyMember.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '无效的 family_id'}, status=404)

    # 删除家属记录
    family_member.delete()

    return JsonResponse({'status': 'success', 'message': '家属删除成功'})


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_schedule(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取与当前登录医师相关的排班数据
    doctor = request.user
    schedules = Schedule.objects.filter(doctor=doctor).select_related('department')

    # 构建结果数据
    schedule_data = [
        {
            'schedule_id': schedule.schedule_id,
            'schedule_time': schedule.schedule_time,
            'department_name': schedule.department.department_name,
        }
        for schedule in schedules
    ]

    return JsonResponse({'status': 'success', 'data': schedule_data}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_schedule_appointment(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录医生
    doctor = request.user

    # 查询医生的所有排班记录
    schedules = Schedule.objects.filter(doctor=doctor)

    # 创建字典存储结果
    schedule_appointment_dict = {}

    # 遍历排班记录，获取对应的预约信息
    for schedule in schedules:
        # 查询与当前排班相关的预约信息
        appointments = Appointment.objects.filter(schedule=schedule)

        # 构建预约信息的列表
        appointment_list = [
            {
                'appointment_id': appointment.appointment_id,
                'user_name': appointment.user.name,
                'relationship': appointment.relationship,
                'state': appointment.state
            }
            for appointment in appointments
        ]

        # 将排班时间和对应的预约信息添加到字典中
        schedule_time_str = schedule.schedule_time.strftime('%Y-%m-%d %H:%M:%S')
        schedule_appointment_dict[schedule_time_str] = appointment_list

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': schedule_appointment_dict}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_comments(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录医生
    doctor = request.user

    # 查询与当前医生相关的所有评价
    evaluations = Evaluation.objects.filter(doctor=doctor).order_by('-evaluation_time')

    # 构建返回数据
    comments = [
        {
            'evaluation_id': evaluation.evaluation_id,
            'evaluation': evaluation.evaluation,
            'evaluation_star': evaluation.evaluation_star,
            'evaluation_time': evaluation.evaluation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'user_name': evaluation.user.name if evaluation.user else None
        }
        for evaluation in evaluations
    ]

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': comments}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_patients_past(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录医生
    doctor = request.user

    # 查询该医生排班下的所有已完成预约
    appointments = Appointment.objects.filter(
        schedule__doctor=doctor,
        state='已完成'  # 筛选状态为 "已完成"
    ).select_related('user', 'schedule')

    # 构建返回数据
    patients = []
    for appointment in appointments:
        user = appointment.user
        patients.append({
            'appointment_id': appointment.appointment_id,
            'patient_name': user.name,
            'patient_gender': user.gender,
            'patient_birth': user.birth.strftime('%Y-%m-%d'),
            'patient_id_number': user.id_number,
            'schedule_time': appointment.schedule.schedule_time.strftime('%Y-%m-%d %H:%M:%S'),
            'relationship': appointment.relationship
        })

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': patients}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_patients_future(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录医生
    doctor = request.user

    # 查询该医生排班下的所有未完成预约
    appointments = Appointment.objects.filter(
        schedule__doctor=doctor,
        state='未完成'  # 筛选状态为 "未完成"
    ).select_related('user', 'schedule')

    # 构建返回数据
    patients = []
    for appointment in appointments:
        user = appointment.user
        patients.append({
            'appointment_id': appointment.appointment_id,
            'patient_name': user.name,
            'patient_gender': user.gender,
            'patient_birth': user.birth.strftime('%Y-%m-%d'),
            'patient_id_number': user.id_number,
            'schedule_time': appointment.schedule.schedule_time.strftime('%Y-%m-%d %H:%M:%S'),
            'relationship': appointment.relationship
        })

    # 返回 JSON 响应
    return JsonResponse({'status': 'success', 'data': patients}, safe=False)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def doctor_add_prescription(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 解析请求体
    data = json.loads(request.body)
    appointment_id = data.get('appointment_id')
    drug_id = data.get('drug_id')
    drug_amount = data.get('drug_amount')
    usage = data.get('usage')
    precautions = data.get('precautions')

    check_return = fields_check(Prescription, data, True)
    if check_return is not None:
        return check_return

    # 验证预约号是否存在，并获取对应诊断
    appointment = Appointment.objects.filter(appointment_id=appointment_id).select_related('schedule').first()
    if not appointment:
        return JsonResponse({'status': 'error', 'message': '预约号不存在'}, status=404)

    # 验证当前医生是否为该预约对应的医生
    if appointment.schedule.doctor != request.user:
        return JsonResponse({'status': 'error', 'message': '权限错误：该预约不属于当前医生'}, status=403)

    # 获取诊断记录
    diagnosis = Diagnosis.objects.filter(appointment=appointment).first()
    if not diagnosis:
        return JsonResponse({'status': 'error', 'message': '诊断记录不存在，请先填写诊断'}, status=404)

    # 获取药品记录
    drug = Drug.objects.filter(drug_id=drug_id).first()
    if not drug:
        return JsonResponse({'status': 'error', 'message': '药品不存在'}, status=404)

    # 创建处方记录
    prescription = Prescription.objects.create(
        prescription_id=Prescription.generate_incremental_prescription_id(),
        diagnosis=diagnosis,
        drug=drug,
        drug_amount=drug_amount,
        usage=usage,
        precautions=precautions
    )

    # 返回成功响应
    return JsonResponse({
        'status': 'success',
        'message': '处方添加成功',
        'prescription_id': prescription.prescription_id
    }, status=201)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_doctor_prescription(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前医生的所有已完成的预约记录
    completed_appointments = Appointment.objects.filter(
        schedule__doctor=request.user,
        state='已完成'
    ).select_related('schedule').prefetch_related(
        Prefetch(
            'diagnosis_set',
            queryset=Diagnosis.objects.prefetch_related('prescriptions'),
            to_attr='diagnoses_with_prescriptions'
        )
    )

    # 构建结果数据
    data = []
    for appointment in completed_appointments:
        appointment_data = {
            'appointment_id': appointment.appointment_id,
            'patient_name': appointment.user.name,
            'diagnoses': []
        }

        # 获取每个诊断及其对应的处方
        for diagnosis in getattr(appointment, 'diagnoses_with_prescriptions', []):
            diagnosis_data = {
                'diagnosis_id': diagnosis.diagnosis_id,
                'clinical_diagnosis': diagnosis.clinical_diagnosis,
                'prescriptions': []
            }

            # 添加处方信息
            for prescription in diagnosis.prescriptions.all():
                prescription_data = {
                    'prescription_id': prescription.prescription_id,
                    'drug_id': prescription.drug.drug_id,
                    'drug_name': prescription.drug.name,
                    'drug_amount': prescription.drug_amount,
                    'usage': prescription.usage,
                    'precautions': prescription.precautions
                }
                diagnosis_data['prescriptions'].append(prescription_data)

            appointment_data['diagnoses'].append(diagnosis_data)

        data.append(appointment_data)

    return JsonResponse({'status': 'success', 'data': data}, status=200)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_GET
def get_medicine_info(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 查询所有药品及其库存信息
    drugs = Drug.objects.all().select_related()

    # 构建结果数据
    data = []
    for drug in drugs:
        inventories = DrugInventory.objects.filter(drug_id=drug.drug_id).select_related('pharmacy')

        # 获取药品库存信息
        inventory_info = []
        for inventory in inventories:
            inventory_info.append({
                "pharmacy_id": inventory.pharmacy.pharmacy_id,
                "pharmacy_name": inventory.pharmacy.pharmacy_name,
                "drug_amount": inventory.drug_amount,
            })

        # 添加药品信息
        data.append({
            "drug_id": drug.drug_id,
            "drug_name": drug.drug_name,
            "price": drug.price,
            "inventories": inventory_info,
        })

    return JsonResponse({'status': 'success', 'data': data}, status=200)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def set_doctor_schedule_appointment_done(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 获取当前登录医生
    doctor = request.user

    # 解析请求体数据
    data = json.loads(request.body)
    appointment_id = data.get('appointment_id')
    if not appointment_id:
        return JsonResponse({'status': 'error', 'message': '预约号不能为空'}, status=400)

    # 查询预约信息并校验关联的排班是否属于当前医生
    appointment = Appointment.objects.select_related('schedule__doctor').filter(
        appointment_id=appointment_id).first()
    if not appointment:
        return JsonResponse({'status': 'error', 'message': '预约不存在'}, status=404)

    if appointment.schedule.doctor != doctor:
        return JsonResponse({'status': 'error', 'message': '该预约不属于当前医师'}, status=403)

    # 更新预约状态为已完成
    appointment.state = '已完成'
    appointment.save()

    return JsonResponse({'status': 'success', 'message': '预约状态已更新为已完成'}, status=200)


@csrf_exempt  # 临时禁用 CSRF 检查
@require_POST
def doctor_prescribe(request):
    # 确保当前用户已登录，并且用户为医师
    if not is_doctor(request.user):
        return JsonResponse({'status': 'error', 'message': '权限错误'}, status=403)

    # 解析请求体
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

    prescription_id = data.get('prescription_id')
    if not prescription_id:
        return JsonResponse({'status': 'error', 'message': '处方号不能为空'}, status=400)

    try:
        # 获取处方记录
        prescription = Prescription.objects.select_related('diagnosis', 'drug').get(prescription_id=prescription_id)
    except Prescription.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '处方不存在'}, status=404)

    # 验证处方是否属于当前医生
    diagnosis = prescription.diagnosis
    if not diagnosis or diagnosis.doctor != request.user:
        return JsonResponse({'status': 'error', 'message': '权限错误：此处方不属于当前医生'}, status=403)

    # 获取药品库存信息
    drug_inventory = DrugInventory.objects.filter(drug_id=prescription.drug.drug_id).first()
    if not drug_inventory:
        return JsonResponse({'status': 'error', 'message': '药品库存不存在'}, status=404)

    # 检查库存是否足够
    if drug_inventory.drug_amount < prescription.drug_amount:
        return JsonResponse({'status': 'error', 'message': '药品库存不足'}, status=400)

    # 扣减库存
    drug_inventory.drug_amount -= prescription.drug_amount
    drug_inventory.save()

    # 创建支付项目
    payment = Payment.objects.create(
        payment_id=Payment.generate_incremental_payment_id(),
        payment_name=f"处方支付 - {prescription.drug.drug_name}",
        payment_description=f"处方 {prescription_id} 对应药品 {prescription.drug.drug_name} 的费用",
        money=prescription.drug.price * prescription.drug_amount,
        user=diagnosis.appointment.user,
        is_paid=False
    )

    # 返回成功响应
    return JsonResponse({
        'status': 'success',
        'message': '药品已成功开具',
        'payment_id': payment.payment_id,
        'payment_amount': payment.money
    }, status=201)


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


@csrf_exempt  # 临时禁用 CSRF 检查
def get_image_url(request):
    image_id = request.GET.get('image')
    image = Image.objects.filter(image_id=image_id).first(
    )
    return JsonResponse({'status': 'success', 'data': request.build_absolute_uri(image.image.url)}, safe=False)
