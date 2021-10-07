from rest_framework import serializers
from interface_app.models import Project


class ProjectQuerySerializer(serializers.ModelSerializer):
    """
    用于项目查询序列化
    """
    class Meta:
        model = Project
        fields = ["id", "name", "describe", "status", "create_time", "update_time"]


class ProjectSaveSerializer(serializers.Serializer):
    """
    用于项目创建&更新序列化
    """
    name = serializers.CharField(required=True, error_messages={'required': '项目名称必填'})
    describe = serializers.CharField(required=False, default="")
    status = serializers.BooleanField(required=False, default=True)

    def create(self, validated_data):
        return Project(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
