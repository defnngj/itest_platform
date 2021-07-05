from enum import Enum, unique
from rest_framework.response import Response


@unique
class Error(Enum):
    """
    子定义错误码 与 错误信息
    """
    USER_OR_PAWD_NULL = {'10010': '用户名密码为空'}
    USER_OR_PAWD_ERROR = {'10011': '用户名密码错误'}


def response(success: bool = True, error: Error = {}, data: any = []) -> Response:
    """
    自定义接口返回格式
    """
    if error == {}:
        error_code = ""
        error_msg = ""
    else:
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    resp = {
        "success": success,
        "error": {
            "code": error_code,
            "message": error_msg
        },
        "data": data
    }
    return Response(resp)
