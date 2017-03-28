#!/usr/bin/python
import urllib2
import urllib
from cpu_load import MachineLoadMonitor as MLM

def postHttp(dev,data,inner_ip):
    url='http://127.0.0.1:5000/load_feedback'
    postdata=dict(dev = dev,data = data,inner_ip=inner_ip)
    data=urllib.urlencode(postdata)
    request = urllib2.Request(url,data)
    response=urllib2.urlopen(request)
    print response.read()
d=MLM()        
cpu_data = d.get_cpu_load()
postHttp('cpu',cpu_data,'1')
#mem_data = d.get_mem_load()
#postHttp('mem',mem_data,'1')
#net_data = d.get_net_interface_load()
#postHttp('net',net_data,'1')
#io_data = d.get_io_load()
#postHttp('io',io_data,'1')


