
### Django测试

* 单元测试？

* 接口测试？

* UI测试？

参考：https://docs.djangoproject.com/en/2.1/topics/testing/overview/
https://docs.djangoproject.com/en/2.1/topics/testing/tools/

针对django的```MTV```开发模式，django给我们提供了不同的测试方案。

#### django模型（models.py）测试

__示例:__

```python
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')

```

验证模型层的增、修改、删除、查询等。

#### django单元/接口（views.py）测试

__示例:__

```python
import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/customer/details/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['customers']), 5)

```

* django提供的有 ```Client()``` 来模拟发送HTTP请求。

* 从形式上看，更像是接口测试，但它又全面验证了viesw.py中的代码逻辑。所以，也可以认为是单元测试。

* views.py 是离不开 models.py 的，比如要获取项目管理列表，所以，多数时候还需要初始化创建测试数据。

#### django UI（templates/）测试

__示例:__

```python
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

```

* UI自动化测试当然是交给selenium来完成，不过Django给我们提供了一些封装，使我们测试django的UI时更加方便。

#### 运行测试粒度

```shell
# Run all the test in porject
$ ./manage.py test

# Run all the tests found within the 'animals' package
$ ./manage.py test animals

# Run all the tests in the animals.tests module
$ ./manage.py test animals.tests

# Run just one test case
$ ./manage.py test animals.tests.AnimalTestCase

# Run just one test method
$ ./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak
```
