from rest_framework.views import APIView
from common_app.utils import response, Error
from django.forms.models import model_to_dict
from common_app.utils import Pagination
from interface_app.models import Project, Module
from interface_app.serializers import ModuleSerializer


class ModuleView(APIView):
    authentication_classes = []

    def get(self, request, pk):
        """
        获得一个模块信息
        """
        print("/module/{}/".format(pk))
        try:
            module = Module.objects.get(id=pk)
            module_dict = model_to_dict(module)
        except Module.DoesNotExist:
            return response(error=Error.PROJECT_ID_NULL)
        return response(data=module_dict)

    def post(self, request, pk):
        """
        添加一个模块
        """
        print("/module/{}/".format(pk))
        print(type(request.data), request.data)
        name = request.data.get('name', "")
        describe = request.data.get('describe', "")
        project_id = request.data.get('projectId', "")
        project = Project.objects.get(id=project_id)
        module = Module.objects.create(name=name, describe=describe, project=project)
        module_dict = model_to_dict(module)
        return response(data=module_dict)

    def put(self, request, pk):
        """
        更新一个项目
        """
        name = request.data.get('name', "")
        describe = request.data.get('describe', "")
        project_id = request.data.get('projectId', True)
        try:
            module = Module.objects.get(id=pk)
            module.name = name
            module.describe = describe
            module.project_id = project_id
            module.save()
        except Module.DoesNotExist:
            return response(error=Error.MODULE_ID_NULL)
        return response()

    def delete(self, request, pk):
        """
        删除项目
        """
        try:
            module = Module.objects.get(id=pk)
            module.delete()
        except Module.DoesNotExist:
            return response(error=Error.MODULE_ID_NULL)
        return response()


class ModulesView(APIView):
    authentication_classes = []

    def get(self, request):
        """
        获得所有项目信息
        """
        print("/modules/")
        modules = Module.objects.all()
        pg = Pagination()
        page_module = pg.paginate_queryset(queryset=modules, request=request, view=self)
        ser = ModuleSerializer(instance=page_module, many=True)
        return response(data=ser.data)

