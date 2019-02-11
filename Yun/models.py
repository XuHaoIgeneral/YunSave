# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class USER(models.Model):

    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    passwd=models.CharField(max_length=255)
    u_time=models.DateField(auto_now_add=True)

    class Meta:
        index_together = [["id", "username"]]
        unique_together=("username",)
        db_table="user"
        ordering = ('-id',)

    def __unicode__(self):
        return self.username