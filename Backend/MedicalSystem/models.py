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
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 身份证号：非空
    user_type = models.CharField(max_length=1, null=False, blank=False)  # 用户类型：非空
    phone = models.CharField(max_length=11, null=False, blank=False)  # 手机号：非空

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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def to_view_fields(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'birth': self.birth,
            'id_number': self.id_number,
            'user_type': self.user_type,
            'phone': self.phone
        }

    def update_view_fields(self, data):
        self.name = data.get('name', self.name)
        self.gender = data.get('gender', self.gender)
        self.birth = data.get('birth', self.birth)
        self.id_number = data.get('id_number', self.id_number)
        self.user_type = data.get('user_type', self.user_type)
        self.phone = data.get('phone', self.phone)
        self.save()


# 表 2: 医师用户数据元素表
class Doctor(BaseUser):
    doctor_id = models.CharField(max_length=5, primary_key=True, unique=True, db_index=True)  # 医工号：主键
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

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'doctor_id': 5,
            'password': 128,
            'name': 15,
            'gender': 1,
            'title': 10
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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'gender': self.gender,
            'title': self.title,
            'image_id': self.image_id,
            'introduction': self.introduction
        }

    def update_view_fields(self, data):
        self.name = data.get('name', self.name)
        self.gender = data.get('gender', self.gender)
        self.title = data.get('title', self.title)
        self.image_id = data.get('image_id', self.image_id)
        self.introduction = data.get('introduction', self.introduction)
        self.save()


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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def to_view_dict(self):
        return {
            'admin_id': self.admin_id,
            'name': self.name
        }

    def update_view_fields(self, data):
        self.name = data.get('name', self.name)
        self.save()


# 表 4: 家属数据元素表
class FamilyMember(models.Model):
    family_id = models.CharField(max_length=2)  # 家属号：主键
    user_id = models.CharField(max_length=8)  # 学工号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 关系：非空
    name = models.CharField(max_length=15, null=False, blank=False)  # 姓名：非空
    gender = models.CharField(max_length=1, null=False, blank=False)  # 性别：非空
    birth = models.DateField(null=False, blank=False)  # 出生日期：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 身份证号：非空

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['family_id', 'user_id'], name='unique_family_teacher')
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'family_id': 2,
            'user_id': 8,
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
    def get_chinese_name(cls):
        return '家属'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'family_id': self.family_id,
            'user_id': self.user_id,
            'relationship': self.relationship,
            'name': self.name,
            'gender': self.gender,
            'birth': self.birth,
            'id_number': self.id_number
        }

    def update_view_fields(self, data):
        self.relationship = data.get('relationship', self.relationship)
        self.name = data.get('name', self.name)
        self.gender = data.get('gender', self.gender)
        self.birth = data.get('birth', self.birth)
        self.id_number = data.get('id_number', self.id_number)
        self.save()


# 表 5: 科室数据元素表
class Department(models.Model):
    department_id = models.CharField(max_length=3, primary_key=True, unique=True)  # 科室号：主键
    department_name = models.CharField(max_length=10, null=False, blank=False)  # 科室名称：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name
        }

    def update_view_fields(self, data):
        self.department_name = data.get('department_name', self.department_name)
        self.save()


# 表 6: 排班数据元素表
class Schedule(models.Model):
    schedule_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 排班号：主键
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, to_field='doctor_id', db_index=True)  # 外键引用 Doctor
    department = models.ForeignKey('Department', on_delete=models.CASCADE, to_field='department_id',
                                   db_index=True)  # 外键引用 Department
    schedule_time = models.CharField(max_length=6, null=False, blank=False)  # 排班时间：非空

    class Meta:
        indexes = [
            models.Index(fields=['department_id', 'doctor'])  # 复合索引
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'schedule_id': 8,
            'doctor_id': 5,
            'department_id': 3,
            'schedule_time': None,  # json字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '排班'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        if 'doctor_id' in data:
            doctor_id = data.pop('doctor_id')
            try:
                doctor = Doctor.objects.get(doctor_id=doctor_id)
                data['doctor'] = doctor  # 将 doctor_id 转为 doctor 对象
            except Doctor.DoesNotExist:
                raise ValueError(f"Doctor with id {doctor_id} does not exist")
        if 'department_id' in data:
            department_id = data.pop('department_id')
            try:
                department = Department.objects.get(department_id=department_id)
                data['department'] = department  # 将 department_id 转为 department 对象
            except Doctor.DoesNotExist:
                raise ValueError(f"Department with id {department_id} does not exist")
        return data

    def get_view_dic(self):
        return {
            'schedule_id': self.schedule_id,
            'doctor_id': self.doctor_id,
            'department_id': self.department_id,
            'schedule_time': self.schedule_time
        }

    def update_view_fields(self, data):
        self.doctor_id = data.get('doctor_id', self.doctor_id)
        self.department_id = data.get('department_id', self.department_id)
        self.schedule_time = data.get('schedule_time', self.schedule_time)
        self.save()


# 表 7: 药房数据元素表
class Pharmacy(models.Model):
    pharmacy_id = models.CharField(max_length=2, primary_key=True, unique=True)  # 药房号：主键
    pharmacy_name = models.CharField(max_length=10, null=False, blank=False)  # 药房名称：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'pharmacy_id': self.pharmacy_id,
            'pharmacy_name': self.pharmacy_name
        }

    def update_view_fields(self, data):
        self.pharmacy_name = data.get('pharmacy_name', self.pharmacy_name)
        self.save()


# 表 8: 药品数据元素表
class Drug(models.Model):
    drug_id = models.CharField(max_length=9, primary_key=True, unique=True)  # 药品号：主键
    drug_name = models.CharField(max_length=20, null=False, blank=False)  # 药品名称：非空
    price = models.FloatField(null=False, blank=False)  # 药品价格：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'drug_id': 9,
            'drug_name': 20,
            'price': None,  # 浮点数字段无需长度限制
        }

    @classmethod
    def get_optional_fields(cls):
        return {}

    @classmethod
    def get_chinese_name(cls):
        return '药品'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'drug_id': self.drug_id,
            'drug_name': self.drug_name,
            'price': self.price
        }

    def update_view_fields(self, data):
        self.drug_name = data.get('drug_name', self.drug_name)
        self.price = data.get('price', self.price)
        self.save()


# 表 9: 药品库存数据元素表
class DrugInventory(models.Model):
    drug_id = models.CharField(max_length=9)  # 药品号：主键
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    pharmacy_id = models.CharField(max_length=2)  # 药房号：主键

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['drug_id', 'pharmacy_id'], name='unique_drug_pharmacy')
        ]

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'drug_id': self.drug_id,
            'drug_amount': self.drug_amount,
            'pharmacy_id': self.pharmacy_id
        }

    def update_view_fields(self, data):
        self.drug_amount = data.get('drug_amount', self.drug_amount)
        self.pharmacy_id = data.get('pharmacy_id', self.pharmacy_id)
        self.save()


# 表 10: 体检安排元素表
class ExaminationArrangement(models.Model):
    examination_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 体检号：主键
    examination = models.TextField(null=False, blank=False)  # 体检项目：非空
    examination_date = models.DateField(null=False, blank=False)  # 体检日期：非空
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 负责医工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'examination_id': self.examination_id,
            'examination': self.examination,
            'examination_date': self.examination_date,
            'doctor_id': self.doctor_id
        }

    def update_view_fields(self, data):
        self.examination = data.get('examination', self.examination)
        self.examination_date = data.get('examination_date', self.examination_date)
        self.doctor_id = data.get('doctor_id', self.doctor_id)
        self.save()


# 表 11: 体检信息数据元素表
class ExaminationInfo(models.Model):
    exam_appointment_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 体检预约号：主键
    examination_id = models.CharField(max_length=8, null=False, blank=False)  # 体检号：非空
    examination_result = models.TextField(null=True, blank=True)  # 体检结果：可空
    user_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'exam_appointment_id': 8,
            'examination_id': 8,
            'user_id': 8
        }

    @classmethod
    def get_optional_fields(cls):
        return {
            'examination_result': None  # text字段无需长度限制
        }

    @classmethod
    def get_chinese_name(cls):
        return '体检信息'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'exam_appointment_id': self.exam_appointment_id,
            'examination_id': self.examination_id,
            'examination_result': self.examination_result,
            'user_id': self.user_id
        }

    def update_view_fields(self, data):
        self.examination_id = data.get('examination_id', self.examination_id)
        self.examination_result = data.get('examination_result', self.examination_result)
        self.user_id = data.get('user_id', self.user_id)
        self.save()


# 表 12: 预约数据元素表
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 预约号：主键
    relationship = models.CharField(max_length=10, null=False, blank=False)  # 患者与预约人关系：非空
    schedule_id = models.CharField(max_length=8, null=False, blank=False)  # 排班号：非空
    user_id = models.CharField(max_length=8, null=False, blank=False)  # 学工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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
        return data

    def get_view_dic(self):
        return {
            'appointment_id': self.appointment_id,
            'relationship': self.relationship,
            'schedule_id': self.schedule_id,
            'user_id': self.user_id
        }

    def update_view_fields(self, data):
        self.relationship = data.get('relationship', self.relationship)
        self.schedule_id = data.get('schedule_id', self.schedule_id)
        self.user_id = data.get('user_id', self.user_id)
        self.save()


# 表 13: 诊断数据元素表
class Diagnosis(models.Model):
    diagnosis_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 诊断号：主键
    examination = models.TextField(null=False, blank=False)  # 检查项目：非空
    examination_result = models.TextField(null=False, blank=False)  # 检查结果：非空
    reference = models.TextField(null=False, blank=False)  # 参考范围：非空
    clinical_diagnosis = models.TextField(null=False, blank=False)  # 临床诊断：非空
    prescription_id = models.CharField(max_length=8, null=False, blank=False)  # 处方号：非空
    diagnosis_time = models.DateTimeField(null=False, blank=False)  # 诊断时间：非空
    id_number = models.CharField(max_length=18, null=False, blank=False)  # 患者身份证号：非空
    appointment_id = models.CharField(max_length=8, null=False, blank=False)  # 预约号：非空
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 医工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    def get_view_dic(self):
        return {
            'diagnosis_id': self.diagnosis_id,
            'examination': self.examination,
            'examination_result': self.examination_result,
            'reference': self.reference,
            'clinical_diagnosis': self.clinical_diagnosis,
            'prescription_id': self.prescription_id,
            'diagnosis_time': self.diagnosis_time,
            'id_number': self.id_number,
            'appointment_id': self.appointment_id,
            'doctor_id': self.doctor_id
        }

    def update_view_fields(self, data):
        self.examination = data.get('examination', self.examination)
        self.examination_result = data.get('examination_result', self.examination_result)
        self.reference = data.get('reference', self.reference)
        self.clinical_diagnosis = data.get('clinical_diagnosis', self.clinical_diagnosis)
        self.prescription_id = data.get('prescription_id', self.prescription_id)
        self.diagnosis_time = data.get('diagnosis_time', self.diagnosis_time)
        self.id_number = data.get('id_number', self.id_number)
        self.appointment_id = data.get('appointment_id', self.appointment_id)
        self.doctor_id = data.get('doctor_id', self.doctor_id)
        self.save()


# 表 14: 处方数据元素表
class Prescription(models.Model):
    prescription_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 处方号：主键
    diagnosis_id = models.CharField(max_length=8, null=False, blank=False)  # 诊断号：非空
    drug_id = models.CharField(max_length=9, null=False, blank=False)  # 药品号：非空
    drug_amount = models.IntegerField(null=False, blank=False)  # 药品数量：非空
    usage = models.TextField(null=False, blank=False)  # 用法用量：非空
    precautions = models.TextField(null=False, blank=False)  # 注意事项：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    def get_view_dic(self):
        return {
            'prescription_id': self.prescription_id,
            'diagnosis_id': self.diagnosis_id,
            'drug_id': self.drug_id,
            'drug_amount': self.drug_amount,
            'usage': self.usage,
            'precautions': self.precautions
        }

    def update_view_fields(self, data):
        self.diagnosis_id = data.get('diagnosis_id', self.diagnosis_id)
        self.drug_id = data.get('drug_id', self.drug_id)
        self.drug_amount = data.get('drug_amount', self.drug_amount)
        self.usage = data.get('usage', self.usage)
        self.precautions = data.get('precautions', self.precautions)
        self.save()


# 表 15: 通知数据元素表
class Notification(models.Model):
    notification_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 通知号：主键
    notification = models.TextField(null=False, blank=False)  # 通知内容：非空
    notification_time = models.DateTimeField(null=False, blank=False)  # 通知时间：非空
    user_id = models.CharField(max_length=8, null=False, blank=False)  # 接收人学工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

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

    def get_view_dic(self):
        return {
            'notification_id': self.notification_id,
            'notification_text': self.notification,
            'notification_time': self.notification_time,
            'user_id': self.user_id
        }

    def update_view_fields(self, data):
        self.notification = data.get('notification', self.notification)
        self.notification_time = data.get('notification_time', self.notification_time)
        self.user_id = data.get('user_id', self.user_id)
        self.save()


# 表 16: 评价数据元素表
class Evaluation(models.Model):
    evaluation_id = models.CharField(max_length=8, primary_key=True, unique=True)  # 评价号：主键
    evaluation = models.TextField(null=False, blank=False)  # 评价内容：非空
    evaluation_time = models.DateTimeField(null=False, blank=False)  # 评价时间：非空
    user_id = models.CharField(max_length=8, null=False, blank=False)  # 评价人学工号：非空
    doctor_id = models.CharField(max_length=5, null=False, blank=False)  # 被评价人医工号：非空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'evaluation_id': 8,
            'evaluation': None,  # text字段无需长度限制
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

    def get_view_dic(self):
        return {
            'evaluation_id': self.evaluation_id,
            'evaluation': self.evaluation,
            'evaluation_time': self.evaluation_time,
            'user_id': self.user_id,
            'doctor_id': self.doctor_id
        }

    def update_view_fields(self, data):
        self.evaluation = data.get('evaluation', self.evaluation)
        self.evaluation_time = data.get('evaluation_time', self.evaluation_time)
        self.user_id = data.get('user_id', self.user_id)
        self.doctor_id = data.get('doctor_id', self.doctor_id)
        self.save()


# 表 17: 图片数据元素表
class Image(models.Model):
    image_id = models.CharField(max_length=10, primary_key=True, unique=True)  # 图片号：主键
    image_path = models.CharField(max_length=255, null=False, blank=False)  # 存储路径：非空
    evaluation_id = models.CharField(max_length=8, null=True, blank=True)  # 评价号：可空
    notification_id = models.CharField(max_length=8, null=True, blank=True)  # 通知号：可空
    drug_id = models.CharField(max_length=9, null=True, blank=True)  # 药品号：可空

    @classmethod
    def get_fields(cls):
        return cls._meta.get_fields()

    @classmethod
    def get_required_fields(cls):
        return {
            'image_id': 10,
            'image_path': 255
        }

    @classmethod
    def get_optional_fields(cls):
        return {
            'evaluation_id': 8,
            'notification_id': 8,
            'drug_id': 9
        }

    @classmethod
    def get_chinese_name(cls):
        return '图片'

    # 对于外键字段进行处理，将其转换为模型对象
    @classmethod
    def prepare_data(cls, data):
        return data

    def get_view_dic(self):
        return {
            'image_id': self.image_id,
            'image_path': self.image_path,
            'evaluation_id': self.evaluation_id,
            'notification_id': self.notification_id,
            'drug_id': self.drug_id
        }

    def update_view_fields(self, data):
        self.image_path = data.get('image_path', self.image_path)
        self.evaluation_id = data.get('evaluation_id', self.evaluation_id)
        self.notification_id = data.get('notification_id', self.notification_id)
        self.drug_id = data.get('drug_id', self.drug_id)
        self.save()
