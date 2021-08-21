from rest_framework.views import APIView
from common_app.utils import response, Error, response_fail
from common_app.utils import Pagination
from interface_app.models import TestCase
from interface_app.serializers import CaseValidators, CaseSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


class CaseViewSet(ViewSet):
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
            return response_fail(val.errors)

        return response(data=val.data)

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
                return response(error=Error.CASE_ID_NULL)
            return response(data=ser.data)

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
        return response(data=data)

    @action(methods=["put"], detail=False, url_path='update')
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        /api/interface/v1/case/update/
        """
        cid = request.data.get("id")
        if cid is None:
            return response(error=Error.CASE_ID_NULL)
        case = TestCase.objects.get(pk=cid, is_delete=False)
        val = CaseValidators(instance=case, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)

        return response(data=val.data)

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_case(self, request, *args, **kwargs):
        """
        删除用例
        /api/interface/v1/case/<pk>/info/
        """
        pk = kwargs.get("pk")
        if pk is None:
            return response(error=Error.CASE_ID_NULL)
        try:
            TestCase.objects.get(id=pk, is_delete=False).update(is_delete=True)
        except TestCase.DoesNotExist:
            return response(error=Error.CASE_OBJECT_NULL)
        return response()


class CaseView(APIView):
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
                return response(error=Error.PROJECT_ID_NULL)
            return response(data=ser.data)
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
            return response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加一条用例
        """
        val = CaseValidators(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)

        return response(data=val.data)

    def put(self, request, *args, **kwargs):
        """
        更新一条用例
        """
        cid = request.data.get("id")
        if cid is None:
            return response(error=Error.CASE_ID_NULL)
        case = TestCase.objects.get(pk=cid, is_delete=False)
        val = CaseValidators(instance=case, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)

        return response(data=val.data)

    def delete(self, request, *args, **kwargs):
        """
        删除用例
        """
        pk = kwargs.get("pk")
        if pk is None:
            return response(error=Error.CASE_ID_NULL)
        try:
            TestCase.objects.get(id=pk, is_delete=False).update(is_delete=True)
        except TestCase.DoesNotExist:
            return response(error=Error.CASE_OBJECT_NULL)
        return response()
