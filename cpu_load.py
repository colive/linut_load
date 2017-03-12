#!/usr/bin/python

from __future__ import division
import time
import os
import sys
from multiprocessing import cpu_count


class MachineLoadMonitor():
    verison=1.0

    def get_cpu_core_num(self):
        return cpu_count()+1

    def get_cpu_stat(self):
        cpu_stat = {}
        cpu_stat_file = '/proc/stat'
        f = open(cpu_stat_file,'r')
        for line in f.readlines()[0:5]:
            cpu_no,user,nice,system,idle,iowait,irq,softirq = line.split()[0:8]
            cpu_total = int(user)+int(nice)+int(system)+int(idle)+int(iowait)+int(irq)+int(softirq)
            cpu_used = int(user)+int(nice)+int(system)+int(irq)+int(softirq)
            cpu_stat[cpu_no] = {'cpu_total':cpu_total,'cpu_used':cpu_used}
        f.close()
        return cpu_stat
    def cpu_load_load(self):
        cpu_time1 = self.get_cpu_stat()
        time.sleep(10)
        cpu_time2 = self.get_cpu_stat()
        for k in cpu_time1:
            print k, (cpu_time2[k]['cpu_used'] - cpu_time1[k]['cpu_used'])/(cpu_time2[k]['cpu_total'] - cpu_time1[k]['cpu_total']) * 100

    def get_mem_load(self):
        mem_file = '/proc/meminfo'
        mem_use = 0
        with open(mem_file,'r') as f:
            total = int(f.readline().split()[1])
            free = int(f.readline().split()[1])
            avalible = int(f.readline().split()[1])
            buffers = int(f.readline().split()[1])
            cache = int(f.readline().split()[1])
            mem_use = total-free-buffers-cache-avalible
        print mem_use


    def get_net_interface_stat(self):
        net_file = '/proc/net/dev'
        net_dev_stat = {}
        f = open(net_file,'r')
        for line in f.readlines()[2:]:
            interface = line.split()[0]
            recv_byte,recv_packet,recv_drop = int(line.split()[1]),int(line.split()[2]),int(line.split()[4])
            trans_byte,trans_packet,trans_drop = int(line.split()[9]),int(line.split()[10]),int(line.split()[12])
            net_dev_stat[interface] = {'recv_bytes':recv_byte,'recv_packet':recv_packet,'recv_drop':recv_drop,
            'trans_bytes':trans_byte,'trans_packet':trans_packet,'trans_drop':trans_drop}
        f.close()
        return net_dev_stat

    def get_net_interface_load(self):
        net_stat1 = self.get_net_interface_stat()
        time.sleep(10)
        net_stat2 = self.get_net_interface_stat()
        for k in net_stat2:
            avg_recv_bytes = (net_stat2[k]['recv_bytes'] - net_stat1[k]['recv_bytes']) * 8 / 60 / 1000
            avg_trans_bytes = (net_stat2[k]['recv_bytes'] - net_stat1[k]['recv_bytes']) * 8 / 60 / 1000
            avg_recv_packet = (net_stat2[k]['recv_packet'] - net_stat1[k]['recv_packet'])  / 60 
            avg_trans_packet = (net_stat2[k]['trans_packet'] - net_stat1[k]['trans_packet']) / 60 
            avg_recv_drop = (net_stat2[k]['recv_drop'] - net_stat1[k]['recv_drop']) / 60 
            ang_trans_drop = (net_stat2[k]['trans_drop'] - net_stat1[k]['trans_drop']) / 60 
            print k,avg_recv_bytes,avg_trans_bytes,avg_recv_packet,avg_trans_packet,avg_recv_drop,ang_trans_drop

if __name__ == '__main__':
    a=MachineLoadMonitor()
   # a.get_cpu_stat()
    a.cpu_load_load()
    a.get_mem_load()
    a.get_net_interface_load()
