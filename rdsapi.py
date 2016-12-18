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
# startTime: 开始时间，格式为：YYYY-MM-DDTHH24:MMZ
# endTime: 开始时间，格式为：YYYY-MM-DDTHH24:MMZ

from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest
from aliyunsdkrds.request.v20140815 import CreateUploadPathForSQLServerRequest 
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import CreateReadOnlyDBInstanceRequest
from aliyunsdkrds.request.v20140815 import DescribeSlowLogsRequest
from aliyunsdkrds.request.v20140815 import DescribeSlowLogRecordsRequest
from aliclient import AliClient
import json
import urllib
import types
import os
import sys
import time
import csv

class RDSClient(AliClient):
    client_conf = {}

    def __init__(self, confFile):
        super(RDSClient,self).__init__(confFile)

    def DescribeDBInstance(self,dbInstanceId):
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(dbInstanceId)
        s = json.loads(self.clt.do_action(request))
        print s

    def DescribeSlowLogRecords(self, dbInstanceId, startTime, endTime, pageNumber):
        pageNumber = 1
        request = DescribeSlowLogRecordsRequest.DescribeSlowLogRecordsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(dbInstanceId)
        request.set_StartTime(startTime)
        request.set_EndTime(endTime)
        request.set_PageNumber(pageNumber)
        return json.loads(self.clt.do_action(request))

    def DescribeBackups(self,dbInstanceId,startTime,endTime):
        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(dbInstanceId)
        request.set_StartTime(startTime)
        request.set_EndTime(endTime)
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
        request.set_DBInstanceId(dbInstanceId)
        request.set_DBName(db_name)
        print self.clt.do_action(request)

    def DescribeRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        print self.clt.do_action(request)

    def CreateReadOnlyDBInstance(self,dbInstanceId,dbInstanceClass,dbInstanceStorage,engineVersion="5.6"):
        request = CreateReadOnlyDBInstanceRequest.CreateReadOnlyDBInstanceRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(dbInstanceId)
        request.set_EngineVrsion(version)
        request.set_DBInstanceClass(ins_cls)
        request.set_DBInstaceStorage(storage)
        print self.clt.do_action(request)

    def getSlowLogs(self, dbInstanceId, startTime, endTime, excelFile):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        s = self.DescribeSlowLogRecords(dbInstanceId, startTime, endTime, 1)
        if os.path.isfile(excelFile):
            f = open(excelFile,"w")
            totalPageCount = s["TotalRecordCount"]/30+1
            for i in xrange(totalPageCount):
                s= self.DescribeSlowLogRecords(dbInstanceId, startTime, endTime, i+1)
                for record in s["Items"]["SQLSlowRecord"]:
                    f.write(record["HostAddress"]+","\
                        +record["DBName"]\
                        +","+str(record["QueryTimes"])\
                        +","+str(record["LockTimes"])\
                        +","+record["ExecutionStartTime"]+"\n")\
                        +","+record["SQLText"].replace("\r\n"," ")
                f.flush()
            f.close()

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

if __name__=="__main__":
    client = RDSClient("aliapi.ini")
    client.getSlowLogs("rds7q8ziv2chbwmb8elcy","2016-12-15T12:00Z","2016-12-15T13:00Z","slowLogs.csv")