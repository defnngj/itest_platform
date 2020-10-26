
### Django表单处理

参考：https://docs.djangoproject.com/en/2.1/topics/forms/
参考：https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

1、创建表单 __forms.py__ 样例代码。

```python
from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(label='名称', max_length=100)
    describe = forms.CharField(label="描述", widget=forms.Textarea)

# 更多类型
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100) 
    message = forms.CharField(widget=forms.Textarea)  # 文本框
    sender = forms.EmailField()  # Email类型
    cc_myself = forms.BooleanField(required=False) # 布尔类型
```

2、视图 __views.py__ 样例代码。

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ProjectForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            # ... 
            Project.objects.create(name=name, describe=describe, status=status)
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'name.html', {'form': form})
```

3、模板 __xxx.html__ 样例代码。

```html
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}  <!--渲染整个表单-->
    {{ form.name }}  <!--渲染表单的一个字段-->
    <input type="submit" value="Submit">
</form>
```

* {{ form.as_table }} 将它们作为表单封装在```<tr>```标签中。
* {{ form.as_p }} 将它们封装在```<p>```标签中。
* {{ form.as_ul }} 将它们封装在```<li>```标签中。


4、更新数据（最简单的方法）

修改forms.py文件

```python
……
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']
        exclude = ['create_time']

```
* fields 表示显示的字段。
* exclude 表示屏蔽的表字段。

实现编辑项目视图：views.py 

```python
def edit_project(request, pid):

    if request.method == 'POST':
        # 更新数据
    else:
        if pid:
            p = Project.objects.get(id=pid)
            form = ProjectForm(instance=p)
        else:
            form = ProjectForm()

    return render(request, 'project_manage.html', {
        'form': form,
        "type": "edit",
    })
```
