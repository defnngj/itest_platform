import time
from datetime import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from backend import settings


class TokenAuthentication(BaseAuthentication):
    """
    自定义基于token的认证
    """

    def authenticate(self, request):
        # 1. 在请求头的query_params中获取token
        # token = request.query_params.get('token')

        # 2. 直接在请求头中获取token
        header_token = request.META.get("HTTP_TOKEN", "")

        if header_token == "":
            raise exceptions.AuthenticationFailed("token为空")

        token = Token.objects.filter(key=header_token).first()
        if not token:
            raise exceptions.AuthenticationFailed("token认证失败")

        utc_now = datetime.utcnow()
        now_timestamp = time.mktime(utc_now.timetuple())
        created_timestamp = time.mktime(token.created.timetuple())
        if (now_timestamp - created_timestamp) > settings.TOKEN_TIME:
            raise exceptions.AuthenticationFailed('token认证过期')

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass
