import json
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework.views import APIView
from common_app.utils import response, response_fail, Error
from common_app.utils import Pagination
from interface_app.models import Project
from interface_app.serializers import ProjectValidators


class ProjectView(APIView):
    authentication_classes = []

    def get(self, request, pk):
        """
        获得一个项目信息
        """
        print("/project/{}/".format(pk))
        try:
            project = Project.objects.get(id=pk)
            project_dict = model_to_dict(project)
        except Project.DoesNotExist:
            return response(error=Error.PROJECT_ID_NULL)
        return response(data=project_dict)

    def post(self, request, pk):
        """
        添加一个项目
        """
        print("/project/{}/".format(pk))
        print(type(request.data), request.data)
        val = ProjectValidators(data=request.data)
        if val.is_valid() is False:
            return response_fail(val.errors)
        name = request.data.get('name', "")
        describe = request.data.get('describe', "")
        status = request.data.get('status', True)
        project = Project.objects.create(name=name, describe=describe, status=status)
        project_dict = model_to_dict(project)
        return response(data=project_dict)

    def put(self, request, pk):
        """
        更新一个项目
        """
        print("/project/{}/".format(pk))
        val = ProjectValidators(data=request.data)
        if val.is_valid() is False:
            return response_fail(val.errors)

        try:
            project = Project.objects.get(id=pk)
            project.name = request.data.get('name')
            project.describe = request.data.get('describe', "")
            project.status = request.data.get('status', True)
            project.save()
        except Project.DoesNotExist:
            return response(error=Error.PROJECT_ID_NULL)
        return response()

    def delete(self, request, pk):
        """
        删除项目
        """
        print("/project/{}/".format(pk))
        try:
            project = Project.objects.get(id=pk)
            project.delete()
        except Project.DoesNotExist:
            return response(error=Error.PROJECT_ID_NULL)
        return response()


class ProjectsView(APIView):
    authentication_classes = []

    def get(self, request):
        """
        获得所有项目信息
        """
        print("/projects/")
        projects = Project.objects.all()
        pg = Pagination()
        page_project = pg.paginate_queryset(queryset=projects, request=request, view=self)
        data = serializers.serialize('json', page_project)
        return response(data=json.loads(data))

