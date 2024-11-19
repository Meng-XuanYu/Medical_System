from MedicalSystem.models import Schedule
from collections import defaultdict


def get_schedules_by_department(department):
    # 查询指定科室的排班数据，并预取关联的 Doctor 信息
    schedules = Schedule.objects.filter(department=department).select_related('doctor')

    # 使用字典整合排班信息，以 doctor 为分类依据
    schedule_dict = defaultdict(dict)
    for schedule in schedules:
        doctor = schedule.doctor
        # 将排班号作为键，排班时间作为值
        schedule_dict[doctor.doctor_id][schedule.schedule_id] = schedule.schedule_time

    # 构建最终的数据结构，包含医生的详细信息
    result = [
        {
            'name': doctor.name,
            'gender': doctor.gender,
            'title': doctor.title,
            'image_id': doctor.image_id,
            'schedule_times': schedule_dict[doctor_id]  # schedule_id: schedule_time 的字典
        }
        for doctor_id, doctor_schedules in schedule_dict.items()
        for schedule in schedules if schedule.doctor.doctor_id == doctor_id
    ]

    return result
