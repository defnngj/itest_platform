from rest_framework import serializers
from interface_app.models import TestCase
from common_app.utils import BaseModelSerializer, BaseSerializer
from rest_framework.validators import UniqueTogetherValidator


class CaseData:
    methods = ["POST", "GET", "DELETE", "PUT"]
    params_type = ["params", "data", "json"]
    assert_type = ["include", "equal"]


class CaseSerializer(BaseModelSerializer):
    class Meta:
        model = TestCase
        fields = ["url", "method", 'header', "params_type", "params_body", "result",
                  "assert_type", "assert_text", "module_id", "name"]
        ordering = ["id"]

    field_mappings = (
        ("parameter_type", "parameterType"),
        ("parameter_body", "parameterBody"),
        ("assert_type", "assertType"),
        ("assert_text", "assertText"),
        ("module_id", "moduleId"),
    )


class CaseValidators(serializers.Serializer):
    name = serializers.CharField(required=True, error_messages={'required': 'name必须填写'})
    url = serializers.CharField(required=True,
                                error_messages={'required': 'URL不能为空'})
    method = serializers.ChoiceField(required=True,
                                     choices=CaseData.methods,
                                     error_messages={'required': 'method不能为空'})
    header = serializers.CharField(required=False)
    params_type = serializers.ChoiceField(required=True,
                                          choices=CaseData.params_type,
                                          error_messages={'required': 'params_type不能为空'})
    params_body = serializers.CharField(required=False)
    result = serializers.CharField(required=False)
    assert_type = serializers.ChoiceField(required=False, choices=CaseData.assert_type)
    assert_text = serializers.CharField(required=False)
    module_id = serializers.IntegerField(required=True, error_messages={'required': 'module_id必须填写'})

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


class DebugValidators(serializers.Serializer):
    """
    用例调验证器
    """
    url = serializers.CharField(required=True,
                                error_messages={'required': 'URL不能为空'})
    method = serializers.ChoiceField(required=True,
                                     choices=CaseData.methods,
                                     error_messages={'required': 'method不能为空'})
    header = serializers.JSONField(required=True)
    params_type = serializers.ChoiceField(required=True,
                                          choices=CaseData.params_type,
                                          error_messages={'required': 'params_type不能为空'})
    params_body = serializers.JSONField(required=True)


class AssertValidators(serializers.Serializer):
    """
    断言验证器
    """
    result = serializers.CharField(required=True, error_messages={'required': '结果不能为空'})
    assert_type = serializers.ChoiceField(required=True,
                                     choices=CaseData.assert_type,
                                     error_messages={'required': 'method不能为空'})
    assert_text = serializers.CharField(required=True, error_messages={'required': '断言不能为空'})


