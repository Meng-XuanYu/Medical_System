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
    path("register/user/", ms_views.user_register_page),
    path("register/doctor/", ms_views.doctor_register_page),
    path("register/admin/", ms_views.admin_register_page),
    path("login/user/", ms_views.user_login_page),
    path("login/doctor/", ms_views.doctor_login_page),
    path("login/admin/", ms_views.admin_login_page),
    path('api/user/register/', ms_views.user_register),
    path('api/user/login/', ms_views.user_login),
    path('api/user/logout/', ms_views.user_logout),
    path('api/doctor/register/', ms_views.doctor_register),
    path('api/doctor/login/', ms_views.doctor_login),
    path('api/doctor/logout/', ms_views.doctor_logout),
    path('api/admin/register/', ms_views.admin_register),
    path('api/admin/login/', ms_views.admin_login),
    path('api/admin/logout/', ms_views.admin_logout),
]
