from rest_framework import serializers
from interface_app.models import TestTask

from common_app.utils import BaseModelSerializer, BaseSerializer


class TaskSerializer(BaseModelSerializer):
    class Meta:
        model = TestTask
        fields = ["name", "describe", "cases"]
        ordering = ["id"]


class TaskValidators(BaseSerializer):
    name = serializers.CharField(required=True, error_messages={'required': 'name不能为空'})
    describe = serializers.CharField(required=False)
    cases = serializers.CharField(required=True, error_messages={'required': 'cases不能为空'})

    def create(self, validated_data):
        """
        创建任务
        """
        task = TestTask.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        """
        更新任务
        """
        instance.name = validated_data.get('name')
        instance.describe = validated_data.get('describe')
        instance.cases = validated_data.get('cases')
        instance.save()
        return instance
