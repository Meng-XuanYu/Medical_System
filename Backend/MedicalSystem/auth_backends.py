from django.contrib.auth.backends import BaseBackend
from .models import *
from django.contrib.auth.hashers import check_password


class UserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get("base_user_type") != "user":
            return None  # 不是用户登录，不继续处理

        try:
            user = User.objects.get(user_id=username)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class DoctorBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get("base_user_type") != "doctor":
            return None  # 不是医生登录，不继续处理

        try:
            doctor = Doctor.objects.get(doctor_id=username)
            if check_password(password, doctor.password):
                return doctor
        except Doctor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None


class AdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get("base_user_type") != "admin":
            return None  # 不是管理员登录，不继续处理

        try:
            admin = Admin.objects.get(admin_id=username)
            if check_password(password, admin.password):
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None
