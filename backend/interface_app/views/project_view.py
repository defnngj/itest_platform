import json
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework.views import APIView
from common_app.utils import response, response_fail, Error
from common_app.utils import Pagination
from interface_app.models import Project
from interface_app.serializers import ProjectQuerySerializer, ProjectSaveSerializer


"""
{
    "name":"研发协作平台",
    "describe": "公司研发团队使用",
    "status": true
}
"""


class ProjectView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        获得所有项目 or 一个项目信息
        """
        print("/project/{}/".format(kwargs.get("pk")))
        pk = kwargs.get("pk")
        if pk is None:
            projects = Project.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_project = pg.paginate_queryset(queryset=projects, request=request, view=self)
            data = serializers.serialize('json', page_project)
            return response(data=json.loads(data))
        else:
            try:
                project = Project.objects.get(id=pk, is_delete=False)
                project_dict = model_to_dict(project)
            except Project.DoesNotExist:
                return response(error=Error.PROJECT_ID_NULL)
            return response(data=project_dict)

    def post(self, request, *args, **kwargs):
        """
        添加一个项目
        """
        print("/project/{}/".format(kwargs.get("pk")))
        print(type(request.data), request.data)
        val = ProjectSaveSerializer(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)
        return response(data=val.data)

    def put(self, request, *args, **kwargs):
        """
        更新一个项目
        """
        pk = kwargs.get("pk")
        if pk is None:
            return response(error=Error.PROJECT_ID_NULL)
        try:
            project = Project.objects.get(id=pk, is_delete=False)
        except Project.DoesNotExist:
            return response(error=Error.PROJECT_OBJECT_NULL)
        val = ProjectSaveSerializer(instance=project, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)

        return response(data=val.data)

    def delete(self, request, *args, **kwargs):
        """
        删除项目
        """
        pk = kwargs.get("pk")
        if pk is None:
            return response(error=Error.PROJECT_ID_NULL)
        project = Project.objects.filter(id=pk, is_delete=False).update(is_delete=True)
        if project == 0:
            return response(error=Error.PROJECT_OBJECT_NULL)

        return response()
