# -*- coding: utf-8 -*-
from Yun.models import USER
from django.shortcuts import render

def userJudge(username):
    try:
        user=USER.objects.get(username=username)
        return True
    except:
        return True

