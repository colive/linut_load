#!/usr/bin/python
from flask import Flask,render_template,request
from common import Mysql_Method
from cpu_load import MachineLoadMonitor
from model import  db_session,engine
from datetime import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/load_feedback",methods = ['GET','POST'])
def load_feedback():
    if request.method == 'POST':
        dev = request.form.get('dev')
        ip = request.form.get('inner_ip')
        print ip
        data = request.form.get('data')
        d=eval(data)
        if dev == 'cpu':
            for k in d:
                sql = "insert into  t_cpu_info (date,time,ip,cpu_num,cpu_load) values('20170325','0010','%s','%s','%s')" %(ip,k,d[k]['load'])
                print  sql
                db_session.execute(sql)
                db_session.commit()
            return "200"
        elif dev == 'net':
            return data
        elif dev == 'io':
            return data
        elif dev == 'mem':
            return data
        else:
            pass
    else:
        return "<h1>login Failure !</h1>"

if __name__ == '__main__':
    app.run(debug=True)
