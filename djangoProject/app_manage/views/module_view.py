from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app_manage.models import Module
from app_manage.forms import ModuleForm
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def list_module(request):
    '''
    模块管理
    :param request:
    :return:
    '''

    module_list = Module.objects.all()
    return render(request, "module/list.html", {"module": module_list})


def add_module(request):
    '''创建模块'''
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(project=project, name=name, describe=describe)
        return HttpResponseRedirect('/manage/module_list/')
    else:
        form = ModuleForm()
        return render(request, "module/add.html", {'form': form})


def edit_module(request, mid):
    '''编辑模块'''
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            m = Module.objects.get(id=mid)
            m.project = project
            m.name = name
            m.describe = describe
            m.save()

        return HttpResponseRedirect('/manage/module_list/')
        # 更新数据
    else:
        if mid:
            m = Module.objects.get(id=mid)
            form = ModuleForm(instance=m)
        else:
            form = ModuleForm()
        return render(request, 'module/edit.html', {
            'form': form, 'id': mid
        })


def del_module(request, mid):
    '''删除模块'''
    if request.method == "GET":
        p = Module.objects.get(id=mid)
        p.delete()
        return HttpResponseRedirect('/manage/module_list/')
    else:
        return HttpResponseRedirect('/manage/module_list/')
