## 制作docker镜像

1. 创建 `Dockerfile` 文件

```dockerfile
FROM python:3.6
#RUN wget -O /etc/apt/sources.list http://ubuntu9.com/topmirror/sourceslist/topfast
#COPY sources.list /etc/apt/
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/itest_platform
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
COPY . .
RUN mkdir /usr/src/erpv2
RUN mkdir /usr/src/erpv2/logs
EXPOSE 8000
CMD ["uwsgi", "--ini", "uwsgi.ini"]
```

2. 构建镜像

通过`docker build` 构建django镜像

```shell
$ docker build -f Dockerfile .
```

* -f 以指定文件系统中任何位置的`Dockerfile`。

3. 保存镜像

指定存储库和标记以保存新镜像。

```shell
$ docker build -t fnngj/django .
```

4. 查看镜像

```shell
$ docker images

REPOSITORY                           TAG                                              IMAGE ID            CREATED              SIZE
fnngj/django                         1.0                                              a36e36979657        About a minute ago   937MB
python                               3.6                                              170e243861ec        9 days ago           874MB
```

5. 创建容器

启动容器，并把容器的端口映射到主机的端口

```shell
$ docker run -d -p 8000:8000 fnngj/django:1.0
```

6. 查看容器

```shell
$ docker ps -a

CONTAINER ID        IMAGE                                 COMMAND                  CREATED             STATUS                     PORTS                                                                                                      NAMES
6f8b1b6f19e9        fnngj/django:1.0                      "uwsgi --ini uwsgi.i…"   23 seconds ago      Up 21 seconds              0.0.0.0:8000->8000/tcp
```

7. 访问系统

http://127.0.0.1:8000/

8. 进入容器

你可以看到容器中自己的django项目

```shell
$ sudo docker exec -it  6f8b1b6f19e9 /bin/bash

root@6f8b1b6f19e9:/usr/src/itest_platform# ls
Dockerfile  README.md  app_case  app_manage  app_personal  app_task  app_variable  db.sqlite3  doc  itest_platform  manage.py  requirements.txt  static  templates  uwsgi.ini
```

## 上传镜像

现在，我制作了一个镜像，如何像git项目一样上传到github仓库。

```shell
$ docker images

REPOSITORY                           TAG                                              IMAGE ID            CREATED              SIZE
fnngj/django                         1.0                                              a36e36979657        About a minute ago   937MB
```

1. 开通阿里云`容器镜像服务`

2. 登录

```shll
$ docker login --username=zhiheng5 registry.cn-hangzhou.aliyuncs.com
Password:   #这里输入密码
Login Succeeded
```

3. 创建镜像标签

```shell
$ docker tag fnngj/django:1.0  registry.cn-hangzhou.aliyuncs.com/zhiheng5/django:1.0

$ docker images

REPOSITORY                                          TAG                                              IMAGE ID            CREATED             SIZE
fnngj/django                                        1.0                                              a36e36979657        4 hours ago         937MB
registry.cn-hangzhou.aliyuncs.com/zhiheng5/django   1.0                                              a36e36979657        4 hours ago         937MB
```

4. 提交镜像

在提交镜像之前，先去阿里云创建命名空间。

```shell
$ docker push registry.cn-hangzhou.aliyuncs.com/zhiheng5/django:1.0

The push refers to repository [registry.cn-hangzhou.aliyuncs.com/zhiheng5/django]
bb1acec6c5d8: Pushed
3f781366c97d: Pushed
2c0815c15512: Pushed
909d64da1bb6: Pushed
0f945d2e38af: Pushed
027a03bdfb44: Pushed
e11d7c9c157f: Pushed
d3f91df4f2c2: Pushed
28c41b4dd660: Pushed
36957997ca7a: Pushed
5c4d527d6b3a: Pushed
a933681cf349: Pushed
f49d20b92dc8: Pushed
fe342cfe5c83: Pushed
630e4f1da707: Pushed
9780f6d83e45: Pushed
1.0: digest: sha256:67df4cc35ef5e5f3937f1c2a7af4f1cf477d959eddc21bb69c0340a43f1987ed size: 3680
```

5. 从Registry中拉取镜像

```shell
$ sudo docker pull registry.cn-hangzhou.aliyuncs.com/zhiheng5/django:1.0
```
