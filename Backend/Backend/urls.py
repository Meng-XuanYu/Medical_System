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

from MedicalSystem import views as ms_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('homepage/', ms_views.homepage, name='homepage'),
    path("page/register/user/", ms_views.page_register_user),
    path("page/register/doctor/", ms_views.page_register_doctor),
    path("page/register/admin/", ms_views.page_admin_register),
    path("page/login/user/", ms_views.page_login_user),
    path("page/login/doctor/", ms_views.page_login_doctor),
    path("page/login/admin/", ms_views.page_login_admin),
    path("page/view/doctors/", ms_views.view_doctors_page, name='view_doctors'),
    path("page/edit/doctor/", ms_views.edit_doctor_page),
    path('register/user/', ms_views.register_user),
    path('register/doctor/', ms_views.register_doctor),
    path('register/admin/', ms_views.register_admin),
    path('login/', ms_views.login),
    path('logout/', ms_views.logout),
    path("view/doctor/", ms_views.view_doctor),
    path('view/doctors/', ms_views.view_doctors),
    path('edit/doctor/', ms_views.edit_doctor),

    # 测试用函数
    path('api/user/info/', ms_views.get_user_info),
]
