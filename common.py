#!/usr/bin/python
#coding=gbk

#use for:something common
#author : colive
import MySQLdb as Mdb
import ConfigParser
import os
import sys
import datetime



class Mysql_Method():
    
    def __init__(self):
        self.conf_file = '/tmp/load_updata.ini'
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(self.conf_file)
        except Exception,e:
            print "Error: no such file"
        else:
            self.host = cf.get("mysql", "host")
            self.user = cf.get("mysql", "user")
            self.passwd = cf.get("mysql", "password")
            self.port = cf.getint("mysql", "port")
            self.db = cf.get("mysql", "database")
            print self.host
            self.conn = Mdb.connect(host=self.host,user = self.user,passwd = self.passwd,db = self.db,charset='gbk')
            self.cursor = self.conn.cursor()

    def _sql_insert(self,sql):
        try:
            self.execute(sql)
        except Exception,e:
            print e.error 

    def __close__(self):
        self.conn.close()

if __name__ == '__main__':
    c= Mysql_Method()

        
