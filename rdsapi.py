#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 执行前下载 aliyun open api sdk(https://pypi.python.org/pypi)
# 修改endpoints.xml中的region_id和Rds域字段
# ------传入参数命名规则(忽略大小写)
# dbInstanceClass: 实例规格
# engine: RDS类型(取值MySQL, SQLServer, PostgresSQL, PPAS)
# engineVersion: 数据库版本号
# dbInstanceStorage: 数据库存储
# dbInstanceNetType: 网络连接类型
# dbInstanceDescription: 实例描述
# securityIPList: RDS白名单
# vpcId: VPC ID
# vSwitchId: vSwitch ID
# privateIPAddress: 私网IP地址
# dbInstanceId: RDS实例名
# dbName: 数据库名称

from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815 import CreateUploadPathForSQLServerRequest 
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import CreateReadOnlyDBInstanceRequest
from aliclient import AliClient
import MySQLdb as db
import json
import urllib
import types
import os
import sys
import time

class RDSClient(AliClient):
    client_conf = {}

    def __init__(self, confFile):
        super(RDSClient,self).__init__(confFile)

    def _init_conn(self):
        with db.connect(host = self.client_conf.get("dbaas_host"),\
        port =int(self.client_conf.get("dbaas_port")),\
        user = self.client_conf.get("dbaas_user"),\
        passwd = self.client_conf.get("dbaas_password"),db = "dbaas") as cur:
            print "Initializing database connections,set charset to utf8...\nVersion of client library: %s" %(db.get_client_info())
            cur.execute("set names utf8")
            return cur

    def _getName(self,dbInstanceId):
        cur = self._init_conn()
        stat = "select ins_name from cust_instance where is_deleted=0 and conn_addr = \'"+instance_name+"\' or ins_name = \'"+instance_name+"\' limit 1;"
        print "%s" %stat
        cur.execute(stat)
        ins_name = cur.fetchone()[0]
        cur.close()
        return ins_name

    def DescribeDBInstance(self,dbInstanceId):
        ins_name = self._getName(name)
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        s = json.loads(self.clt.do_action(request))
        print s

    def DescribeBackups(self,dbInstanceId,start_time,end_time):
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

    def DescribeDBInstances(self):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest() 
        request.set_accept_format('json')
        print self.clt.do_action(request)
            
    def CreateUploadPathForSQLServer(self, dbInstanceId,dbName):
        request = CreateUploadPathForSQLServerRequest.CreateUploadPathForSQLServerRequest() 
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        request.set_DBName(db_name)
        print self.clt.do_action(request)

    def DescribeRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        print self.clt.do_action(request)

    def CreateReadOnlyDBInstance(self,dbInstanceId,dbInstanceClass,dbInstanceStorage,engineVersion="5.6"):
        ins_name = self._getName(dbInstanceId)
        request = CreateReadOnlyDBInstanceRequest.CreateReadOnlyDBInstanceRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(ins_name)
        request.set_EngineVrsion(version)
        request.set_DBInstanceClass(ins_cls)
        request.set_DBInstaceStorage(storage)
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