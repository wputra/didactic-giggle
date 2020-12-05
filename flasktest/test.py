import time
import redis
import string
import random


cache = redis.Redis(host='localhost', port=6379)

def short_url_generator(size=9):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def set_url(short_url, long_url):
    retries = 5
    while True:
        try:
            return cache.set(short_url, long_url)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

surl = short_url_generator()
lurl = cache.get("ksalfsdfs")

if lurl is None:
    print("Home")
else:
    print(lurl)
