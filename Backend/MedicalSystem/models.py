from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


# 用户抽象类
class BaseUser(AbstractBaseUser, PermissionsMixin):
    # 公共字段
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        abstract = True  # 设置为抽象类，防止创建数据表


class UserManager(BaseUserManager):
    def create_base_user(self, base_user_type, id, password=None, **extra_fields):
        if not id:
            raise ValueError("必须提供用户ID")

        match base_user_type:
            case "user":
                user = self.model(user_id=id, **extra_fields)
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

    def create_superuser(self, base_user_type, id, password=None, **extra_fields):
        if not id:
            raise ValueError("必须提供用户ID")
        elif base_user_type != "admin":
            raise ValueError("超级用户必须为管理员")

        # 确保超级用户具备必要的权限
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # 验证超级用户必须有权限
        if extra_fields.get('is_staff') is not True:
            raise ValueError("超级用户必须设置 is_admin=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("超级用户必须设置 is_superuser=True")

        return self.create_base_user(base_user_type, id, password, **extra_fields, )


# 表 1: 用户数据元素表
class User(BaseUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, db_index=True)  # 学工号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False, db_index=True)  # 身份证号：非空
    user_type = models.CharField(max_length=1, null=False, blank=False)  # 用户类型：非空
    phone = models.CharField(max_length=11, null=False, blank=False)  # 手机号：非空
    image = models.ForeignKey('Image', on_delete=models.CASCADE, to_field='image_id', null=True, blank=True)
    # 用户权限设置
    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions")

    # 指定用户ID作为登录字段
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'gender', 'birth', 'id_number', 'user_type', 'phone']

    objects = UserManager()

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'user_id': 8,
            'password': 128,
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

    @classmethod
    def get_chinese_name(cls):
        return '用户'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 2: 医师用户数据元素表
class Doctor(BaseUser):
    doctor_id = models.CharField(max_length=5, primary_key=True, unique=True, db_index=True)  # 医工号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    title = models.CharField(max_length=10, null=False, blank=False)  # 职称：非空
    image = models.ForeignKey('Image', on_delete=models.CASCADE, to_field='image_id', null=True, blank=True)
    introduction = models.TextField(null=False, blank=False)  # 介绍：可空

    # 医师权限设置
    groups = models.ManyToManyField(Group, related_name="doctor_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="doctor_permissions")

    # 使医生的用户名字段指向 doctor_id
    USERNAME_FIELD = 'doctor_id'
    REQUIRED_FIELDS = ['name', 'gender', 'title']

    objects = UserManager()

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'doctor_id': 5,
            'password': 128,
            'name': 15,
            'gender': 1,
            'title': 10,
            'image': None,  # 图片字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {
            'image_id': 10,
            'introduction': None  # text字段无需长度限制
        }

    @classmethod
    def get_chinese_name(cls):
        return '医师'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 3: 管理员数据元素表
class Admin(BaseUser):
    admin_id = models.CharField(max_length=3, primary_key=True, unique=True, db_index=True)  # 管理员号：主键
    password = models.CharField(max_length=128, null=False, blank=False)  # 密码：非空，128个字符用于加密后的存储
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空

    # 管理员权限设置
    groups = models.ManyToManyField(Group, related_name="admin_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="admin_permissions")

    # 设置管理员登录字段为 admin_id
    USERNAME_FIELD = 'admin_id'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'admin_id': 3,
            'password': 128,
            'name': 15
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '管理员'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 4: 家属数据元素表
class FamilyMember(models.Model):
    family_id = models.CharField(max_length=2, null=False, blank=False)  # 家属号：主键
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 关系：非空
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False, db_index=True)  # 身份证号：非空

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['family_id', 'user'], name='unique_family_teacher'),
        ]
        indexes = [
            models.Index(fields=['family_id', 'user']),  # 家属号 + 用户复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'relationship': 10,
            'name': 15,
            'gender': 1,
            'birth': None,  # 日期字段无需长度限制
            'id_number': 18
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def allowed_update_fields(cls):
        return ['relationship', 'name', 'gender', 'birth', 'id_number']

    @classmethod
    def get_chinese_name(cls):
        return '家属'

    # 生成唯一的递增家属号，从 1 开始。如果已存在，则跳到下一个可用的数字
    @classmethod
    def generate_incremental_family_id(cls):
        # 获取现有的最大 family_id
        last_family_member = cls.objects.order_by('-family_id').first()
        if last_family_member and last_family_member.family_id.isdigit():
            next_id = int(last_family_member.family_id) + 1
        else:
            next_id = 1
        return str(next_id).zfill(2)  # 补齐 2 位

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 5: 科室数据元素表
class Department(models.Model):
    department_id = models.CharField(max_length=3, primary_key=True, unique=True, db_index=True)  # 科室号：主键
    department_name = models.CharField(max_length=10, null=False, blank=False)  # 科室名称：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'department_id': 3,
            'department_name': 10
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '科室'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 6: 排班数据元素表
class Schedule(models.Model):
    schedule_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 排班号：主键
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, to_field='doctor_id', null=True,
                               db_index=True)  # 外键引用 Doctor
    department = models.ForeignKey('Department', on_delete=models.CASCADE, to_field='department_id', null=True,
                                   db_index=True)  # 外键引用 Department
    schedule_time = models.CharField(max_length=50, null=False, blank=False)  # 排班时间：非空

    class Meta:
        indexes = [
            models.Index(fields=['doctor', 'department']),  # 医生 + 科室复合索引
            models.Index(fields=['doctor', 'schedule_time']),  # 医生 + 排班时间复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'schedule_id': 8,
            'doctor_id': 5,
            'department_id': 3,
            'schedule_time': None,  # 时间字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '排班'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 7: 药房数据元素表
class Pharmacy(models.Model):
    pharmacy_id = models.CharField(max_length=2, primary_key=True, unique=True)  # 药房号：主键
    pharmacy_name = models.CharField(max_length=10, null=False, blank=False)  # 药房名称：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'pharmacy_id': 2,
            'pharmacy_name': 10
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '药房'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 8: 药品数据元素表
class Drug(models.Model):
    drug_id = models.CharField(max_length=9, primary_key=True, unique=True)  # 药品号：主键
    drug_name = models.CharField(max_length=20, null=False, blank=False)  # 药品名称：非空
    image = models.ForeignKey('Image', on_delete=models.CASCADE, to_field='image_id', null=True, blank=True)
    price = models.FloatField(null=False, blank=False)  # 药品价格：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'drug_id': 9,
            'drug_name': 20,
            'image': None,  # 图片字段无需长度限制
            'price': None,  # 浮点数字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '药品'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 9: 药品库存数据元素表
class DrugInventory(models.Model):
    drug_id = models.CharField(max_length=9)  # 药品号：主键
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE, to_field='pharmacy_id', null=True,
                                 db_index=True)  # 外键引用 Pharmacy

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['drug_id', 'pharmacy'], name='unique_drug_pharmacy'),
        ]
        indexes = [
            models.Index(fields=['drug_id', 'pharmacy']),  # 药品号 + 药房复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'drug_id': 9,
            'drug_amount': None,  # 整数字段无需长度限制
            'pharmacy_id': 2
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '药品库存'

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 10: 体检安排元素表
class ExaminationArrangement(models.Model):
    examination_id = models.CharField(max_length=8, primary_key=True, unique=True, db_index=True)  # 体检号：主键
    examination = models.TextField(null=False, blank=False)  # 体检项目：非空
    examination_date = models.DateField(null=False, blank=False)  # 体检日期：非空
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, to_field='doctor_id', null=True,
                               db_index=True)  # 外键引用 Doctor

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'examination_id': 8,
            'examination': None,  # text字段无需长度限制
            'examination_date': None,  # 日期字段无需长度限制
            'doctor_id': 5
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '体检安排'

    @classmethod
    def prepare_data(cls, data):
        data['doctor'] = Doctor.objects.get(doctor_id=data['doctor_id'])
        return data


# 表 11: 体检信息数据元素表
class ExaminationInfo(models.Model):
    exam_appointment_id = models.CharField(max_length=8, primary_key=True, unique=True, db_index=True)  # 体检预约号：主键
    examination_arrangement = models.ForeignKey('ExaminationArrangement', on_delete=models.CASCADE,
                                                to_field='examination_id', null=True, blank=False,
                                                db_index=True)  # 外键引用 ExaminationArrangement
    examination_result = models.TextField(null=True, blank=True)  # 体检结果：可空
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User
    state = models.CharField(max_length=8, null=True, blank=False)  # 体检状态：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'exam_appointment_id': 8,
            'examination_id': 8,
            'user_id': 8,
            'state': 8
        }

    @classmethod
    def get_optional_fields(cls):
        return {
            'examination_result': None  # text字段无需长度限制
        }

    @classmethod
    def get_chinese_name(cls):
        return '体检信息'

    # 生成唯一的递增体检预约号，从 1 开始。如果已存在，则跳到下一个可用的数字
    @classmethod
    def generate_incremental_exam_appointment_id(cls):
        # 获取现有的最大 appointment_id
        last_exam_appointment = cls.objects.order_by('-exam_appointment_id').first()
        if last_exam_appointment and last_exam_appointment.exam_appointment_id.isdigit():
            next_id = int(last_exam_appointment.exam_appointment_id) + 1
        else:
            next_id = 1
        return str(next_id).zfill(8)  # 补齐 8 位

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 12: 预约数据元素表
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, primary_key=True, unique=True, db_index=True)  # 预约号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 患者与预约人关系：非空
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, to_field='schedule_id', null=True, blank=False,
                                 db_index=True)  # 外键引用 Schedule
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User
    state = models.CharField(max_length=8, null=True, blank=False, db_index=True)  # 预约状态：非空

    class Meta:
        indexes = [
            models.Index(fields=['relationship', 'user']),  # 关系 + 用户复合索引
            models.Index(fields=['schedule', 'state']),  # 排班 + 状态复合索引
            models.Index(fields=['user', 'state']),  # 用户 + 状态复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'appointment_id': 8,
            'relationship': 10,
            'schedule_id': 8,
            'user_id': 8
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '预约'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        if 'user_id' in data:
            user_id = data.pop('user_id')
            try:
                user = User.objects.get(user_id=user_id)
                data['user'] = user  # 将 user_id 转为 user 对象
            except User.DoesNotExist:
                raise ValueError(f"Doctor with id {user_id} does not exist")
        if 'schedule_id' in data:
            schedule_id = data.pop('schedule_id')
            try:
                schedule = Schedule.objects.get(schedule_id=schedule_id)
                data['schedule'] = schedule
                # 将 schedule_id 转为 schedule 对象
            except Schedule.DoesNotExist:
                raise ValueError(f"Doctor with id {schedule_id} does not exist")
        return data

    # 生成唯一的递增预约号，从 1 开始。如果已存在，则跳到下一个可用的数字
    @classmethod
    def generate_incremental_appointment_id(cls):
        # 获取现有的最大 appointment_id
        last_appointment = cls.objects.order_by('-appointment_id').first()
        if last_appointment and last_appointment.appointment_id.isdigit():
            next_id = int(last_appointment.appointment_id) + 1
        else:
            next_id = 1
        return str(next_id).zfill(8)  # 补齐 8 位

    @classmethod
    def prepare_data(cls, data):
        return data


# 表 13: 诊断数据元素表
class Diagnosis(models.Model):
    diagnosis_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 诊断号：主键
    examination = models.TextField(null=False, blank=False)  # 检查项目：非空
    examination_result = models.TextField(null=False, blank=False)  # 检查结果：非空
    reference = models.TextField(null=False, blank=False)  # 参考范围：非空
    clinical_diagnosis = models.TextField(null=False, blank=False)  # 临床诊断：非空
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, to_field='prescription_id', null=True,
                                     db_index=True, related_name='diagnoses')  # 外键引用 Prescription
    diagnosis_time = models.DateTimeField(null=False, blank=False)  # 诊断时间：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 患者身份证号：非空
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, to_field='appointment_id', null=True,
                                    db_index=True)  # 外键引用 Appointment
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, to_field='doctor_id', null=True,
                               db_index=True)  # 外键引用 Doctor

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'diagnosis_id': 8,
            'examination': None,  # text字段无需长度限制
            'examination_result': None,  # text字段无需长度限制
            'reference': None,  # text字段无需长度限制
            'clinical_diagnosis': None,  # text字段无需长度限制
            'prescription_id': 8,
            'diagnosis_time': None,  # 时间字段无需长度限制
            'id_number': 18,
            'appointment_id': 8,
            'doctor_id': 5
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '诊断'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data


# 表 14: 处方数据元素表
class Prescription(models.Model):
    prescription_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 处方号：主键
    diagnosis = models.ForeignKey('Diagnosis', on_delete=models.CASCADE, to_field='diagnosis_id', null=True,
                                  db_index=True, related_name='prescriptions')  # 外键引用 Diagnosis
    drug = models.ForeignKey('Drug', on_delete=models.CASCADE, to_field='drug_id', null=True,
                             db_index=True)  # 外键引用 Drug
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    usage = models.TextField(null=False, blank=False)  # 用法用量：非空
    precautions = models.TextField(null=False, blank=False)  # 注意事项：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'prescription_id': 8,
            'diagnosis_id': 8,
            'drug_id': 9,
            'drug_amount': None,  # 整数字段无需长度限制
            'usage': None,  # text字段无需长度限制
            'precautions': None  # text字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '处方'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    # 生成唯一的递增处方号，从 1 开始。如果已存在，则跳到下一个可用的数字
    @classmethod
    def generate_incremental_prescription_id(cls):
        # 获取现有的最大 prescription_id
        last_prescription = cls.objects.order_by('-prescription_id').first()
        if last_prescription and last_prescription.prescription_id.isdigit():
            next_id = int(last_prescription.prescription_id) + 1
        else:
            next_id = 1
        return str(next_id).zfill(8)  # 补齐 8 位


# 表 15: 通知数据元素表
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, unique=True)  # 通知号：主键
    notification = models.TextField(null=False, blank=False)  # 通知内容：非空
    notification_time = models.DateTimeField(null=False, blank=False)  # 通知时间：非空
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'notification_id': 8,
            'notification_text': None,  # text字段无需长度限制
            'notification_time': None,  # 时间字段无需长度限制
            'user_id': 8
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '通知'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data


# 表 16: 评价数据元素表
class Evaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True, unique=True)  # 评价号：主键
    evaluation = models.TextField(null=False, blank=False)  # 评价内容：非空
    evaluation_star = models.IntegerField(null=False, blank=False)  # 评价星级：非空
    evaluation_time = models.DateTimeField(null=False, blank=False)  # 评价时间：非空
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, to_field='doctor_id', null=True,
                               db_index=True)  # 外键引用 Doctor

    class Meta:
        indexes = [
            models.Index(fields=['doctor', 'evaluation_time']),  # 医师 + 评价时间复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'evaluation_id': 8,
            'evaluation': None,  # text字段无需长度限制
            'evaluation_star': None,  # 整数字段无需长度限制
            'evaluation_time': None,  # 时间字段无需长度限制
            'user_id': 8,
            'doctor_id': 5
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '评价'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data


# 表 17: 支付项目数据元素表
class Payment(models.Model):
    payment_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 支付项目：主键
    payment_name = models.CharField(max_length=20, null=False, blank=False)  # 支付项目名：非空
    payment_description = models.TextField(null=False, blank=False)  # 支付项目描述：非空
    money = models.FloatField(null=False, blank=False)  # 支付金额：非空
    user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='user_id', null=True, blank=False,
                             db_index=True)  # 外键引用 User
    is_paid = models.BooleanField(null=False, blank=False)  # 是否已支付：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'payment_id': 8,
            'payment_name': 20,
            'payment_description': None,  # 文本字段无需长度限制
            'money': None,  # 浮点数字段无需长度限制
            'user_id': 8,
            'is_paid': None,  # 布尔字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '支付项目'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    # 生成唯一的递增支付项目号，从 1 开始。如果已存在，则跳到下一个可用的数字
    @classmethod
    def generate_incremental_payment_id(cls):
        # 获取现有的最大 payment_id
        last_payment = cls.objects.order_by('-payment_id').first()
        if last_payment and last_payment.payment_id.isdigit():
            next_id = int(last_payment.payment_id) + 1
        else:
            next_id = 1
        return str(next_id).zfill(8)  # 补齐 8 位


# 表 18: 图片数据元素表
class Image(models.Model):
    image_id = models.AutoField(primary_key=True, unique=True)  # 图片号：主键
    image = models.ImageField(upload_to='images/', null=False, blank=False)  # 图片：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_primary_key_field(cls):
        return cls._meta.pk.name

    @classmethod
    def get_required_fields(cls):
        return {
            'image_id': 10,
            'image': None  # 图片字段无需长度限制
        }

    @classmethod
    def get_chinese_name(cls):
        return '图片'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data
