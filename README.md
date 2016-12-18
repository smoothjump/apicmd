# apicmd
Aliyun API commandline tool

## 使用依赖
1. 下载 aliyun open api sdk(https://pypi.python.org/pypi)

2. 修改endpoints.xml中的`region_id`和对应域字段后再执行`sudo python setup.py install`(具体Region ID查看CMDB)

3. 测试各个产品的endpoint链接是否可用

4. 填写aliapi.ini参数(AK及regionID)
		
		AccessKeyId=4FWXXXXXXXXX
		AccessKeySecret=iXXXXXXXXXXXXXXA8tN98X
		RegionId=cn-aliyun-c01
		
## 使用须知
工具运行动态加载api类执行openapi对应action，具体参数和公有云保持一致。