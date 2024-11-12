from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


# 用户抽象类
class BaseUser(AbstractBaseUser, PermissionsMixin):
    # 公共字段
    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)

    class Meta:
        abstract = True  # 设置为抽象类，防止创建数据表


class UserManager(BaseUserManager):
    def create_base_user(self, base_user_type, id, password=None, **extra_fields):
        if not id:
            raise ValueError("必须提供用户ID")

        match base_user_type:
            case "user":
                user = self.model(id=id, **extra_fields)
            case "doctor":
                user = self.model(doctor_id=id, **extra_fields)
            case "admin":
                user = self.model(admin_id=id, **extra_fields)
            case _:
                raise ValueError("不存在的基础用户类型：" + base_user_type)

        # 设置用户密码
        user.set_password(password)  # 对密码进行哈希处理
        user.save(using=self._db)
        return user

    def create_base_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        extra_fields.setdefault('is_superuser', True)

        # 验证超级用户必须有权限
        if extra_fields.get('is_doctor') is not True:
            raise ValueError("超级用户必须设置 is_doctor=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("超级用户必须设置 is_superuser=True")

        return self.create_base_user(id, password, **extra_fields)


# 表 1: 用户数据元素表
class User(BaseUser):
    id = models.CharField(max_length=8, primary_key=True, unique=True)  # 学工号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 身份证号：非空
    user_type = models.CharField(max_length=1, null=False, blank=False)  # 用户类型：非空
    phone = models.CharField(max_length=11, null=False, blank=False)  # 手机号：非空

    # 用户权限设置
    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions")

    # 指定用户ID作为登录字段
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'gender', 'birth', 'id_number', 'user_type', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.id

    @classmethod
    def get_required_fields(cls, use_password):
        if use_password:
            return {
                'id': 8,
                'password': 128,
                'name': 15,
                'gender': 1,
                'birth': None,  # 日期字段无需长度限制
                'id_number': 18,
                'user_type': 1,
                'phone': 11
            }
        else:
            return {
                'id': 8,
                'name': 15,
                'gender': 1,
                'birth': None,  # 日期字段无需长度限制
                'id_number': 18,
                'user_type': 1,
                'phone': 11
            }

    @classmethod
    def get_optional_fields(cls):
        return {}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth': self.birth,
            'id_number': self.id_number,
            'user_type': self.user_type,
            'phone': self.phone
        }


# 表 2: 医师用户数据元素表
class Doctor(BaseUser):
    doctor_id = models.CharField(max_length=5, primary_key=True, unique=True)  # 医工号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    title = models.CharField(max_length=10, null=False, blank=False)  # 职称：非空
    image_id = models.CharField(max_length=10, null=True, blank=True)  # 图片号：可空
    introduction = models.TextField(null=False, blank=False)  # 介绍：可空

    # 医师权限设置
    groups = models.ManyToManyField(Group, related_name="doctor_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="doctor_permissions")

    # 使医生的用户名字段指向 doctor_id
    USERNAME_FIELD = 'doctor_id'
    REQUIRED_FIELDS = ['name', 'gender', 'title']

    objects = UserManager()

    def __str__(self):
        return self.id

    @classmethod
    def get_required_fields(cls, use_password):
        if use_password:
            return {
                'doctor_id': 5,
                'password': 128,
                'name': 15,
                'gender': 1,
                'title': 10
            }
        else:
            return {
                'doctor_id': 5,
                'name': 15,
                'gender': 1,
                'title': 10
            }

    @classmethod
    def get_optional_fields(cls):
        return {
            'image_id': 10,  # 图片号为可选字段
            'introduction': None  # 介绍为 TextField，无固定长度
        }

    def get_view_dic(self):
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'gender': self.gender,
            'title': self.title,
            'image_id': self.image_id,
            'introduction': self.introduction
        }


# 表 3: 管理员数据元素表
class Admin(BaseUser):
    admin_id = models.CharField(max_length=3, primary_key=True, unique=True)  # 管理员号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空

    # 管理员权限设置
    groups = models.ManyToManyField(Group, related_name="admin_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="admin_permissions")

    # 设置管理员登录字段为 admin_id
    USERNAME_FIELD = 'admin_id'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.id

    @classmethod
    def get_required_fields(cls, use_password):
        if use_password:
            return {
                'admin_id': 3,
                'password': 128,
                'name': 15
            }
        else:
            return {
                'admin_id': 3,
                'name': 15
            }

    @classmethod
    def get_optional_fields(cls):
        return {}

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'name': self.name
        }


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
    department_id = models.CharField(max_length=3, primary_key=True, unique=True)  # 科室号：主键
    department_name = models.CharField(max_length=10, null=False, blank=False)  # 科室名称：非空


# 表 6: 排班数据元素表
class Schedule(models.Model):
    schedule_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 排班号：主键
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 医工号：非空
    department_id = models.CharField(max_length=3, null=False, blank=False)  # 科室号：非空
    schedule_time = models.DateTimeField(null=False, blank=False)  # 排班时间：非空


# 表 7: 药房数据元素表
class Pharmacy(models.Model):
    pharmacy_id = models.CharField(max_length=2, primary_key=True, unique=True)  # 药房号：主键
    pharmacy_name = models.CharField(max_length=10, null=False, blank=False)  # 药房名称：非空


# 表 8: 药品数据元素表
class Drug(models.Model):
    drug_id = models.CharField(max_length=9, primary_key=True, unique=True)  # 药品号：主键
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
    examination_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 体检号：主键
    examination_text = models.TextField(null=False, blank=False)  # 体检项目：非空
    examination_date = models.DateField(null=False, blank=False)  # 体检日期：非空
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 负责医工号：非空


# 表 11: 体检信息数据元素表
class ExaminationInfo(models.Model):
    exam_appointment_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 体检预约号：主键
    examination_id = models.CharField(max_length=8, null=False, blank=False)  # 体检号：非空
    examination_result = models.TextField(null=True, blank=True)  # 体检结果：可空
    student_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空


# 表 12: 预约数据元素表
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 预约号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 患者与预约人关系：非空
    schedule_id = models.CharField(max_length=8, null=False, blank=False)  # 排班号：非空
    student_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空


# 表 13: 诊断数据元素表
class Diagnosis(models.Model):
    diagnosis_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 诊断号：主键
    examination = models.TextField(null=False, blank=False)  # 检查项目：非空
    examination_result = models.TextField(null=False, blank=False)  # 检查结果：非空
    reference_range = models.TextField(null=False, blank=False)  # 参考范围：非空
    clinical_diagnosis = models.TextField(null=False, blank=False)  # 临床诊断：非空
    prescription_id = models.CharField(max_length=8, null=False, blank=False)  # 处方号：非空
    diagnosis_time = models.DateTimeField(null=False, blank=False)  # 诊断时间：非空
    patient_id_number = models.CharField(max_length=18, null=False, blank=False)  # 患者身份证号：非空
    appointment_id = models.CharField(max_length=8, null=False, blank=False)  # 预约号：非空
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 医工号：非空


# 表 14: 处方数据元素表
class Prescription(models.Model):
    prescription_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 处方号：主键
    diagnosis_id = models.CharField(max_length=8, null=False, blank=False)  # 诊断号：非空
    drug_id = models.CharField(max_length=9, null=False, blank=False)  # 药品号：非空
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    usage = models.TextField(null=False, blank=False)  # 用法用量：非空
    precautions = models.TextField(null=False, blank=False)  # 注意事项：非空


# 表 15: 通知数据元素表
class Notification(models.Model):
    notification_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 通知号：主键
    notification_text = models.TextField(null=False, blank=False)  # 通知内容：非空
    notification_time = models.DateTimeField(null=False, blank=False)  # 通知时间：非空
    recipient_student_id = models.CharField(max_length=8, null=False, blank=False)  # 接收人学工号：非空


# 表 16: 评价数据元素表
class Evaluation(models.Model):
    evaluation_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 评价号：主键
    evaluation_text = models.TextField(null=False, blank=False)  # 评价内容：非空
    evaluation_time = models.DateTimeField(null=False, blank=False)  # 评价时间：非空
    evaluator_student_id = models.CharField(max_length=8, null=False, blank=False)  # 评价人学工号：非空
    evaluated_doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 被评价人医工号：非空


# 表 17: 图片数据元素表
class Image(models.Model):
    image_id = models.CharField(max_length=10, primary_key=True, unique=True)  # 图片号：主键
    image_path = models.CharField(max_length=255, null=False, blank=False)  # 存储路径：非空
    evaluation_id = models.CharField(max_length=8, null=True, blank=True)  # 评价号：可空
    notification_id = models.CharField(max_length=8, null=True, blank=True)  # 通知号：可空
    drug_id = models.CharField(max_length=9, null=True, blank=True)  # 药品号：可空
