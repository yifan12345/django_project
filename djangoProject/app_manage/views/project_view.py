from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app_manage.models import Project
from app_manage.forms import ProjectForm, ProjectEditForm
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def list_project(request):
    '''
    接口列表
    :param request:
    :return:
    '''
    username= request.COOKIES.get('user','')
    projects_list = Project.objects.all()

    return render(request, "projecrt/list.html", {"projects": projects_list,
                                                  "user":username})


@login_required
def add_project(request):
    '''项目新增'''
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name, describe=describe, status=status)
        return HttpResponseRedirect('/manage/')
    else:
        form = ProjectForm()
        return render(request, "projecrt/add.html", {'form': form})


# 编辑项目
def edit_project(request, pid):
    if request.method == "POST":
        form = ProjectEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            p = Project.objects.get(id=pid)
            p.name = name
            p.describe = describe
            p.status = status
            p.save()

        return HttpResponseRedirect('/manage/')
        # 更新数据
    else:
        if pid:
            project = Project.objects.get(id=pid)
            form = ProjectEditForm(instance=project)
        else:
            form = ProjectEditForm()
        return render(request, 'projecrt/edit.html', {
            'form': form, 'id': pid
        })


# 删除项目
def del_project(request, pid):
    if request.method == "GET":
        p = Project.objects.get(id=pid)
        p.delete()
        return HttpResponseRedirect('/manage/')
    else:
        return HttpResponseRedirect('/manage/')
