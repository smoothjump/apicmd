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
import xlwt

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

    def getSlowLogs(self, dbInstanceId, startTime, endTime):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        s = self.DescribeSlowLogRecords(dbInstanceId, startTime, endTime, 1)
        f = xlwt.Workbook()
        j=0
        table = f.add_sheet('slow_query',cell_overwrite_ok=True)
        print "Dowloading slow query now, %d records in total" %(s["TotalRecordCount"])
        totalPageCount = s["TotalRecordCount"]/30+1
        table.write(j ,0,u"执行SQL用户及主机名")
        table.write(j,1,u"数据库名称")
        table.write(j,2,u"查询时长(秒)")
        table.write(j,3,u'锁定时长(秒)')
        table.write(j,4,u"开始执行时间")
        table.write(j,5,u"SQL语句")
        for i in xrange(totalPageCount):
            s= self.DescribeSlowLogRecords(dbInstanceId, startTime, endTime, i+1)
            j=i*30+1
            for record in s["Items"]["SQLSlowRecord"]:
                table.write(j ,0,record["HostAddress"])
                table.write(j,1,record["DBName"])
                table.write(j,2,record["QueryTimes"])
                table.write(j,3,record["LockTimes"])
                table.write(j,4,record["ExecutionStartTime"])
                table.write(j,5,record["SQLText"])
                j+=1
            table.flush_row_data()
        f.save("slow_query_"+dbInstanceId+".xls")
        print "Download done, %d records in total" %(j-1)

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
    client.getSlowLogs("XXXXXXXXX","2016-12-15T12:00Z","2016-12-16T13:00Z")