from rest_framework import serializers


class Base:
    field_mappings = ()

    def init_mapping(self):
        for (field_name, data_key) in getattr(self, 'field_mappings', []):
            if field_name in self.fields:
                self.fields[data_key] = self.fields[field_name]
                del self.fields[field_name]

    def get_local_data(self):
        """
        前端 --> 后端，在参数校验的时候，获取的经过转换后的数据
        :return:
        """
        data = dict(self.data)

        for (field_name, data_key) in getattr(self, 'field_mappings', []):
            if data_key in data:
                data[field_name] = data.get(data_key, None)
                del data[data_key]
        return data

    def get_mapping_data(self):
        """
        后端  -->  前端，获取的经过转换后的数据
        :return:
        """
        return dict(self.data)


class BaseSerializer(serializers.Serializer, Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_mapping()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BaseModelSerializer(serializers.ModelSerializer, Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_mapping()
