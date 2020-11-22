from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_manage.models.case import TestCase


def list_case(request):
    """用例例表"""
    cases = TestCase.objects.all()
    p = Paginator(cases, 10)
    page = request.GET.get("page", "")
    if page == "":
        page = 1

    try:
        page_cases = p.page(page)
    except EmptyPage:
        page_cases = p.page(p.num_pages)
    except PageNotAnInteger:
        page_cases = p.page(1)
    return render(request, "case/list.html", {"cases": page_cases})


def add_case(request):
    """添加用例"""
    return render(request, "case/debug.html")


def edit_case(request, cid):
    """编辑用例"""
    return render(request, "case/edit.html")

