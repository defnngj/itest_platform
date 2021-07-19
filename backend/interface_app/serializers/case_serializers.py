from rest_framework import serializers
from interface_app.models import TestCase


class CaseData:
    methods = ["POST", "GET", "DELETE", "PUT"]


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["id", "name", 'describe', "project"]
        ordering = ["id"]


class CaseValidators(serializers.Serializer):
    url = serializers.CharField(required=True, error_messages={'required': 'URL不能为空'})
    method = serializers.IntegerField(required=True, error_messages={'required': 'method不能为空'})
    header = serializers.CharField(required=False)
    parameter_type = serializers.CharField(required=True, error_messages={'required': 'method不能为空'})
    parameter_body = serializers.CharField(required=True, error_messages={'required': 'parameter_body请填写名字'})
    result_text = serializers.CharField(required=False)
    assert_type = serializers.CharField(required=True, error_messages={'required': 'assert_type必须填写'})
    assert_text = serializers.CharField(required=True, error_messages={'required': 'assert_text必须填写'})
    module_id = serializers.IntegerField(required=True, error_messages={'required': 'module_id必须填写'})
    name = serializers.CharField(required=True, error_messages={'required': 'name必须填写'})

    def create(self, validated_data):
        """
        创建用例
        """
        case = TestCase.objects.create(**validated_data)
        return case

    def update(self, instance, validated_data):
        """
        更新用例
        """
        instance.url = validated_data.get('url')
        instance.method = validated_data.get('method')
        instance.parameter_type = validated_data.get('parameter_type')
        instance.parameter_body = validated_data.get('parameter_body')
        instance.result_text = validated_data.get('result_text')
        instance.assert_type = validated_data.get('assert_type')
        instance.assert_text = validated_data.get('assert_text')
        instance.module_id = validated_data.get('module_id')
        instance.name = validated_data.get('name')
        instance.save()
        return instance
