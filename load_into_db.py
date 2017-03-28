#!/usr/bin/python
from flask import Flask,render_template,request
from common import Mysql_Method
from cpu_load import MachineLoadMonitor

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load_feedback",methods = ['GET','POST'])
def load_feedback():
    if request.method == 'POST':
        dev = request.form.get('dev')
        print dev
        ip = request.form.get('ip')
        data = request.form.get('data')
        if dev == 'cpu':
            return "cpu" 
        elif dev == 'net':
            return "net"    
        elif dev == 'io':
            return "io"
        elif dev == 'mem':
            return "mem"
        else:
            pass
    else:
        return "<h1>login Failure !</h1>"

if __name__ == '__main__':
    app.run(debug=True)
