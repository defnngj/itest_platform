import json
import requests
from django.http import JsonResponse
from django.forms.models import model_to_dict
from app_manage.models.project import Project
from app_manage.models.module import Module
from app_manage.models.case import TestCase


def delete_case(request):
    """删除用例"""
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        case.delete()
        return JsonResponse({"code": 10200, "message": "success"})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})


def send_req(request):
    """
    发送接口
    """
    if request.method == "GET":
        url = request.GET.get("url", "")
        method = request.GET.get("method", "")
        header = request.GET.get("header", "")
        par_type = request.GET.get("par_type", "")
        par_value = request.GET.get("par_value", "")

        if url == "":
            return JsonResponse({"code": 10101, "message": "URL不能为空！"})

        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message": "Header格式错误，必须是标准的JSON格式！"})

        try:
            par_value = json.loads(par_value)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103,
                                 "message": "参数格式错误，必须是标准的JSON格式！"})

        resp_data = ""
        if method == "get":
            r = requests.get(url, params=par_value, headers=header)
            resp_data = r.text
        if method == "post":
            if par_type == "form":
                r = requests.post(url, data=par_value, headers=header)
                resp_data = r.text
            if par_type == "json":
                r = requests.post(url, json=par_value, headers=header)
                resp_data = r.text

        return JsonResponse({"code": 10200, "message": "success", "data": resp_data})


def assert_result(request):
    """
    断言结果
    """
    if request.method == "POST":
        result_text = request.POST.get("result_text", "")
        assert_type = request.POST.get("assert_type", "")
        assert_text = request.POST.get("assert_text", "")
        print("-------->", result_text)
        print(assert_type)
        print(assert_text)

        if result_text == "" or assert_text == "":
            return JsonResponse({"code": 10101, "message": "断言的参数不能为空"})

        if assert_type != "include" and assert_type != "equal":
            return JsonResponse({"code": 10101, "message": "断言的参数不能为空"})

        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"code": 10200, "message": "断言包含成功"})
            else:
                return JsonResponse({"code": 10200, "message": "断言包含失败"})

        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"code": 10200, "message": "断言相等成功"})
            else:
                return JsonResponse({"code": 10200, "message": "断言相等失败"})

        return JsonResponse({"code": 10102, "message": "fail"})


def save_case(request):
    """
    用例创建/编辑保存
    """
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        parameter_type = request.POST.get("par_type", "")
        parameter_body = request.POST.get("par_value", "")
        result_text = request.POST.get("result_text", "")
        assert_type = request.POST.get("assert_type", "")
        assert_text = request.POST.get("assert_text", "")
        module_id = request.POST.get("mid", "")
        name = request.POST.get("name", "")
        cid = request.POST.get("cid", "")

        print("parameter_type", parameter_type)

        if name == "":
            return JsonResponse({"status": 10101, "message": "用例名称不能为空"})

        if module_id == "":
            return JsonResponse({"status": 10103, "message": "所属的模块不能为空"})

        if assert_type == "" or assert_text == "":
            return JsonResponse({"status": 10102, "message": "断言的类型或文本不能为空"})

        if method == "get":
            method_number = 1
        elif method == "post":
            method_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的请求方法"})

        if parameter_type == "form":
            parameter_number = 1
        elif parameter_type == "json":
            parameter_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的参数类型"})

        if assert_type == "include":
            assert_number = 1
        elif assert_type == "equal":
            assert_number = 2
        else:
            return JsonResponse({"status": 10104, "message": "未知的断言类型"})

        if cid == "":
            TestCase.objects.create(name=name,
                                    module_id=module_id,
                                    url=url,
                                    header=header,
                                    method=method_number,
                                    parameter_type=parameter_number,
                                    parameter_body=parameter_body,
                                    result=result_text,
                                    assert_type=assert_number,
                                    assert_text=assert_text)
            return JsonResponse({"status": 10200, "message": "创建成功！"})
        else:
            case = TestCase.objects.get(id=cid)
            case.name = name
            case.module_id = module_id
            case.url = url
            case.header = header
            case.method = method_number
            case.parameter_type = parameter_number
            case.parameter_body = parameter_body
            case.result = result_text,
            case.assert_type = assert_number
            case.assert_text = assert_text
            case.save()
        return JsonResponse({"status": 10200, "message": "保存成功！"})
    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})


def get_select_data(request):
    """
    获取 "项目>模块" 列表
    :param request:
    :return: 项目接口列表
    """
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "id": project.id,
                "name": project.name
            }

            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_list.append({
                    "id": module.id,
                    "name": module.name,
                })

            project_dict["moduleList"] = module_list
            data_list.append(project_dict)

        return JsonResponse({"status": 10200, "message": "success", "data": data_list})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})


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
