# -*- coding = utf-8 -*-
# @Time: 2023/01/15
# @Author:MoyiTech
# @Software: PyCharm
from flask import Flask, render_template
from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler
import data_process
from settings import refresh_time, http_host, http_port

scheduler = BackgroundScheduler()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=refresh_time)


@app.route('/')
def root():
    now = datetime.now()
    print(now.strftime("%Y/%m/%d-%H:%M"))
    return render_template('index.html', last_time=data_process.last_time)


if __name__ == '__main__':
    scheduler.add_job(func=data_process.run_task, trigger='interval', seconds=refresh_time)
    scheduler.start()
    app.run(host=http_host, port=http_port)
