'''
Created on 20171025

@author: zhou
'''

import config
import time
#from .views import rm_channel_placeholder
import redis
import json

rc = redis.Redis()

def rm_channel_placeholder(data):
    for index, item in enumerate(data):
        if item == config.CHANNEL_PLACEHOLDER:
            data.pop(index)

class Comet(object):
    def check(self, channel, comet, ts, room_id = 0):
        conn_channel_set = config.CONN_CHANNEL_SET.format(channel=channel)
        if 'online_users' in comet:
            rc.sadd(conn_channel_set, 'online_users')
            new_data = rc.zrangebyscore(config.ONLINE_USER_CHANNEL, ts, '+inf')
            if new_data:
                data=rc.zrevrange(config.ONLINE_USER_CHANNEL, 0, -1)
                data.pop(0) if data[0] == config.CHANNEL_PLACEHOLDER else True
                return dict(data=data,
                        ts=time.time(), type='online_users')

        if 'room_online_users' in comet:
            rc.sadd(conn_channel_set, 'room_online_users')
            room_online_user_channel = config.ROOM_ONLINE_USER_CHANNEL.format(room=room_id)
            new_data = rc.zrangebyscore(room_online_user_channel, ts, '+inf')
            if new_data:
                users=rc.zrevrange(room_online_user_channel, 0, -1)
                rm_channel_placeholder(users)
                data = {'room_id': room_id, 'users': users}
                return dict(data=data,
                    ts=time.time(), type='room_online_users')

        if 'room_content' in comet:
            rc.sadd(conn_channel_set, 'room_content')
            room_channel = config.ROOM_CHANNEL.format(room=room_id)
            new_data = rc.zrangebyscore(room_channel, ts, '+inf')
            if new_data:
                data = {'room_id': room_id, 'content':[]}
                for item in new_data:
                    data['content'].append(json.loads(item))
                return dict(data=data, ts=time.time(), type='add_content')

        if 'room_online_users_count_all' in comet:
            rc.sadd(conn_channel_set, 'room_online_users_count_all')
            room_online_user_channels = config.ROOM_ONLINE_USER_CHANNEL.format(room='*')
            for room_online_user_channel in rc.keys(room_online_user_channels):
                new_data = rc.zrangebyscore(room_online_user_channel, ts, '+inf')
                if new_data:
                    users=rc.zrevrange(room_online_user_channel, 0, -1)
                    rm_channel_placeholder(users)
                    room_id = room_online_user_channel.split('_')[-1]
                    data = {'room_id': room_id, 'users': users}
                    return dict(data=data, ts=time.time(), type='room_online_users')

        if 'room_content_all' in comet:
            rc.sadd(conn_channel_set, 'room_content_all')
            room_channels = config.ROOM_CHANNEL.format(room='*')
            for room_channel in rc.keys(room_channels):
                new_data = rc.zrangebyscore(room_channel, ts, '+inf')
                if new_data:
                    room_id = room_channel.split('_')[-1]
                    data = {'room_id': room_id, 'content':[]}
                    for item in new_data:
                        data['content'].append(json.loads(item))
                    return dict(data=data, ts=time.time(), type='add_content')