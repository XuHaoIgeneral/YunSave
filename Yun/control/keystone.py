# -*- coding: UTF-8 -*-
from swiftclient import client as swiftclient
from keystoneclient.v3 import client as lient
import json

def get_keystone_conn():
    conn = lient.Client(
        user_domain_name='default',
        username='admin',
        password='123',
        project_domain_name='default',
        project_name='admin',
        auth_url='http://192.168.10.55:35357/v3/'
        )
    return conn


# 连接配置
def con(username,password):
    _authurl = 'http://127.0.0.1:5000/v3/'
    _auth_version = '3'
    print username
    print password
    _user = username
    _key = password

    _os_options = {
        'user_domain_name': 'default',
        'project_domain_name': 'default',
        'project_name': 'admin'
    }

    try:
        conn = swiftclient.Connection(
            authurl=_authurl,
            user=_user,
            key=_key,
            os_options=_os_options,
            auth_version=_auth_version
        )

    except Exception as e:
        conn = "error"

    return conn

def list_container(username,password):
    conn = con(username,password)
    resp_headers, containers = conn.get_account()
    ret=[]
    for container in containers:
        ret.append(container)
    for i in range(len(ret)):
        ret[i]["id"]=i+1
    return ret

#容器详细信息
def inf_container(container_name,username,password):
    conn = con(username,password)
    container_inf=[]
    # for i in container_name:
    test=conn.get_container(container_name)
    for i in test:
        container_inf.append(i)
    container_inf=container_inf[1]
    for i in range(len(container_inf)):
        container_inf[i]["id"]=i+1
    return container_inf

# 创建容器
def create_container(container_name_c,username,password):
    conn = con(username,password)
    resp_headers, containers = conn.get_account()
    ret = []
    #获取已经存在的容器名
    for container in containers:
        u=container.items()
        ret.append(u[2][1])
    # 对可能重复的容器名进行判断
    state = True
    for i in ret:
        if container_name_c==i:
            state=False
            break

    # 如果容器名在swift中已经存在 返回false
    if state==False:
        return False
    else:
        try:
            conn.put_container(container_name_c)
            return True
        except:
            return False

#删除容器
def del_container(container_name_d,username,password):
    conn = con(username,password)
    try:
        print "test del_container"
        conn.delete_container(container_name_d)
        print "secc del_container"
        return True
    except:
        return False

#获取对象元数据  容器名+对象名
def object_metadata(container_name, objec_name,username,password):
    conn = con(username,password)
    object_inf = []
    test = conn.head_object(container_name, objec_name)
    for i in test:
        object_inf.append(i)
    return test


# 上传文件
def object_upload(container_name,object_name,path,username,password):
    conn=con(username,password)
    try:
        with open(path,'rb') as local:
            conn.put_object(container_name
                            ,object_name
                            ,contents=local
                            # ,content_type='text/plain'
                            )
        return True
    except:
        return False

# 下载文件
def object_download(container_name,object_name,username,password):
    conn=con(username,password)
    try:
        resp_headers, obj_contents = conn.get_object(container_name, object_name)
        return obj_contents
    except:
        return False


# 删除对象 传入容器名和对象
def del_object(container_name,object_name,username,password):
    conn = con(username,password)
    try:
        print container_name
        print type(container_name)
        conn.delete_object(container_name,object_name)
        return True
    except:
        return False

# 获取文件内容
def get_object(container_name,object_name,username,password):
    conn = con(username,password)
    test=conn.get_object(container_name, object_name)
    return test[1]

