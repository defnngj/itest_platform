

#### ztree 的使用

官方网站：http://www.treejs.cn/v3/api.php

首先，前端主要代码如下。

```html

...
        <div>
            <p>用例：</p>
            <ul id="treeDemo" class="ztree"></ul>
        </div>
...

<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
<link href="http://cdn.bootcss.com/zTree.v3/3.5.23/css/zTreeStyle/zTreeStyle.css" rel="stylesheet">
<script src="http://cdn.bootcss.com/zTree.v3/3.5.23/js/jquery.ztree.all.js"></script>

<script type="text/javascript">

    var zTreeObj;

    // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
    var setting = {
        check: {
            enable: true,
            chkStyle: "checkbox"
        }
    };


    $(document).ready(function () {
        // 调用获取用例树
        $.get("/testtask/get_case_tree", {}, function (resp) {
            if (resp.status === 10200) {
                var zNodes = resp.data;
                zTreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
                zTreeObj.expandAll(true);  //设置默认展开
            }

        });

    });


</script>

```

其次，后端返回接口代码：

```python

def get_case_tree(request):
    """
    获得用例树形结构
    """
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }

                cases = TestCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    case_dict = {
                        "name": case.name,
                        "isParent": False,
                        "id": case.id,
                    }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)

        return JsonResponse({"status": 10200, "message": "success", "data": data_list})

```

接口返回数据格式：

```json

{
    "status": 10200,
    "message": "success",
    "data": [
        {
            "name": "测试平台",
            "isParent": true,
            "children": [
                {
                    "name": "模块1",
                    "isParent": true,
                    "children": [
                        {
                            "name": "简单的POST接口",
                            "isParent": false,
                            "id": 3
                        },
                        {
                            "name": "测试平台  》》 模块 1",
                            "isParent": false,
                            "id": 10
                        }
                    ]
                }
            ]
        },
        {
            "name": "新项目BBB",
            "isParent": true,
            "children": [
                {
                    "name": "模块AA",
                    "isParent": true,
                    "children": [
                        {
                            "name": "get 测试用例",
                            "isParent": false,
                            "id": 1
                        }
                    ]
                },
                {
                    "name": "模块BB",
                    "isParent": true,
                    "children": [
                        {
                            "name": "新项目BBB>> 模块BBB",
                            "isParent": false,
                            "id": 6
                        }
                    ]
                }
            ]
        },

    ]
}
```
