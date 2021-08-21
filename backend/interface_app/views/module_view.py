from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from common_app.utils import response, Error, response_fail
from django.forms.models import model_to_dict
from common_app.utils import Pagination
from interface_app.models import Project, Module
from interface_app.serializers import ModuleSerializer, ModuleValidators


class ModuleView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        模块查询
        """
        pk = kwargs.get("pk")
        if pk is not None:
            print("/module/1/")
            try:
                module = Module.objects.get(id=pk, is_delete=False)
                module_dict = model_to_dict(module)
            except Module.DoesNotExist:
                return response(error=Error.PROJECT_ID_NULL)
            return response(data=module_dict)
        else:
            print("/module/?page=1&size=10")
            modules = Module.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_module = pg.paginate_queryset(queryset=modules, request=request, view=self)
            ser = ModuleSerializer(instance=page_module, many=True)
            data = {
                "total": modules.count(),
                "moduleList": ser.data,
            }
            return response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加一个模块
        """
        print("/module/{}/".format(kwargs))
        val = ModuleValidators(data=request.data)
        if val.is_valid() is False:
            return response_fail(val.errors)
        name = request.data.get('name')
        describe = request.data.get('describe')
        project_id = request.data.get('projectId')
        project = Project.objects.get(id=project_id)
        module = Module.objects.create(name=name, describe=describe, project=project)
        module_dict = model_to_dict(module)
        return response(data=module_dict)

    def put(self, request, pk):
        """
        更新一个项目
        """
        val = ModuleValidators(data=request.data)
        if val.is_valid() is False:
            return response_fail(val.errors)

        try:
            module = Module.objects.get(id=pk, is_delete=False)
            module.name = request.data.get('name')
            module.describe = request.data.get('describe')
            module.project_id = request.data.get('projectId')
            module.save()
        except Module.DoesNotExist:
            print("aaa", type(Error.MODULE_ID_NULL), Error.MODULE_ID_NULL)
            return response(error=Error.MODULE_ID_NULL)
        return response()

    def delete(self, request, pk):
        """
        删除项目
        """
        try:
            Module.objects.get(id=pk, is_delete=False).update(is_delete=True)
        except Module.DoesNotExist:
            return response(error=Error.MODULE_ID_NULL)
        return response()


# class ModulesView(ListAPIView):
#     authentication_classes = []
#
#     def list(self, request, *args, **kwargs):
#         queryset = Module.objects.all()
#
#         pg = Pagination()
#         page_module = pg.paginate_queryset(queryset=queryset, request=request, view=self)
#         ser = ModuleSerializer(instance=page_module, many=True)
#         return response(data=ser.data)


# class ModulesView(APIView):
#     authentication_classes = []
#
#     def get(self, request):
#         """
#         获得所有项目信息
#         """
#         print("/modules/")
#         modules = Module.objects.all()
#         pg = Pagination()
#         page_module = pg.paginate_queryset(queryset=modules, request=request, view=self)
#         ser = ModuleSerializer(instance=page_module, many=True)
#         return response(data=ser.data)
#
