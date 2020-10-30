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