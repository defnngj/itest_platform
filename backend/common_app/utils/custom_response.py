from rest_framework.response import Response


class Error:
    """
    子定义错误码与错误信息
    """
    USER_OR_PAWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}

    PROJECT_ID_NULL = {"10020": "项目id不存在"}
    PROJECT_OBJECT_NULL = {"10021": "通过id查询项目不存在"}
    MODULE_ID_NULL = {"10030": "模块id不存在"}
    CASE_ID_NULL = {"10040": "用例id不存在"}
    CASE_OBJECT_NULL = {"10041": "通过id查询用例不存在"}


def response_fail(error=""):
    """
    返回失败, 主要用于参数验证失败
    """
    error_msg = {
        "30010": str(error)
    }
    return response(success=False, error=error_msg, data=[])


def response(success: bool = True, error={}, data: any = []) -> Response:
    """
    自定义接口返回格式
    """
    if error == {}:
        error_code = ""
        error_msg = ""
    else:
        success = False
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
