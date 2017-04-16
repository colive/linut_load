#!/usr/bin/env  python
# --*-- coding:UTF-8 --*--
import  sys
#import  tab
import  re
import  os
import  time
import docker
import  commands

def get_container_info(container_name):
    global container_stats
    conn = docker.APIClient(base_url='unix://run/docker.sock',version='1.21')
    stats = conn.stats(container_name)
    try:
        container_stats=eval(stats.next())
        print container_stats['precpu_stats']
        print container_stats['memory_stats']
        print container_stats['cpu_stats']
        print container_stats['networks']
    except NameError,error_msg:
        pass
#        print error_msg
        container_stats=eval(generator.next())

    finally:
        conn.close()

get_container_info('ubuntu21')
time.sleep(30)
get_container_info('ubuntu21')
