

import redis

rc = redis.Redis()

p = rc.pubsub()



print type(p)
