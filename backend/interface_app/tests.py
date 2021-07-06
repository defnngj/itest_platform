from random import randint

import requests

for i in range(20):
    data = {
        "name": "接口项目"+str(i),
        "describe": "描述信息"+str(i),
        "status": True
    }
    r = requests.post("http://127.0.0.1:8000/api/interface/v1/project/0/", json=data)
    print(r.json())


for i in range(20):
    data = {
        "name": "接口模块"+str(i),
        "describe": "描述信息"+str(i),
        "projectId": randint(1, 20)
    }
    r = requests.post("http://127.0.0.1:8000/api/interface/v1/module/0/", json=data)
    print(r.json())
