#!/usr/bin/python

from __future__ import division
import time
import os
import sys
import re
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
    def get_cpu_load(self):
        cpu_load_dict = {}
        cpu_time1 = self.get_cpu_stat()
        time.sleep(5)
        cpu_time2 = self.get_cpu_stat()
        for k in cpu_time1:
            cpu_load = (cpu_time2[k]['cpu_used'] - cpu_time1[k]['cpu_used'])/(cpu_time2[k]['cpu_total'] - cpu_time1[k]['cpu_total']) * 100
            cpu_load_dict[k] = {'load':cpu_load}
        return cpu_load_dict
            
    def get_mem_load(self):
        mem_file = '/proc/meminfo'
        mem_load = {}
        with open(mem_file,'r') as f:
            mem_load['total'] = int(f.readline().split()[1])
            mem_load['free'] = int(f.readline().split()[1])
            mem_load['avalible'] = int(f.readline().split()[1])
            mem_load['buffers'] = int(f.readline().split()[1])
            mem_load['cache'] = int(f.readline().split()[1])
            
        return mem_load


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
        time.sleep(5)
        net_stat2 = self.get_net_interface_stat()
        net_load = {}
        for k in net_stat2:
            avg_recv_bytes = (net_stat2[k]['recv_bytes'] - net_stat1[k]['recv_bytes']) * 8 / 60 / 1000
            avg_trans_bytes = (net_stat2[k]['recv_bytes'] - net_stat1[k]['recv_bytes']) * 8 / 60 / 1000
            avg_recv_packet = (net_stat2[k]['recv_packet'] - net_stat1[k]['recv_packet'])  / 60 
            avg_trans_packet = (net_stat2[k]['trans_packet'] - net_stat1[k]['trans_packet']) / 60 
            avg_recv_drop = (net_stat2[k]['recv_drop'] - net_stat1[k]['recv_drop']) / 60 
            ang_trans_drop = (net_stat2[k]['trans_drop'] - net_stat1[k]['trans_drop']) / 60 
            net_load[k] = {'avg_recv_bytes':avg_recv_bytes,'avg_trans_bytes':avg_trans_bytes,'avg_recv_packet':avg_recv_packet,
            'avg_trans_packet':avg_trans_packet,'avg_recv_drop':avg_recv_drop,'ang_trans_drop':ang_trans_drop}
        return net_load

    def get_io_stat(self):
        io_file = '/proc/diskstats'
        io_stat = {}
        f = open(io_file,'r')
        for line in f:
            #   8      34 sdc2 115 0 17752 4144 0 0 0 0 0 3896 4144
            (main_dev_num,next_dev_num,dev_name,read_succ_count,merge_read_count,read_block_count,
            read_time,write_succ_count,merge_write_count,write_block_count,write_time,io_progress,
            io_time,io_spend_time)=line.split(' ')[0:14]
            if re.match('sd',dev_name):
                io.stat[dev_name]={'read_succ_count':read_succ_count,'merge_read_count':merge_read_count,
                'read_block_count':read_block_count,'read_time':read_time,
                'write_succ_count':write_succ_count,'merge_write_count':merge_write_count,
                'write_block_count':write_block_count,'write_time':write_time,
                'io_progress':io_progress,'io_time':io_time,'io_spend_time':io_spend_time}
        f.close()
        return io_stat
    def get_io_load(self):
        io_time1 = self.get_io_stat()
        time.sleep(5)
        io_time2 = self.get_io_stat()
        io_load = {}
        for k in io_time2:
            read_succ_count = int(io_time2[k]['read_succ_count']) - int(io_time1[k]['read_succ_count'])
            merge_read_count = int(io_time2[k]['merge_read_count']) - int(io_time1[k]['merge_read_count'])
            read_block_count = int(io_time2[k]['read_block_count']) - int(io_time1[k]['read_block_count'])
            read_time = int(io_time2[k]['read_time']) - int(io_time1[k]['read_time'])
            write_succ_count = int(io_time2[k]['write_succ_count']) - int(io_time1[k]['write_succ_count'])
            merge_write_count = int(io_time2[k]['merge_write_count']) - int(io_time1[k]['merge_write_count'])
            write_block_count = int(io_time2[k]['write_block_count']) - int(io_time1[k]['write_block_count'])
            write_time = int(io_time2[k]['write_time']) - int(io_time1[k]['write_time'])
            io_progress = int(io_time2[k]['io_progress']) - int(io_time1[k]['io_progress'])
            io_time = int(io_time2[k]['io_time']) - int(io_time1[k]['io_time'])
            io_spend_time =  int(io_time2[k]['io_spend_time']) - int(io_time1[k]['io_spend_time'])
            io_load[k] = {'read_succ_count':read_succ_count,'merge_read_count':merge_read_count,'read_block_count':read_block_count,
            'read_time':read_time,'write_succ_count':write_succ_count,'merge_write_count':merge_write_count,'write_block_count':write_block_count
            ,'write_time':write_time,'io_progress':io_progress,'io_time':io_time,'io_spend_time':io_spend_time}
        return io_load




if __name__ == '__main__':
    a=MachineLoadMonitor()
    #a.get_cpu_stat()
    #a.get_cpu_load()
    #a.get_mem_load()
    #a.get_net_interface_load()
    a.get_io_load()
