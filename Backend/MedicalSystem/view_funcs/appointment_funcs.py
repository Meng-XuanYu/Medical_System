from MedicalSystem.models import Schedule
from collections import defaultdict


def get_schedules_by_department(department):
    # 查询指定科室的排班数据，并预取关联的 Doctor 信息
    schedules = Schedule.objects.filter(department=department).select_related('doctor')

    # 使用字典整合排班信息，以 doctor 为分类依据
    schedule_dict = defaultdict(dict)
    doctor_info = {}

    for schedule in schedules:
        doctor = schedule.doctor
        doctor_id = doctor.doctor_id

        # 将排班时间添加到对应医生的排班列表中
        schedule_dict[doctor_id][schedule.schedule_id] = schedule.schedule_time

        # 保存医生的详细信息
        if doctor_id not in doctor_info:
            doctor_info[doctor_id] = {
                'name': doctor.name,
                'gender': doctor.gender,
                'title': doctor.title,
                'image_id': doctor.image_id,
                'introduction': doctor.introduction
            }

    # 构建最终的数据结构，包含医生的详细信息和排班时间
    result = [
        {
            'doctor_id': doctor_id,
            'name': info['name'],
            'gender': info['gender'],
            'title': info['title'],
            'image_id': info['image_id'],
            'introduction': info['introduction'],
            'schedule_times': schedule_dict[doctor_id]  # 包含 schedule_id 和 schedule_time 的字典
        }
        for doctor_id, info in doctor_info.items()
    ]

    return result
