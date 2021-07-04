## FBV vs CBV

* FBV（function base views） 就是在视图里使用函数处理请求。


* CBV（class base views） 就是在视图里使用类处理请求。

### FBV demo

* view.py

```py
from django.http import HttpResponse
  
def my_view(request):
     if request.method == 'GET':
            return HttpResponse('OK')
```

* urls.py

```py
from xx import  view
path("test/", view.my_view)
```

### CBV demo

* view.py

```py
from django.http import HttpResponse
from django.views import View
  
class MyView(View):

      def get(self, request):
            return HttpResponse('OK')
```

* urls.py

```py
from xx import  view
path("test/", view.MyView.as_view())
```
