from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from common_app.utils import response, Error, response_fail
from django.forms.models import model_to_dict
from common_app.utils import Pagination
from interface_app.models import Project, Module, TestCase
from interface_app.serializers import CaseValidators, CaseSerializer


class CaseView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        获得用例数据
        """
        pk = kwargs.get("pk")
        if pk is not None:
            print("/case/1/")
            try:
                case = TestCase.objects.get(id=pk)
                ser = CaseSerializer(instance=case, many=False)
            except TestCase.DoesNotExist:
                return response(error=Error.PROJECT_ID_NULL)
            return response(data=ser.data)
        else:
            print("/case/?page=1&size=10")
            test_case = TestCase.objects.all()
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
        case = TestCase.objects.get(pk=cid)
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
            case = TestCase.objects.get(id=pk)
            case.delete()
        except TestCase.DoesNotExist:
            return response(error=Error.CASE_OBJECT_NULL)
        return response()
