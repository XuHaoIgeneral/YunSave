# -*- coding: utf-8 -*-
from Yun.models import USER

class Personal():
    #个人标签信息查看
    def partysu(self,username):
        userInformation=USER.objects.filter(username=username)
        