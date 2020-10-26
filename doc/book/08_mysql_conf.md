

#### MySQL的配置

参考：https://docs.djangoproject.com/en/2.1/ref/databases/


1、先有一个MySQL数据库, 可以单独安装，为了方便也可以使用WampServer集成环境。

2、在项目根目录创建一个配置文件my.cnf文件。

```
[client]
host = 127.0.0.1
port = 3306
user = root
password = pyif07
database = test_dev
default-character-set = utf8
```

3、 settings.py添加配置：

```python
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR + '/my.cnf',
        },
    }
}
```

4、 安装mysqlclient

```
$ pip install mysqlclient
```

5、重新执行数据库迁移和创建超级管理账号

```
python manage.py migrate

python manage.py createsuperuser

```



