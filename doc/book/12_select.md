
#### 二级联动菜单的实现

看似一个简单的功能，做起来却花费了我们不少时间，这里做个总结。


引用 select2 样式库
官方文档：https://select2.org/


要实现 二级联动菜单的 HTML 代码。

```html
<label>项目：</label>
<select class="form-control select2-single" id="selectProject">
</select>

<label>模块：</label>
<select class="form-control select2-single" id="selectModule">
</select>

...

<link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/css/select2.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/js/select2.min.js"></script>

<script type="text/javascript">
	//调用二级联动菜单初始方法
	 SelectInit();

</script>
```

首先，准备好后端接口: views.py 

```python
from module_app.models import Module
from project_app.models import Project


def get_select_data(request):
    """
    获取 "项目>模块" 列表
    :param request:
    :return: 项目接口列表
    """
    if request.method == "GET":
        project_list = Project.objects.all()
        data_list = []
        for project in project_list:
            project_dict = {
                "id": project.id,
                "name": project.name
            }

            module_list = Module.objects.filter(project_id=project.id)
            module_name = []
            for module in module_list:
                module_name.append({
                    "id": module.id,
                    "name": module.name,
                })

            project_dict["moduleList"] = module_name
            data_list.append(project_dict)

        return JsonResponse({"status": 10200, "message": "success", "data": data_list})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})

```

接口返回的结果如下：

```json

{
    "status": 10200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "测试平台",
            "moduleList": [
                {
                    "id": 1,
                    "name": "模块1"
                }
            ]
        },
        {
            "id": 2,
            "name": "新项目BBB",
            "moduleList": [
                {
                    "id": 4,
                    "name": "模块AA"
                },
                {
                    "id": 5,
                    "name": "模块BB"
                }
            ]
        },
        {
            "id": 3,
            "name": "旧平台AAA",
            "moduleList": [
                {
                    "id": 2,
                    "name": "模块001"
                },
                {
                    "id": 3,
                    "name": "模块002"
                }
            ]
        }
    ]
}
```

注意看 ```data``` 的数据结构，接下来使用js 解析。


```js

//初始化 “项目>模块” 二级联动菜单
var SelectInit = function (defaultProjectId, defaultModuleId) {
    var cmbProject = document.getElementById("selectProject");
    var cmbModule = document.getElementById("selectModule");
    var dataList = [];

    //设置默认选项
    function setDefaultOption(obj, id) {
        for (var i = 0; i < obj.options.length; i++) {
            if (obj.options[i].value == id) {
                obj.selectedIndex = i;
                return;
            }
        }
    }

    //创建下拉选项
    function addOption(cmb, obj) {
        var option = document.createElement("option");
        cmb.options.add(option);
        option.innerHTML = obj.name;
        option.value = obj.id;
    }

    //改变项目
    function changeProject() {
        cmbModule.options.length = 0;
        if (cmbProject.selectedIndex == -1) {
            return;
        }
        var pid = cmbProject.options[cmbProject.selectedIndex].value;
        for (let i = 0; i < dataList.length; i++) {
            if(dataList[i].id == pid) {
                let modules = dataList[i].moduleList;
                for(let j=0; j< modules.length; j++){
                    addOption(cmbModule, modules[j]);
                }
            }
        }

        setDefaultOption(cmbModule, defaultModuleId);
    }

    function getSelectData() {
        // 调用获取select数据列表
        $.get("/testcase/get_select_data", {}, function (resp) {
            if (resp.status === 10200) {
                dataList = resp.data;
                //遍历项目
                for (var i = 0; i < dataList.length; i++) {
                    addOption(cmbProject, dataList[i]);
                }

                setDefaultOption(cmbProject, defaultProjectId);
                changeProject();
                cmbProject.onchange = changeProject;
            }

            setDefaultOption(cmbProject, defaultProjectId);

        });
    }

    // 调用getSelectData函数
    getSelectData();

};

```