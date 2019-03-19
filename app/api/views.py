'''
Created on 20171029

@author: zhou
'''

from .forms import QueryIPForm, TalkForm
from flask import render_template, session, redirect, url_for, current_app,flash, abort, request, make_response, g
from flask import Response, jsonify
from . import api
from .queryip import queryip
from .onlineusers import mark_online, get_online_users, get_user_last_activity
from flask_login import login_required
from flask_login.utils import current_user
from ..decorators import admin_required, permission_required
from .check_mobile import checkMobile
from .todayonhistory import todayonhistory
from .talk_robot import talkrobot
import time
import sys
from .mongo_conn import Mongo_Conn
from flask_restful import Resource, Api
from ..models import Post, User, Comment


@api.route('/api/v1.0/posts/')
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/api/v1.0/users/')
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]})


@api.route('/api/v1.0/comments')
def get_comments():
    comments = Comment.query.all()
    return jsonify({'comments': [comment.to_json() for comment in comments]})


@api.route('/api/todayonhistory/enevts/<m>/<d>', methods=['GET', 'POST'])
def querytoday(m, d):
    history = todayonhistory(m, d)
    his = history['Events']
    return render_template('api/todayonhistory.html', his=his)


@api.route('/api/talk-robot/<info>/<roomid>', methods=['GET', 'POST'])
def talk(info, roomid):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    db = Mongo_Conn()
    t = time.strftime("%Y-%m-%d %X", time.localtime())
    #info_new = info.decode('utf-8').encode('unicode_escape')[2:]
    content = talkrobot(info)
    rooms = db[roomid]
    rooms.insert({"robotsay":content,"yousay":info, "time":t})
    cc = {"robotsay":content,"yousay":info, "time":t}
    return content
    # return json.dumps(cc)
    # return jsonify(
    #     {'text': 'haha'}
    # )
    # return render_template('api/talk_robot.html', content=content)


@api.route('/api/talkrobot', methods=['GET', 'POST'])
def talk_robot():
    db = Mongo_Conn()
    t = time.strftime("%Y-%m-%d %X", time.localtime())
    room = "R" + str(t)
    rooms = db[room]
    rooms.insert({"robotsay":"","yousay":"","time":t})
    form = TalkForm()
    # if form.validate_on_submit():
    #     info = form.body.data
    #     content = talkrobot(info)
    #     return content
        # return render_template('api/talk.html', form=form, content=content, t=t)
    return render_template('api/talk.html',form=form, t=t, room=room)


@api.before_app_request
def checkmobile():
    MB = False
    if checkMobile(request):
        MB = True


@api.route('/api/query-ip', methods=['GET', 'POST'])
def query_ip():
    form = QueryIPForm()
    if form.validate_on_submit():
        ip = form.search.data
        # return redirect('http://maps.google.com/?ip=%s' % ip)
        return redirect(url_for('.ip_detail',ip=ip))
    return render_template('api/query_ip.html',form=form)


@api.route('/api/ip-detail/<ip>')
def ip_detail(ip):
    ip = queryip(ip)
    ipAddress = ip['ip']
    ip_is_available = ip['valid']
    YIP = request.headers.get('X-Forwarded-For',request.remote_addr)
    if ip['valid'] == True:
        countryName = ip['country']
        countryCode = ip['country_code']
        region = ip['region']
        # continentName = ip['continent_code']
        ipAddress = ip['ip']
        city = ip['city']
        continentCode = ip['continent_code']
        lat = ip['latitude']
        lon = ip['longitude']
        # location = query_lat_long(countryName,countryCode)
        # if len(location['locations']) != 0:
    #   lat = location['locations'][0]['latitude']
    #   lon = location['locations'][0]['longitude']
        return render_template('api/ip_detail.html', countryName=countryName,
                            countryCode=countryCode, region=region,
                            ipAddress=ipAddress,ip_is_available=ip_is_available,
                            city=city, continentCode=continentCode,
                            lat=lat, lon=lon,YIP=YIP)
    return render_template('api/ip_detail.html', countryName='',
                               countryCode='', region='',
                               ipAddress=ipAddress,lat=0, lon=0,
                               city='', continentCode='',ip_is_available=ip_is_available,
                           YIP=YIP)

'''
@api.before_app_request
def mark_current_user_online():
    if request.headers.get('X-Forwarded-For'):
        mark_online(request.headers['X-Forwarded-For'])
    else:
        mark_online(request.remote_addr)
'''

@api.route('/api/online-user')
@login_required
@admin_required
def online_user():
    Online_user = get_online_users()
    for i in Online_user:
        location = queryip(i)
        city = location.get('city','kenya')
        return render_template('api/online_user.html', Online_user=Online_user, city=city)
    return Response('Online User: %s' % ','.join(get_online_users()), mimetype='text/plain')


@api.route('/api/online-info')
def online_info():
    # raise Exception('test')
    apiua = request.headers
    return Response('Online Info: %s' % apiua)


@api.route('/api/check-mobile')
def check_mobile():
    if checkMobile(request):
        return 'Mobile'
    else:
        return 'PC'


