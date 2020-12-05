from flask import Flask, request, render_template, redirect
from urllib.parse import urlparse
from envparse import env
import string
import random
import time
import redis


str_encode = str.encode
app = Flask(__name__)
host = env('FLASK_APP_HOST')
cache = redis.Redis(host='redis', port=6379)
cache_read = redis.Redis(host='redis_read', port=6379)


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


@app.route('/')
def hello():
    return 'Hello from Docker!!\n'

@app.route('/newurl', methods=['GET', 'POST'])
def newurl():
    if request.method == 'POST':
        lurl = str_encode(request.form.get('url'))

        while True:
            surl = short_url_generator()
            if cache_read.get(surl) is None:
                break

        set_url(surl, lurl)

        return render_template('home.html', short_url = host + surl), 201

    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    try:
        lurl = cache_read.get(short_url)
        if lurl is None:
            lurl = host + "newurl"  # fallback if no URL is found

        return redirect(lurl, code=304)
    except redis.exceptions.ConnectionError as exc:
        if retries == 0:
            raise exc
        retries -= 1
        time.sleep(0.5)


if __name__ == '__main__':
    app.run(debug=True)
