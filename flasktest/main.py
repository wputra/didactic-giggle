from flask import Flask, request, render_template, redirect
import string
import random
import time
import redis

app = Flask(__name__)
host = 'http://192.168.77.10:5000/'
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

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
    count = get_hit_count()
    return 'Hello from Docker!! I have been seen {} times.\n'.format(count)

@app.route('/newurl', methods=['GET', 'POST'])
def newurl():
    if request.method == 'POST':
        surl = short_url_generator()
        lurl = str_encode(request.form.get('url'))

        set_url(surl, lurl)

        return render_template('home.html', short_url = host + surl)

    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    lurl = host + "/newurl"  # fallback if no URL is found

    try:
        lurl = cache.get(short_url)
        return redirect(lurl)
    except OverflowError as e:
        print(str(e))


if __name__ == '__main__':
    app.run(debug=True)
