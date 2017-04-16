#!/usr/bin/python
from flask import Flask,render_template,request
from common import Mysql_Method
from cpu_load import MachineLoadMonitor
from model import  db_session,engine
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
        data = request.form.get('data')
        date = request.form.get('date')
        time = request.form.get('time')
        d=eval(data)

        if dev == 'cpu':
            for k in d:
                sql = ("insert into  t_cpu_info (date,time,ip,cpu_num,cpu_load) \
                values('%s','%s','%s','%s','%s')" %(date,time,ip,k,d[k]['load']))
                db_session.execute(sql)
                db_session.commit()
            return "200"
        elif dev == 'net':
            for k in d:
                sql = ("insert into t_net_info(date,time,ip,avg_recv_bytes,avg_trans_bytes,\
                 avg_recv_packet,avg_trans_packet,avg_recv_drop,ang_trans_drop) \
                values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " %(date,time,ip,
                d[k]['avg_recv_bytes'],d[k]['avg_trans_bytes'],d[k]['avg_recv_packet'],
                d[k]['avg_trans_packet'],d[k]['avg_recv_drop'],d[k]['ang_trans_drop']))
                db_session.execute(sql)
                db_session.commit()
            return data
        elif dev == 'io':
            return data
        elif dev == 'mem':
            #{'cache': 850776, 'avalible': 6448148, 'total': 8115684, 'buffers': 121704, 'free': 5656004}
            sql = ("insert into t_mem_info(date,time,ip,mem_total,mem_free,mem_avalible,\
            mem_buffer,mem_cache) values('%s','%s','%s','%s','%s','%s','%s','%s')" \
            % (date,time,ip,d['total'],d['free'],d['avalible'],d['buffers'],d['cache']))
            db_session.execute(sql)
            db_session.commit() 
            return '200'
        else:
            pass
    else:
        return "<h1>login Failure !</h1>"

if __name__ == '__main__':
    app.run(debug=True)
