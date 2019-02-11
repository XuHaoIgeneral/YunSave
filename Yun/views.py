# -*- coding: UTF-8 -*-
from django.shortcuts import render
from swiftclient import client as swiftclient
from keystoneclient.v3 import client as lient
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template.loader import get_template
from Yun.models import USER
import os
from Yun.control import sessionJudge,keystone
import json
from django.http import StreamingHttpResponse

# Create your views here.

# 主页面
def Index(request):
    #身份验证
    try:
        session_user = request.session['user']
        session_passwd=request.session['passwd']
    except:
        session_user = None
        session_passwd = None
    # 判断是否是用户登录状态
    if session_user is not None:
        userstate = sessionJudge.userJudge(session_user)
    else:
        userstate = False
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)
    
    # 如果初始化为GET请求
    if request.method=="GET" and userstate==True:
        #
        containnerlist=keystone.list_container(session_user,session_passwd)
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'
                                        , 'index.html'), {
                                                            'containnerlist':containnerlist,
                                                          'login_user': session_user,
                                                          })

    elif request.method=="POST" and userstate==True:
        actice=request.POST['actice']
        if actice == "delete":
            try:
                container_name = request.POST['container_name']
                container_name = str(container_name)
                print "aa"
                print container_name
                print "aa"
                state = keystone.del_container(container_name,session_user,session_passwd)
                print state
                if state == True:
                    return HttpResponse(json.dumps({
                        'state': 1,
                    }))
                else:
                    return HttpResponse(json.dumps({
                        'state': 0,
                    }))
            except:
                return HttpResponse(json.dumps({
                    'state': 2,
                }))


# 列表显示容器下对象
def Object(request):

    try:
        session_user = request.session['user']
        session_passwd = request.session['passwd']
    except:
        session_user = None
        session_passwd = None
    # 判断是否是用户登录状态7
    print session_user
    if session_user is not None:
        userstate = sessionJudge.userJudge(session_user)
    else:
        userstate = False
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)

    if request.method == "GET" and userstate == True:
        container_name=request.GET['containner']
        object_list=keystone.inf_container(container_name,session_user,session_passwd)

        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'

                                            , 'object.html'), {"object_list":object_list,
                                                               'login_user': session_user,
                                                               'container_name':container_name,

                      })

    elif request.method == "POST" and userstate == True:
        behavior=str(request.POST['actice'])
        print behavior
        if behavior=="show":
            try:
                container_name = request.POST['container_name']
                container_name = str(container_name)
                object_name = request.POST['object_name']
                object_name = str(object_name)
                try:
                    show = keystone.get_object(container_name, object_name,session_user,session_passwd)
                    return HttpResponse(json.dumps({
                        'show': show,
                    }))
                except:
                    return HttpResponse(json.dumps({
                        'show': "error",
                    }))
            except:
                pass
        elif behavior=="delete":
            try:
                container_name = request.POST['container_name']
                container_name=str(container_name)
                object_name=request.POST['object_name']
                object_name=str(object_name)
                state=keystone.del_object(container_name,object_name,session_user,session_passwd)
                if state==True:
                    return HttpResponse(json.dumps({
                        'state': 1,
                    }))
                else:
                    return HttpResponse(json.dumps({
                        'state': 0,
                    }))
            except:
                return HttpResponse(json.dumps({
                    'state': 2,
                }))
        elif behavior=="download":

            container_name = request.POST['container_name']
            container_name = str(container_name)
            object_name = request.POST['object_name']
            object_name = str(object_name)
            ret=keystone.object_download(container_name,object_name,session_user,session_passwd)
            if ret!=False:
                s = os.path.dirname(__file__) + "/" + "static" + "/" + "upload"
                path=os.path.dirname(s,object_name)
                with open(path,"wb+") as local:
                    local.write(ret)

                def file_iterator(filename):
                    with open(filename,'rb+') as files:
                        while True:
                            c=file.read(512)
                            if c:
                                yield c
                            else:
                                break

                response=StreamingHttpResponse(file_iterator(path))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(object_name)
                return response
        else:
            pass

# 创建容器
def Create(request):
    try:
        session_user = request.session['user']
        session_passwd = request.session['passwd']
    except:
        session_user = None
        session_passwd = None
    # 判断是否是用户登录状态
    if session_user is not None:
        userstate = sessionJudge.userJudge(session_user)
    else:
        userstate = False
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)


    if request.method == "GET" and userstate == True:
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'
                                            , 'container_create.html'), {
                                            'login_user': session_user,
                      })

    elif request.method == "POST" and userstate == True:
        container_name=request.POST['container_name']
        container_name=str(container_name)
        state=keystone.create_container(container_name,session_user,session_passwd)
        if state == True:
            return HttpResponse(json.dumps({
                'state': 1,
            }))
        else:
            return HttpResponse(json.dumps({
                'state': 0,
            }))

#登录入口
def login(request):
    # 页面接受数据使用post
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        state = False      #默认上锁 验证登录状态
        print(username)
        try:
            user=USER.objects.filter(username=username).filter(passwd=password).values()
            if user is not None:
                request.session['user']=username
                #
                #*****************************************************
                #******************非常不安全 后期必须改*****************
                #*****************************************************
                #
                request.session['passwd']=password
                print username
                state=True    #进行传参json到前端 前端部分来做业务逻辑 登录成功 state=True 否则为False
        except:
            pass
        finally:
            if state==True:
                return HttpResponse(json.dumps({
                    'state' : 1,
                }))
            elif state==False:
                return HttpResponse(json.dumps({
                    'state': 0,
                }))
            else:
                return HttpResponse(json.dumps({
                    'state': 3,
                }))

    # 初始化的注册页面，需要填写
    else:
        #当以GET请求来进行访问的时候 也就是说初始登录页面
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)


#注册入口
def into(request):
    #页面接受数据使用post
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # 添加进入数据库中
        try:
            print username
            print password
            #在swift中进行注册
            domain_id="21fdfa2502014c0f8051961ee0fae344"
            project_name='admin'
            keystone_conn=keystone.get_keystone_conn()
            print "lianjie true"
            keystone_conn.users.create(username,domain_id,project_name,password)
            print "gogo"
            USER.objects.create(username=username
                                ,passwd=password
                                     )
            return HttpResponse(json.dumps({
                'state': 1,
            }))
        except:
            #失败转发到注册页面
            return HttpResponse(json.dumps({
                'state': 0,
            }))

    #初始化的注册页面，需要填写表单
    else:
        #显示初始化的页面
        template = get_template('into.html')
        html = template.render(locals())
        return HttpResponse(html)


#上传文件
def upload(request):
    try:
        session_user = request.session['user']
        session_passwd = request.session['passwd']
    except:
        session_user = None
        session_passwd = None
    # 判断是否是用户登录状态
    if session_user is not None:
        userstate = sessionJudge.userJudge(session_user)
    else:
        userstate = False
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)

    if request.method == "GET" and userstate == True:

        containnerlist = keystone.list_container(session_user,session_passwd)

        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'
                                            , 'object_create.html'), {
                                            'containnerlist': containnerlist,
                                            'login_user': session_user,
                      })

    elif request.method == "POST" and userstate == True:
        # 获取form表单信息
        container_name=request.POST['container_name']
        container_name=str(container_name)
        object_file=request.FILES.get('file')
        object_name=object_file.name
        # 存放路径
        s=os.path.dirname(__file__)+"/"+"static"+"/"+"upload"
        print s
        error=None  #锁
        # Linux本地存放
        try:
            f=open(os.path.join(s,object_file.name),'wb')
            for chunk in object_file.chunks(chunk_size=1024):
                f.write(chunk)
            path = os.path.join(s, object_file.name)
        except Exception as e:
            error = e
	
        f.close()
	
        if error==None:
            state=keystone.object_upload(container_name,object_name,path,session_user,session_passwd)
            if state==True:
                containnerlist = keystone.list_container(session_user,session_passwd)
                PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'
                                                    , 'object_create.html'), {
                                    'containnerlist': containnerlist,
                                    'login_user': session_user,
                                })
            else:
                containnerlist = keystone.list_container(session_user,session_passwd)
                PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                return render(request, os.path.join(PROJECT_ROOT, 'Yun/templates'
                                                    , 'object_create.html'), {
                                    'containnerlist': containnerlist,
                                    'login_user': session_user,
                                 })

# 下载文件
def download(request):
    try:
        session_user = request.session['user']
        session_passwd = request.session['passwd']
    except:
        session_user = None
        session_passwd=None
    # 判断是否是用户登录状态
    if session_user is not None:
        userstate = sessionJudge.userJudge(session_user)
    else:
        userstate = False
        template = get_template('login.html')
        html = template.render(locals())
        return HttpResponse(html)

    container_name = request.GET['container_name']
    object_name = request.GET['object_name']
    ret = keystone.object_download(container_name, object_name,session_user,session_passwd)
    if ret != False:
        s = os.path.dirname(__file__) + "/" + "static" + "/" + "upload"
        path = os.path.join(s, object_name)
        with open(path, "wb+") as local:
            local.write(ret)

        def file_iterator(filename):
            with open(filename, 'rb+') as files:
                while True:
                    c = files.read(512)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(object_name)
        return response









