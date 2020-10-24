from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def login(request):
    '''
    登录动作的处理
    :param request:
    :return:
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(  # 用户认证鉴权：指定并关联到前端输入的用户名及密码
            username=username,
            password=password
        )
        if user is not None:
            auth.login(request, user)  # 记录用户的登录状态
            return HttpResponseRedirect("/project/1/")
        else:
            return render(request, 'login.html', {
                'error': '用户名或密码错误',
            })
    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    auth.logout(request)
    return HttpResponseRedirect("/")


