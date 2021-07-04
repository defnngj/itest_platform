from enum import Enum, unique
from rest_framework.response import Response


@unique
class Error(Enum):
    """
    子定义错误码 与 错误信息
    """
    USER_OR_PAWD_NULL = {'10010': '用户名密码为空'}
    USER_OR_PAWD_ERROR = {'10010': '用户名密码错误'}


def response(success=True, error={}, data=[]) -> Response:
    """
    自定义错误返回格式
    """
    if error != {}:
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]
    else:
        error_code = ""
        error_msg = ""

    resp = {
        "success": success,
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "data": data
    }
    return Response(resp)
