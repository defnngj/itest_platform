from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from common_app.utils import response, Error, response_fail
from django.forms.models import model_to_dict
from common_app.utils import Pagination
from interface_app.models import Project, Module, TestCase
from interface_app.serializers import CaseValidators


class CaseView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """
        添加一条用例
        """
        print("/case/ POST".format(kwargs))
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
        print("/case/ POST".format(kwargs))
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
