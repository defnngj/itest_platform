from rest_framework.serializers import ModelSerializer
from interface_app.models import Module


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name", "project"]
        ordering = ["id"]
