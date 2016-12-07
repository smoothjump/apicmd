#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
# 执行前下载 aliyun open api sdk(https://pypi.python.org/pypi)
# 约定：所有执行action方法都需要以大写字母开头，调用参数与openapi名称一致
# 以JSON格式导入执行命令

from aliyunsdkcore import client
import inspect
import json
import urllib
import types
import os
import sys
import time
import argparse

class AliClient(object):
    client_conf = {}

    def __init__(self, confFile):
        args = []
        with open(confFile) as conf:
            print "Loading private cloud configuration...."
            for line in conf.readlines():
                if not line.startswith("#"):
                    arg = line.strip("\n").split("=")
                    args.append(arg)
            self.client_conf = dict(args)
            conf.close()
        self.clt = client.AcsClient(self.client_conf.get("AccessKeyId"),\
        self.client_conf.get("AccessKeySecret"),\
        self.client_conf.get("RegionId"))

    def doAction(self, paras):
        action = paras["action"]
        if hasattr(self,action) and action[:1].isupper():
            print "Action: %s" %paras["action"]
            func = getattr(self,paras["action"])
            print func
            args = getattr(inspect.getargspec(func),"args")
            args = args[1:]
            val = []
            for i in args:
                val.append(paras[i])
            try:
                apply(func,val)
            except KeyError as e:
                print "Your parameter list has some problem(s), pls re-check again:"
                print "Action: %s" %paras["action"]
                print "Require parameter as follows" %args
                raise SystemExit
        else:
            print "Action: %s for product %s not implemented or not exist" %(paras["action"], paras["product"].upper())