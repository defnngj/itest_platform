from rest_framework import serializers
from interface_app.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name", 'describe', "project"]
        ordering = ["id"]


class ModuleValidators(serializers.Serializer):
    name = serializers.CharField(required=True)
    describe = serializers.CharField(required=False)
    projectId = serializers.IntegerField(required=True)
