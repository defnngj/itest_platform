from rest_framework import serializers
from interface_app.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectValidators(serializers.Serializer):
    name = serializers.CharField(required=True)
    describe = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)
