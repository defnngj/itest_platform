from django.contrib.auth.models import User, Group
from django.contrib import auth
from rest_framework.authtoken.models import Token
from common_app.utils import BaseAPIView
from common_app.serializers import UserSerializer, GroupSerializer
from common_app.utils import TokenAuthentication


class TestView(BaseAPIView):
    # 因为setting设置了全局认证，这个视图把认证去掉
    authentication_classes = []

    def get(self, request):
        return self.response()


class LoginView(BaseAPIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def post(self, request):
        """
        登录账号，并获取token
        """
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == '' or login_password == '':
            return self.response(error=self.USER_OR_PAWD_NULL)
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None and user.is_active:
                auth.login(request, user)  # 验证登录
                # update the token
                token = Token.objects.filter(user=user)
                token.delete()
                token = Token.objects.create(user=user)
                return self.response(data={"Token": str(token)})
            else:
                return self.response(error=self.USER_OR_PAWD_ERROR)

    def delete(self, request):
        """
        退出账号，并删除token
        """
        userId = request.POST.get("user")
        token = Token.objects.filter(user=userId)
        token.delete()
        return self.response()


class UserView(BaseAPIView):
    # 设置了全局认证，默认该接口调用需要传token
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        print(request.method)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return self.response(data=serializer.data)


class GroupView(BaseAPIView):
    # 设置了全局认证，默认该接口调用需要传token
    # authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True, context={'request': request})
        return self.response(data=serializer.data)
