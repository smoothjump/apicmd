#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
###/usr/lib64/python2.7/site-packages/aliyun_python_sdk_core-2.1.0-py2.7.egg/aliyunsdkcore/client.py
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815 import CreateUploadPathForSQLServerRequest 
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest 
import MySQLdb as db
import json
import urllib
import types
import os
import time

class RDSClient(object):
    client_conf = {}

    def __init__(self):
        args = []
        with open("rds.ini") as conf:
            print "Loading configuration...."
            for line in conf.readlines():
                if not line.startswith("#"):
                    arg = line.strip("\n").split("=")
                    args.append(arg)
            print args
            self.client_conf = dict(args)
            conf.close()
        self.clt = client.AcsClient(self.client_conf.get("access_key"),\
        self.client_conf.get("access_secret"),\
        self.client_conf.get("region"))

    def _init_conn(self):
        with db.connect(host = self.client_conf.get("dbaas_host"),\
        port =int(host = self.client_conf.get("dbaas_port")),\
        user = self.client_conf.get("dbaas_user"),\
        passwd = self.client_conf.get("dbaas_password"),db = "dbaas") as cur:
            print "Initializing database connections,set charset to utf8...\nVersion of client library: %s" %(db.get_client_info())
            cur.execute("set names utf8")
            return cur

    def _getName(self,instance_name):
        cur = self._init_conn()
        stat = "select ins_name from cust_instance where is_deleted=0 and conn_addr = \'"+instance_name+"\' or ins_name = \'"+instance_name+"\' limit 1;"
        print "%s" %stat
        cur.execute(stat)
        ins_name = cur.fetchone()[0]
        cur.close()
        return ins_name

    def describeDBInstance(self,name):
        ins_name = self._getName(name)
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        s = json.loads(self.clt.do_action(request))
        print s

    def describeBackups(self,name,start_time,end_time):
        ins_name = self._getName(name)
        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        request.set_StartTime(start_time+'T08:00Z')
        request.set_EndTime(end_time+'T08:00Z')
        s = json.loads(self.clt.do_action(request))
        result=[]
        for item in s['Items']['Backup']:
            result.append(item['BackupDownloadURL'])
        return result

    def describeDBInstances(self):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest() 
        request.set_accept_format('json')
        print self.clt.do_action(request)
            
    def createUploadPathForSQLServer(self, ins_name,db_name):
        request = CreateUploadPathForSQLServerRequest.CreateUploadPathForSQLServerRequest() 
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        request.set_DBName(db_name)
        print self.clt.do_action(request)

    def describeRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        print self.clt.do_action(request)

def downloadHook(block_read,block_size,total_size):
    if not block_read:
        print "Download begins...";
        return
    if total_size<0:
    #unknown size
        print "read %d blocks (%dbytes)" %(block_read,block_read*block_size);
    else:
        amount_read=block_read*block_size;
        print 'Read %d blocks,or %d/%d' %(block_read,block_read*block_size,total_size);

def dowloadFromURLs(urlList):
    if type(urlList)==type(u' '):
        file_name = os.getcwd()+urlList.split("/")[-1].split('?')[0]
        print "Download path: %s" %file_name
        urllib.urlretrieve(urlList,file_name,reporthook=downloadHook)
    elif type(urlList)==types.ListType:
        for url in urlList:
            file_name = os.getcwd()+url.split("/")[-1].split('?')[0]
            urllib.urlretrieve(url,file_name,reporthook=downloadHook)
    else:
        print "Invalid argument!"

if __name__=='__main__':
    client = RDSClient()
    client.describeRegions()
    client.createUploadPathForSQLServer('rds5708ip684n4267170','tt1')
