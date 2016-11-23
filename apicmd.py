#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os

# 日志输出定义
logging.basicConfig(level=logging.DEBUG,\
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
    datefmt='%a, %d %b %Y %H:%M:%S',\
    filename='pwd_scan.log',\
    filemode='w')
# 全局命令行转换函数
def cmdParser():
    parser = argparse.ArgumentParser(description='Aliyun private cloud API tool commandline')
    parser.add_argument('-P','--product',dest = 'product', action = 'store',\
        help='Specify the product name, only rds was implemented for now', default='rds')
    parser.add_argument('-a','--action',dest = 'action', action = 'store',\
        help = 'Action defined in open API document', default = '{action:DescribeRegions}')
    args = parser.parse_args()
    if not any(args.__dict__.values()):
        parser.print_help()
        raise SystemExit
    return args.__dict__

class AliyunClient(object):
	
