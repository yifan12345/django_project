import json
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app_case.models import TestCase
from app_manage.models import Project, Module
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def case_list(request):
    '''
    用例列表
    :param request:
    :return:
    '''
    # 根据id对数据进行排序
    case_list = TestCase.objects.all().order_by("id")
    # 对数据进行分页处理，每页10行显示
    p = Paginator(case_list, 10)
    # 通过请求得到需要第几页的数据
    page = request.GET.get("page", "")
    if page == "":
        page = 1
    try:
        page_cases = p.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型去第一页
        page_cases = p.page(1)
    except EmptyPage:
        # 如果页数超出范围：取最后一页
        page_cases = p.page(p.num_pages)
    return render(request, "case/list.html", {"cases": page_cases})


def new_case(request):
    '''
    新增用例
    :param request:
    :return:
    '''
    return render(request, "case/debug.html")


def edit_case(request, cid):
    '''编辑模块'''
    return render(request, "case/edit.html")

def case_delete(request,cid):
    """删除用例"""
    if request.method == "GET":
        case = TestCase.objects.get(id=cid)
        case.delete()
        return HttpResponseRedirect('/case/')
    else:
        return HttpResponseRedirect('/case/')

@csrf_exempt
def get_case_info(request):
    """获取接口数据"""
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module_id)
        case_info = model_to_dict(case)
        case_info["project"] = module.project_id
        return JsonResponse({"code": 10200,
                             "message": "success",
                             "data": case_info})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})



def send_req(request):
    '''发送请求'''
    global r
    if request.method == "GET":
        url = request.GET.get("url", "")
        method = request.GET.get("method", "")
        header = request.GET.get("header", "")
        per_type = request.GET.get("per_type", "")
        per_value = request.GET.get("per_value", "")
        if url == "":
            return JsonResponse({"code": 10101, "message": "url不能为空"})
        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10101, "message": "header格式错误，必须是标准的json格式"})

        try:
            per_value = json.loads(per_value)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10101, "message": "参数错误，必须是标准的json格式"})

        if method == "get":
            r = requests.get(url=url, params=per_value, headers=header)
        if method == "post":
            if per_type == "form":
                r = requests.post(url=url, data=per_value, headers=header)
            if per_type == "json":
                r = requests.post(url=url, json=per_value, headers=header)

    return JsonResponse({"code": 10200, "message": "success", "data": r.text})


def assert_result(request):
    """断言结果"""
    if request.method == "POST":
        result_text = request.POST.get("result_text", "")
        assert_text = request.POST.get("assert_text", "")
        assert_type = request.POST.get("assert_type", "")
        if result_text == "" or assert_text == "":
            return JsonResponse({"code": 10101, "message": "断言的参数不能为空"})
        if assert_type != "include" and assert_type != "equal":
            return JsonResponse({"code": 10101, "message": "断言类型错误"})
        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"code": 10200, "message": "断言包含成功"})
            else:
                return JsonResponse({"code": 10101, "message": "断言包含失败"})
        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"code": 10200, "message": "断言相等成功"})
            else:
                return JsonResponse({"code": 10101, "message": "断言相等失败"})

        return JsonResponse({"code": 10102, "message": "fail"})


def get_select_data(request):
    """
    获取Select下拉框需要的项目/模块数据
    """
    if request.method == "GET":
        Projects = Project.objects.all()
        data_list = []
        for p in Projects:
            project_dict = {
                "id": p.id,
                "name": p.name,
            }
            modules = Module.objects.filter(project=p)
            moduleList = []
            for m in modules:
                module_dict = {
                    "id": m.id,
                    "name": m.name,
                }
                moduleList.append(module_dict)
            project_dict["moduleList"] = moduleList
            data_list.append(project_dict)
        return JsonResponse({"code": 10200, "message": "success", "data": data_list})


def save_case(request):
    '''保存&更新case'''
    if request.method == "POST":
        case_id = request.POST.get('cid', "")
        url = request.POST.get('url', "")
        method = request.POST.get('method', "")
        per_type = request.POST.get('per_type', "")
        header = request.POST.get('header', "")
        per_value = request.POST.get('per_value', "")
        result_text = request.POST.get('result_text', "")
        assert_text = request.POST.get('assert_text', "")
        assert_type = request.POST.get('assert_type', "")
        module_id = request.POST.get('module_id', "")
        case_name = request.POST.get('case_name', "")
        if method == "get":
            method_int = 1
        elif method == "post":
            method_int = 2
        else:
            return JsonResponse({"code": 10101, "message": "请求方法错误"})

        if per_type == "form":
            per_type_int = 1
        elif per_type == "json":
            per_type_int = 2
        else:
            return JsonResponse({"code": 10102, "message": "参数类型错误"})

        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code": 10103, "message": "断言类型错误"})
        if case_id == "":
            TestCase.objects.create(module_id=module_id,
                                    name=case_name,
                                    url=url,
                                    method=method_int,
                                    header=header,
                                    parameter_type=per_type_int,
                                    parameter_body=per_value,
                                    result=result_text,
                                    assert_type=assert_type_int,
                                    assert_text=assert_text,
                                    )
            return JsonResponse({"code": 10200, "message": "create success"})
        else:
            case = TestCase.objects.get(id=case_id)
            case.module_id = module_id
            case.name = case_name
            case.url = url
            case.method = method_int
            case.case.header = header
            case.parameter_type = per_type_int
            case.parameter_body = per_value
            case.result = result_text
            case.assert_type = assert_type_int
            case.assert_text = assert_text
            case.save()
            return JsonResponse({"code": 10200, "message": "save success"})

    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})
