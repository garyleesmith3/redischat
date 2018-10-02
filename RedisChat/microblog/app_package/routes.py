
from flask import render_template, flash, redirect, url_for
from app_package import da_app
from app_package.forms import InputForm
import redis
import os
import time

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

redis_client.hset("incrementer", "count", 0)


@da_app.route('/')
@da_app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        count = redis_client.hget("incrementer","count") # + 1
        mystring = str(count)
        myint = int(mystring)
        myint += 1     
        redis_client.hset("incrementer","count", myint)
        frogName = form.variableX.data
        frogMessage = form.variableY.data
        messageObject = {"name":frogName, "message":frogMessage}
        redis_client.hmset(myint, messageObject)
        value = redis_client.hmget(myint, ['name', 'message'])
        redis_client.zadd("chosenSet", myint, value)
        return redirect('/index')
    return render_template('index.html', title='Home', form=form, redis_client=redis_client) # posts=posts , value=value, user=user)




