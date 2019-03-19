'''
Created on 20171025

@author: zhou
'''

from flask import Flask, request, session, render_template, Response, jsonify, redirect, flash, url_for
from . import chat
import redis
import time
import json
import config
import gevent
from .models import Comet, rm_channel_placeholder
from .text import linkify, escape_text
from ..api.onlineusers import mark_online, get_online_users, get_user_last_activity

# rc = redis.Redis()

'''
@chat.before_app_request
def mark_current_user_online():
    if request.headers.get('X-Forwarded-For'):
        mark_online(request.headers['X-Forwarded-For'])
    else:
        mark_online(request.remote_addr)
'''

@chat.route('/chat/index', methods=['GET', 'POST'])
def chat_index():
    t = time.asctime( time.localtime(time.time()) )
    Online_user = get_online_users()
    return render_template('chat/index_chat.html',Online_user=Online_user, t=t)












