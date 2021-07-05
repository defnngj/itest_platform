import json
from project_app.models import Project, Module
from rest_framework.views import APIView
from personal_app.utils import response, Error
from django.forms.models import model_to_dict
from django.core import serializers


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
            return response(Error.PROJECT_ID_NULL)
        return response(data=project_dict)

    def post(self, request, pk):
        """
        添加一个项目
        """
        print("/project/{}/".format(pk))
        print(type(request.data), request.data)
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
        name = request.data.get('name', "")
        describe = request.data.get('describe', "")
        status = request.data.get('status', True)
        try:
            project = Project.objects.get(id=pk)
            project.name = name
            project.describe = describe
            project.status = status
            project.save()
        except Project.DoesNotExist:
            return response(error=Error.PROJECT_ID_NULL)
        return response()

    def delete(self, request, pk):
        """
        删除项目
        """
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
        data = serializers.serialize('json', projects)
        return response(data=json.loads(data))

