from django.shortcuts import render, redirect
from django.http import HttpResponse


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("psw")
        if username == "admin" and password == "123456":
            # return HttpResponse("登录成功")
            return redirect("https://buaa.edu.cn/")
        else:
            return render(request, "login.html", {"error_msg": "用户名或密码错误！"})
