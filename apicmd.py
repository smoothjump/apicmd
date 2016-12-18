#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import json
import apiloader

# 日志输出定义
logging.basicConfig(level=logging.DEBUG,\
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
    datefmt='%a, %d %b %Y %H:%M:%S',\
    filename='api.log',\
    filemode='w')

# 全局命令行转换函数
def getOptions(usage):
    parser = argparse.ArgumentParser(usage)
    parser.add_argument("-n", "--dryrun", action="store", help="dryrun")
    parser.add_argument("-j", "--json", dest = 'parameters', action="store",\
        help="json string", default = "{\"action\":\"DescribeLoadBalancers\"}")
    parser.add_argument("-f", '--conf', dest = 'conf', action="store",\
        help="configuration file", default = "aliapi.ini")
    parser.add_argument("-o", "--ouput", dest = 'output', action="store",\
        help="outfile")
    parser.add_argument("-p", "--product", dest = 'product', action="store",\
        help="outfile", default = "slb")
    args = parser.parse_args()
    if not any(args.__dict__.values()):
        parser.print_help()
        raise SystemExit
    return args.__dict__

if __name__=='__main__':
    args = getOptions("Open API command line tool")
    aliClient = None
    product = args["product"]
    aliClient = apiloader.getObject(product+"api"+"."+product.upper()+"Client", args["conf"])
    if aliClient is not None:
        paras = json.loads(args["parameters"])
        print paras
        aliClient.doAction(paras)
    else:
        print "Open api tool for product \"%s\" has not yet implemented" %args["product"]
    
