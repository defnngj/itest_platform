from rest_framework.serializers import  ModelSerializer
from interface_app.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
