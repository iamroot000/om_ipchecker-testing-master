# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class GROUPS(models.Model):
    group = models.CharField(verbose_name='Group', max_length=64, primary_key=True)

    class Meta:
        verbose_name = u"Group"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % (self.group)


class HOSTS(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    hostname = models.CharField(verbose_name='Hostname', max_length=64,null=True,blank=True)
    host_ip = models.GenericIPAddressField(verbose_name='Host IP',unique=True)
    hosttype = models.CharField(verbose_name='Host Type', max_length=64,null=True,blank=True)
    groups = models.ManyToManyField(GROUPS, verbose_name='Groups',null=True,blank=True)
    remarks = models.TextField(verbose_name='Remarks',null=True,blank=True)
    enabled = models.BooleanField(verbose_name='Enabled',default=False)


    class Meta:
        verbose_name = u"Host"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if self.host_ip.startswith('10.16'):
            self.hosttype = 'HKIDC'

        elif self.host_ip.startswith('192.168.'):
            self.hosttype = 'TZIDC'
        else:
            self.hosttype= 'CLOUD_HOST'

        super(HOSTS, self).save(*args, **kwargs)

    def __str__(self):
        return self.host_ip