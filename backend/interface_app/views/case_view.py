import json
import requests
from rest_framework.decorators import action
from common_app.utils import BaseAPIView, BaseViewSet
from common_app.utils import Pagination
from interface_app.serializers import CaseValidators, CaseSerializer, DebugValidators, AssertValidators
from interface_app.models import Project, Module, TestCase


class CaseViewSet(BaseViewSet):
    queryset = TestCase.objects.all()
    serializer_class = CaseSerializer
    authentication_classes = []

    @action(methods=["post"], detail=False, url_path='create')
    def case_create(self, request, *args, **kwargs):
        """
        添加一条用例
        /api/interface/v1/case/
        """
        val = CaseValidators(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response(data=val.data)

    @action(methods=["get"], detail=True, url_path='info')
    def get_case(self, request, *args, **kwargs):
        """
        获得用例数据
        /api/interface/v1/case/<pk>/info/
        """
        pk = kwargs.get("pk")
        if pk is not None:
            try:
                case = TestCase.objects.get(id=pk, is_delete=False)
                ser = CaseSerializer(instance=case, many=False)
            except TestCase.DoesNotExist:
                return self.response(error=self.CASE_ID_NULL)
            return self.response(data=ser.data)

    @action(methods=["get"], detail=False, url_path='list')
    def get_cases_list(self, request, *args, **kwargs):
        """
        获得用例数据
        /api/interface/v1/case/list/
        """
        test_case = TestCase.objects.filter(is_delete=False).all()
        pg = Pagination()
        page_module = pg.paginate_queryset(queryset=test_case, request=request, view=self)
        ser = CaseSerializer(instance=page_module, many=True)
        data = {
            "total": test_case.count(),
            "caseList": ser.data
        }
        return self.response(data=data)

    @action(methods=["put"], detail=False, url_path='update')
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        /api/interface/v1/case/update/
        """
        cid = request.data.get("id")
        if cid is None:
            return self.response(error=self.CASE_ID_NULL)
        case = TestCase.objects.get(pk=cid, is_delete=False)
        val = CaseValidators(instance=case, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response(data=val.data)

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_case(self, request, *args, **kwargs):
        """
        删除用例
        /api/interface/v1/case/<pk>/delete/
        """
        pk = kwargs.get("pk")
        if pk is None:
            return self.response(error=self.CASE_ID_NULL)
        case = TestCase.objects.filter(id=pk, is_delete=False).update(is_delete=True)
        if case == 0:
            return self.response(error=self.CASE_OBJECT_NULL)

        return self.response()

    @action(methods=["get"], detail=False, url_path='tree')
    def get_cases_tree(self, request, *args, **kwargs):
        """
        获得用例树: 项目-> 模块 -> 用例
        /api/interface/v1/case/tree/
        """
        projects = Project.objects.filter(is_delete=False)
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Module.objects.filter(project_id=project.id, is_delete=False)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }

                cases = TestCase.objects.filter(module_id=module.id, is_delete=False)
                case_list = []
                for case in cases:
                    case_dict = {
                        "name": case.name,
                        "isParent": False,
                        "id": case.id,
                    }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)

        return self.response(data=data_list)

    @action(methods=["post"], detail=False, url_path="debug")
    def post_case_debug(self, request, *args, **kwargs):
        val = DebugValidators(data=request.data)
        if val.is_valid() is False:
            return self.response_fail(val.errors)

        url = request.data.get("url")
        method = request.data.get("method")
        header = request.data.get("header")
        params_type = request.data.get("params_type")
        params_body = request.data.get("params_body")
        resp_data = "error"
        header_dict = json.loads(header)
        params_body_dict = json.loads(params_body)
        if method == "GET":
            r = requests.get(url, params=params_body_dict, headers=header_dict)
            resp_data = r.text
        if method == "POST":
            if params_type == "form":
                r = requests.post(url, data=params_body_dict, headers=header_dict)
                resp_data = r.text
            if params_type == "json":
                r = requests.post(url, json=params_body_dict, headers=header_dict)
                resp_data = r.text

        return self.response(data=resp_data)

    @action(methods=["post"], detail=False, url_path="assert")
    def post_case_assert(self, request, *args, **kwargs):
        val = AssertValidators(data=request.data)
        if val.is_valid() is False:
            return self.response_fail(val.errors)

        result = request.data.get("result")
        assert_type = request.data.get("assert_type")
        assert_text = request.data.get("assert_text")
        print(result)
        print(assert_type)
        print(assert_text)
        if assert_type == "include":
            if assert_text in result:
                return self.response()
            else:
                return self.response(error=self.CASE_ASSERT_INCLUDE_FAIL)

        if assert_type == "equal":
            if assert_text == result:
                return self.response()
            else:
                return self.response(error=self.CASE_ASSERT_EQUAL_FAIL)



class CaseView(BaseAPIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        获得用例数据
        """
        pk = kwargs.get("pk")
        if pk is not None:
            try:
                case = TestCase.objects.get(id=pk, is_delete=False)
                ser = CaseSerializer(instance=case, many=False)
            except TestCase.DoesNotExist:
                return self.response(error=self.PROJECT_ID_NULL)
            return self.response(data=ser.data)
        else:
            print("/case/?page=1&size=10")
            test_case = TestCase.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_module = pg.paginate_queryset(queryset=test_case, request=request, view=self)
            ser = CaseSerializer(instance=page_module, many=True)
            data = {
                "total": test_case.count(),
                "caseList": ser.data
            }
            return self.response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加一条用例
        """
        val = CaseValidators(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response(data=val.data)

    def put(self, request, *args, **kwargs):
        """
        更新一条用例
        """
        cid = request.data.get("id")
        if cid is None:
            return self.response(error=self.CASE_ID_NULL)
        case = TestCase.objects.get(pk=cid, is_delete=False)
        val = CaseValidators(instance=case, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response(data=val.data)

    def delete(self, request, *args, **kwargs):
        """
        删除用例
        """
        pk = kwargs.get("pk")
        if pk is None:
            return self.response(error=self.CASE_ID_NULL)
        try:
            TestCase.objects.get(id=pk, is_delete=False).update(is_delete=True)
        except TestCase.DoesNotExist:
            return self.response(error=self.CASE_OBJECT_NULL)
        return self.response()
