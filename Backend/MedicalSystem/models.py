from django.db import models


# 表 1: 用户数据元素表
class User(models.Model):
    id = models.CharField(max_length=8, primary_key=True)  # 学工号：主键
    password = models.CharField(max_length=25, null=False, blank=False)  # 密码：非空
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 身份证号：非空
    user_type = models.CharField(max_length=1, null=False, blank=False)  # 用户类型：非空
    phone = models.CharField(max_length=11, null=False, blank=False)  # 手机号：非空


# 表 2: 医师用户数据元素表
class Doctor(models.Model):
    staff_id = models.CharField(max_length=5, primary_key=True)  # 医工号：主键
    password = models.CharField(max_length=25, null=False, blank=False)  # 密码：非空
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    title = models.CharField(max_length=10, null=False, blank=False)  # 职称：非空
    image_id = models.CharField(max_length=10, null=True, blank=True)  # 图片号：可空
    introduction = models.TextField(null=False, blank=False)  # 介绍：非空


# 表 3: 管理员数据元素表
class Admin(models.Model):
    admin_id = models.CharField(max_length=3, primary_key=True)  # 管理员号：主键
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    password = models.CharField(max_length=25, null=False, blank=False)  # 密码：非空


# 表 4: 家属数据元素表
class FamilyMember(models.Model):
    family_id = models.CharField(max_length=2)  # 家属号：主键
    teacher_id = models.CharField(max_length=8)  # 学工号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 关系：非空
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 身份证号：非空

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['family_id', 'teacher_id'], name='unique_family_teacher')
        ]


# 表 5: 科室数据元素表
class Department(models.Model):
    department_id = models.CharField(max_length=3, primary_key=True)  # 科室号：主键
    department_name = models.CharField(max_length=10, null=False, blank=False)  # 科室名称：非空


# 表 6: 排班数据元素表
class Schedule(models.Model):
    schedule_id = models.CharField(max_length=8, primary_key=True)  # 排班号：主键
    staff_id = models.CharField(max_length=5, null=False, blank=False)  # 医工号：非空
    department_id = models.CharField(max_length=3, null=False, blank=False)  # 科室号：非空
    schedule_time = models.DateTimeField(null=False, blank=False)  # 排班时间：非空


# 表 7: 药房数据元素表
class Pharmacy(models.Model):
    pharmacy_id = models.CharField(max_length=2, primary_key=True)  # 药房号：主键
    pharmacy_name = models.CharField(max_length=10, null=False, blank=False)  # 药房名称：非空


# 表 8: 药品数据元素表
class Drug(models.Model):
    drug_id = models.CharField(max_length=9, primary_key=True)  # 药品号：主键
    drug_name = models.CharField(max_length=20, null=False, blank=False)  # 药品名称：非空
    price = models.FloatField(null=False, blank=False)  # 药品价格：非空


# 表 9: 药品库存数据元素表
class DrugInventory(models.Model):
    drug_id = models.CharField(max_length=9)  # 药品号：主键
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    pharmacy_id = models.CharField(max_length=2)  # 药房号：主键

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['drug_id', 'pharmacy_id'], name='unique_drug_pharmacy')
        ]


# 表 10: 体检安排元素表
class ExaminationArrangement(models.Model):
    examination_id = models.CharField(max_length=8, primary_key=True)  # 体检号：主键
    examination_text = models.TextField(null=False, blank=False)  # 体检项目：非空
    examination_date = models.DateField(null=False, blank=False)  # 体检日期：非空
    staff_id = models.CharField(max_length=5, null=False, blank=False)  # 负责医工号：非空


# 表 11: 体检信息数据元素表
class ExaminationInfo(models.Model):
    exam_appointment_id = models.CharField(max_length=8, primary_key=True)  # 体检预约号：主键
    examination_id = models.CharField(max_length=8, null=False, blank=False)  # 体检号：非空
    examination_result = models.TextField(null=True, blank=True)  # 体检结果：可空
    student_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空


# 表 12: 预约数据元素表
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, primary_key=True)  # 预约号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 患者与预约人关系：非空
    schedule_id = models.CharField(max_length=8, null=False, blank=False)  # 排班号：非空
    student_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空


# 表 13: 诊断数据元素表
class Diagnosis(models.Model):
    diagnosis_id = models.CharField(max_length=8, primary_key=True)  # 诊断号：主键
    examination = models.TextField(null=False, blank=False)  # 检查项目：非空
    examination_result = models.TextField(null=False, blank=False)  # 检查结果：非空
    reference_range = models.TextField(null=False, blank=False)  # 参考范围：非空
    clinical_diagnosis = models.TextField(null=False, blank=False)  # 临床诊断：非空
    prescription_id = models.CharField(max_length=8, null=False, blank=False)  # 处方号：非空
    diagnosis_time = models.DateTimeField(null=False, blank=False)  # 诊断时间：非空
    patient_id_number = models.CharField(max_length=18, null=False, blank=False)  # 患者身份证号：非空
    appointment_id = models.CharField(max_length=8, null=False, blank=False)  # 预约号：非空
    staff_id = models.CharField(max_length=5, null=False, blank=False)  # 医工号：非空


# 表 14: 处方数据元素表
class Prescription(models.Model):
    prescription_id = models.CharField(max_length=8, primary_key=True)  # 处方号：主键
    diagnosis_id = models.CharField(max_length=8, null=False, blank=False)  # 诊断号：非空
    drug_id = models.CharField(max_length=9, null=False, blank=False)  # 药品号：非空
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    usage = models.TextField(null=False, blank=False)  # 用法用量：非空
    precautions = models.TextField(null=False, blank=False)  # 注意事项：非空


# 表 15: 通知数据元素表
class Notification(models.Model):
    notification_id = models.CharField(max_length=8, primary_key=True)  # 通知号：主键
    notification_text = models.TextField(null=False, blank=False)  # 通知内容：非空
    notification_time = models.DateTimeField(null=False, blank=False)  # 通知时间：非空
    recipient_student_id = models.CharField(max_length=8, null=False, blank=False)  # 接收人学工号：非空


# 表 16: 评价数据元素表
class Evaluation(models.Model):
    evaluation_id = models.CharField(max_length=8, primary_key=True)  # 评价号：主键
    evaluation_text = models.TextField(null=False, blank=False)  # 评价内容：非空
    evaluation_time = models.DateTimeField(null=False, blank=False)  # 评价时间：非空
    evaluator_student_id = models.CharField(max_length=8, null=False, blank=False)  # 评价人学工号：非空
    evaluated_staff_id = models.CharField(max_length=5, null=False, blank=False)  # 被评价人医工号：非空


# 表 17: 图片数据元素表
class Image(models.Model):
    image_id = models.CharField(max_length=10, primary_key=True)  # 图片号：主键
    image_path = models.CharField(max_length=255, null=False, blank=False)  # 存储路径：非空
    evaluation_id = models.CharField(max_length=8, null=True, blank=True)  # 评价号：可空
    notification_id = models.CharField(max_length=8, null=True, blank=True)  # 通知号：可空
    drug_id = models.CharField(max_length=9, null=True, blank=True)  # 药品号：可空
