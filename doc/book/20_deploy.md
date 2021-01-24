# 部署django

## admin静态文件

1.设置 `ROOT_STATIC`

```python
...
STATIC_URL = '/static/'

if DEBUG == True:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

2.拷贝admin静态文件

```shell
python .\manage.py collectstatic
```
静态目录会多一个`\static\admin\` 的目录

## wsgi 部署django

* WSGI: Python Web Server Gateway Interface

* uwsgi是一种通信协议，不过跟WSGI分属两种东西，该协议下速度比较快。

* uWSGI是一个Web Server，并且独占uwsgi协议，但是同时支持WSGI协议、HTTP协议等，它的功能是把HTTP协议转化成语言支持的网络协议供python使用。

1.安装uwsgi (uWSGI)
```shell script
sudo apt-get install libpcre3 libpcre3-dev
sudo python3 -m pip install uwsgi -i https://pypi.douban.com/simple
```

2.创建`uwsgi.ini`文件 

```ini
[uwsgi]

# Django-related settings

http = :8000

# the base directory (full path)
chdir = /usr/src/itest_platform

# Django s wsgi file
module = itest_platform.wsgi
# django static file 
static-map = /static=/usr/src/itest_platform/static

# process-related settings
# master
master = true

# maximum number of worker processes
processes = 4

# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum  = true
```

运行方式：
```shell script
> uwsgi -ini uwsgi.ini
```

请求 ---> uWSIG(http协议) --> django 

请求 ---> nginx(8099) --> uWSIG(socket协议8087) --> django 


## reids 安装

1.安装redis
```shell script
> sudo apt install redis-server
```
2.查看redis服务
```shell script
> ps -aux|grep redis

redis      15025  0.1  0.1  55864  4480 ?        Ssl  19:37   0:00 /usr/bin/redis-server 127.0.0.1:6379
fnngj      15706  0.0  0.0  11992   660 pts/2    S+   19:40   0:00 grep --color=auto redis
```
3.查看redis
```shell script
> redis-cli
127.0.0.1:6379> keys *
(empty list or set)
127.0.0.1:6379> exit
```

## nginx 配置

```shell script
sudo apt-get install nginx
```

访问nginx服务
http://127.0.0.1:80

nginx配置
创建`/etc/nginx/conf.d/default.conf`文件，配置如下：
```shell script
server {
    listen       8005;
    server_name  localhost;
    return 200 "This is 1\n";
}
```

nginx命令
```shell script
service nginx
Usage: nginx {start|stop|restart|reload|force-reload|status|configtest|rotate|upgrade}
```

django 服务配置：
```shell script
server {
    listen         8099;  重要
    server_name    127.0.0.1 
    charset UTF-8;
    access_log      /var/log/nginx/myweb_access.log;
    error_log       /var/log/nginx/myweb_error.log;

    client_max_body_size 75M;

    location / { 
        include uwsgi_params;  重要
        uwsgi_pass 127.0.0.1:8000;  重要
        uwsgi_read_timeout 2;
    }   
    location /static {
        expires 30d;
        autoindex on; 
        add_header Cache-Control private;
        alias /home/fnngj/pydj/myweb/static/;  重要
     }
 }
```

