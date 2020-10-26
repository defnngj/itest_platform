
#### django 分页器

django 提供了 ``` Paginator ``` 类来实现分页功能。

在 ```views.py``` 文件中的使用如下.
```python
from django.core.paginator import Paginator  
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def testcase_manage(request):
    """ 用例列表"""
    case_list = TestCase.objects.all()
    # 将数据做分页处理，每一页显示 3 条
    p = Paginator(case_list, 10)
    # 通过请求得到要第几页的数据
    page = request.GET.get('page')
    try:
        cases = p.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        cases = p.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        cases = p.page(p.num_pages)

    return render(request, "case_list.html", {"cases": cases})

```

然后，在 ```case_list.html``` 文件中的使用如下：

```html
<!-- 分页器 -->
<div>
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <li>
                {% if cases.has_previous %}
                    <a href="?page={{ cases.previous_page_number }}" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                {% endif %}
            </li>

            <li><a href="#">{{ cases.number }}</a></li>

            {% if cases.has_next %}
                <li>
                    <a href="?page={{ cases.next_page_number }}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            {% endif %}

            <li><a href="#">共：{{ cases.paginator.num_pages }} 页</a></li>

        </ul>
    </nav>
</div>

```

API说明：

* has_previous 是否有上一页（布尔类型True/False）
* previous_page_number  上一页的页数（整型）
* number 当前页的页数（整型）
* has_next  是否有下一页（布尔类型True/False）
* next_page_number 下一页的页数（整型）
* paginator.num_pages 总共有几页（整型）