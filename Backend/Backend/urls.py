"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from MedicalSystem import views as ms_views

urlpatterns = [
    # path('', RedirectView.as_view(url='/homepage/', permanent=False)),
    path("admin/", admin.site.urls),
    path('homepage/', ms_views.homepage, name='homepage'),

    # 页面函数
    path("page/register/user/", ms_views.page_register_user),
    path("page/register/doctor/", ms_views.page_register_doctor),
    path("page/register/admin/", ms_views.page_admin_register),
    path("page/login/user/", ms_views.page_login_user),
    path("page/login/doctor/", ms_views.page_login_doctor),
    path("page/login/admin/", ms_views.page_login_admin),

    # 前端页面函数
    path("menu/", ms_views.menu_page),

    # 登录函数
    path('register/user/', ms_views.register_user),
    path('register/doctor/', ms_views.register_doctor),
    path('register/admin/', ms_views.register_admin),
    path('login/', ms_views.login),
    path('logout/', ms_views.logout),
    path('user/profile/', ms_views.get_base_user_profile),

    # 管理员函数
    path('<str:model_name>/all/', ms_views.get_all_record),
    path('<str:model_name>/single/', ms_views.get_single_record),
    path('<str:model_name>/update/', ms_views.update_record),
    path('<str:model_name>/add/', ms_views.add_record),
    path('<str:model_name>/delete/', ms_views.delete_record),
    
    # 预约函数
    path('appointment/info/', ms_views.get_appointment_info),
    path('user/appointment/info/', ms_views.get_user_appointment_info),
    path('user/appointment/book/', ms_views.appointment_reserve),
    path('user/appointment/cancel/', ms_views.appointment_cancel),
    path('examination/info/', ms_views.get_examination_info),
    path('user/examination/info/', ms_views.get_user_examination_info),
    path('user/examination/reserve/', ms_views.examination_reserve),
    path('user/examination/cancel/', ms_views.examination_cancel),
    path('user/wait/', ms_views.get_user_wait),
    path('user/prescription/', ms_views.get_user_prescriptions),
    path('user/ill_history/', ms_views.get_user_ill_history),
    path('user/pay/info/', ms_views.get_user_payments),
    path('user/pay/check/', ms_views.get_user_payment_check),
    path('user/comment/', ms_views.user_comment),
    path('user/get_doctors_comments/', ms_views.get_doctors_comments),
    path('notice/', ms_views.notice),

    # 家属管理
    path('teacher/family_members/info/', ms_views.get_family_members),
    path('teacher/family_members/update/', ms_views.update_family_members),
    path('teacher/family_members/add/', ms_views.add_family_members),
    path('teacher/family_members/delete/', ms_views.delete_family_members),

    # 医师相关
    path('doctor/schedule/info/', ms_views.get_doctor_schedule),
    path('doctor/schedule/appointment/', ms_views.get_doctor_schedule_appointment),
    path('doctor/schedule/appointment/done/', ms_views.set_doctor_schedule_appointment_done),
    path('doctor/comment/', ms_views.get_doctor_comments),
    path('doctor/patients/past/', ms_views.get_doctor_patients_past),
    path('doctor/patients/future/', ms_views.get_doctor_patients_future),
    path('doctor/prescription/add/', ms_views.doctor_add_prescription),
    path('doctor/prescription/info/', ms_views.get_doctor_prescription),
    path('doctor/medicine/info/', ms_views.get_medicine_info),
    path('doctor/medicine/decrease/', ms_views.doctor_prescribe),

    path('getImageUrl/', ms_views.getImageUrl),  # 获取图片地址
    # 测试用函数
    path('user/info/', ms_views.get_user_info),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
