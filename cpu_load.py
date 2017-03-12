#!/usr/bin/python

from __future__ import division
import time
import os
import sys
from multiprocessing import cpu_count


class CpuLoadMonitor():
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
    def cpu_load_statistic(self):
        cpu_time1 = self.get_cpu_stat()
        time.sleep(5)
        cpu_time2 = self.get_cpu_stat()
        for k in cpu_time1:
            print k, (cpu_time2[k]['cpu_used'] - cpu_time1[k]['cpu_used'])/(cpu_time2[k]['cpu_total'] - cpu_time1[k]['cpu_total']) * 100

if __name__ == '__main__':
    a=CpuLoadMonitor()
   # a.get_cpu_stat()
    a.cpu_load_statistic()
