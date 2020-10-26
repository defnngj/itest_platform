
#### 测试任务的执行

测试任务的执行比较复杂，整体思路如下。

1、使用 ```unittest``` 实现用例的执行，以及结果的统计。

2、```ddt``` 基于unittest单元测试框架的数据驱动库，方便读取JOSN文件。
https://github.com/datadriventests/ddt

3、 ```xmlrunner``` 执行 unittest 测试用例并生成 XML 格式的报告。
https://github.com/xmlrunner/unittest-xml-reporting

4、```Requests``` 实现接口的调用。
https://github.com/kennethreitz/requests


* JSON 数据文件如下：

```JSON
{
    "3": {
        "url": "http://httpbin.org/post",
        "method": "post",
        "header": "{}",
        "parameter_type": "from",
        "parameter_body": "{'key':'value'}",
        "assert_type": "contains",
        "assert_text": "113.89.239.241"
    },
    "10": {
        "url": "https://api.github.com/events",
        "method": "get",
        "header": "{}",
        "parameter_type": "from",
        "parameter_body": "{}",
        "assert_type": "contains",
        "assert_text": "github"
    }
}
```

* 运行代码如下：

```python

……

@ddt
class InterfaceTest(unittest.TestCase):

    @unpack
    @file_data("test_data_list.json")
    def test_run_cases(self, url, method, header, parameter_type, parameter_body, assert_type, assert_text):

        if header == "{}":
            header_dict = {}
        else:
            header_dict = json.loads(header.replace("\'", "\""))

        if parameter_body == "{}":
            parameter_dict = {}
        else:
            parameter_dict = json.loads(parameter_body.replace("\'", "\""))

        if method == "get":
            if parameter_type == "from":
                r = requests.get(url, headers=header_dict, params=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_text, r.text)
                else:
                    self.assertEqual(assert_text, r.text)

        if method == "post":
            if parameter_type == "from":
                r = requests.post(url, headers=header_dict, data=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_text, r.text)
                else:
                    self.assertEqual(assert_text, r.text)

            elif parameter_type == "json":
                r = requests.post(url, headers=header_dict, json=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_text, r.text)
                else:
                    self.assertEqual(assert_text, r.text)
            else:
                raise NameError("参数类型错误")


# 运行测试用例
def run_cases():
    with open(EXTEND_DIR + 'results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False
        )


if __name__ == '__main__':
    run_cases()

```
