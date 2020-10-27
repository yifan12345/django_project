from django.shortcuts import render
from django.http import JsonResponse
import requests
import json


# Create your views here.
def list_case(request):
    return render(request, "case/debug.html")


# 发送请求
def send_req(request):
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
