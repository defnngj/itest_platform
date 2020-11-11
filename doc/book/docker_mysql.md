# 通过docker 安装mysql

登录docker hub:
https://hub.docker.com/_/mysql?tab=tags

根据自己的需求找到对应的 mysql 版本, 通过`docker pull`命令下载。

```shell
docker pull mysql:5.7
5.7: Pulling from library/mysql
bb79b6b2107f: Pull complete
49e22f6fb9f7: Pull complete
842b1255668c: Pull complete
9f48d1f43000: Pull complete
c693f0615bce: Pull complete
8a621b9dbed2: Pull complete
0807d32aef13: Pull complete
f15d42f48bd9: Pull complete
098ceecc0c8d: Pull complete
b6fead9737bc: Pull complete
351d223d3d76: Pull complete
Digest: sha256:4d2b34e99c14edb99cdd95ddad4d9aa7ea3f2c4405ff0c3509a29dc40bcb10ef
Status: Downloaded newer image for mysql:5.7
docker.io/library/mysql:5.7
```

启动容器

```shell
docker run -p 3309:3306 --restart=always --privileged=true --name mysql -v /Users/tech/tools/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD="klook101" -d mysql:5.7
```

* `3309` 本地端口，保证本地该端口没有被其他应用占用，映射到 容器里面的mysql的默认端口`3306`。

* `/Users/tech/tools/mysql` 本地mysql 数据存储路径。

* `klook101` mysql 登录密码， 用户名默认 `root`。

创建数据：

通过客户端登录Mysql容器，查看数据库。
