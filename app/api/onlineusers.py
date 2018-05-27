'''
Created on 2017415

@author: zhou
'''

import os
import redis
import time
from datetime import datetime
from config import config
from flask import current_app
#rc = redis.from_url('redis://h:pd267e12c87bf8b379b46374c1c7a753bb1498ec6c3ad31b08007c1b878afb39b@ec2-34-236-65-51.compute-1.amazonaws.com:39539')
rc=redis.from_url('redis://h:p00f294fe37e130212ed6242c58f6961e4c41112c3aa00b15dbf4c165a975851f@ec2-54-86-200-206.compute-1.amazonaws.com:11759')
#cfg = config[os.getenv('FLASK_CONFIG') or 'default']()

def mark_online(user_id):
    now = int(time.time())
    #expires = now + (cfg.ONLINE_LAST_MINUTES * 60) + 10
    expires = now + (current_app.config['ONLINE_LAST_MINUTES'] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    users_key = 'user-activity/%s' % user_id
    p = rc.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(users_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(users_key, expires)
    p.execute()

def get_user_last_activity(user_id):
    last_active = rc.get('user-activity/%s' % user_id)
    if last_active is None:
        return None
    return datetime.utcfromtimestamp(int(last_active))

def get_online_users():
    current = int(time.time()) // 60
    #minutes = xrange(cfg.ONLINE_LAST_MINUTES)
    minutes = xrange(current_app.config['ONLINE_LAST_MINUTES'])
    return rc.sunion(['online-users/%d' % (current - x) for x in minutes])


