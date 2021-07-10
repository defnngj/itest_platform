## FBV vs CBV

* FBV（function base views） 就是在视图里使用函数处理请求。


* CBV（class base views） 就是在视图里使用类处理请求。

### FBV demo

* view.py

```py
from django.http import HttpResponse
from rest_framework.decorators import api_view

def my_view(request):
     if request.method == 'GET':
            return HttpResponse('OK')

@api_view(['GET'])
def rf_view(request, format=None):
     if request.method == 'GET':
            return HttpResponse('OK')

```

* urls.py

```py
from xx import  view
path("test/", view.my_view)
path("test2/", view.rf_view)
```

### CBV demo

* view.py

```py
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response


class MyView(View):

      def get(self, request):
            return HttpResponse('OK')


class RFView(APIView):

      def get(self, request, format=None):
            return Response({"success":'OK'})

```

* urls.py

```py
from xx import  view
path("test/", view.MyView.as_view())
path("test/", view.RFView.as_view())
```
