
#### 通过Ajax实现接口调用

1、页面HTML代码
```HTML
<input type="text" id="number1">+
<input type="text" id="number2">
<button type="button" onclick="myFunction()">&nbsp;&nbsp;=&nbsp;&nbsp; </button>
<textarea rows="3" cols="20" id="result">
```
这里没有用到```form```表单。 通过onclick绑定```myFunction()```方法。

2、页面中插入JS代码
```js
<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>

<script type="text/javascript">
    function myFunction()
    {
        let number1 = document.querySelector("#number1").value;
        let number2 = document.querySelector("#number2").value;
        console.log("数字1", number1);
        console.log("数字2", number2);

        if(number1 === ""){
            document.querySelector("#number1").style.border = "2px solid red";
            return;
        }else{
            document.querySelector("#number1").style.border = "";
        }
        if (number2 === "") {
            document.querySelector("#number2").style.border = "2px solid red";
            return;
        }else{
            document.querySelector("#number2").style.border = "";
        }
        
        $.post("/js_jisuan/",
         { num1: number1, num2: number2},
         function (result) {
            //alert("结果: "+ result);
            if(result.status_code !== 10200){
                document.querySelector("#result").value = result.message;    
            } else {
                document.querySelector("#result").value = result.data;
            }
        });

    }

</script>
```
实现 myFunction() 方法，通过 ```$.post()``` 调用后端接口。

3、使用django实现接口
```python
from django.http import JsonResponse

def js_jisuan(request):
    if request.method == "POST":
        n1 = request.POST.get("num1", "")
        n2 = request.POST.get("num2", "")
        if n1 == "" or n2 == "":
            return JsonResponse({"status_code": 10011,"message": "参数不能为空"})
        try:
            n1 = int(n1)
            n2 = int(n2)
        except ValueError:
            return JsonResponse({"status_code": 10012,"message": "参数类型错误"})

        return JsonResponse({"status_code": 10200,"message": "成功","data": n1+n2})
    else:
        return JsonResponse({"status_code": 10010,"message": "请求方法错误"})
```
使用 ```JsonResponse()``` 反回json对象。



