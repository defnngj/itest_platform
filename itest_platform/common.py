from django.http import JsonResponse


def response(status=None, message=None, data=[]):
    """通用的接口返回"""
    if status is None:
        status = 10200
    if message is None:
        message = "成功"

    return JsonResponse({"status": status, "message": message, "data": data})
