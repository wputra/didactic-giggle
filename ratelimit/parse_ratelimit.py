#!/usr/bin/python3
import datetime
import pytz
import redis

def convert_unix_timestamp(datestring):
    d = datetime.datetime.strptime(datestring, format)
    d = d.astimezone(utc)
    ts = (d - epoch).total_seconds()
    return ts

def request_is_limited(t, key, limit, period, ban):
    period_in_seconds = period.total_seconds()
    ban_in_seconds = ban.total_seconds()
    separation = period_in_seconds / limit
    r.setnx(key, 0)
    r.setnx(key+"_start", t)
    input_t = t
    try:
        with r.lock('lock:' + key, blocking_timeout=5) as lock:
            t = min(float(r.get(key+"_start")), t)
            tat = max(float(r.get(key)), t)
            if tat - t <= period_in_seconds - separation:
                new_tat = max(tat, t) + separation
                r.set(key, new_tat)
                return False
            else:
                r.set(key, t + ban_in_seconds)
                r.set(key+"_start", input_t)
            return True
    except LockError:
        return True

def parse_input(input_file):
    with open(input_file, 'r') as in_file:
        for line in in_file:
            log_list = line.split()

            log_timestamp = log_list[3] + log_list[4]
            timestamp = convert_unix_timestamp(log_timestamp)

            ip = log_list[0]
            if request_is_limited(timestamp, ip+"_1m", 40, datetime.timedelta(minutes=1), datetime.timedelta(minutes=10)):
                decision = "BAN"
            elif request_is_limited(timestamp, ip+"_10m", 100, datetime.timedelta(minutes=10), datetime.timedelta(minutes=60)):
                decision = "BAN"
            else:
                decision = "UNBAN"

            path = log_list[6]
            if path == "/login":
                if request_is_limited(timestamp, ip+"_login", 20, datetime.timedelta(minutes=10), datetime.timedelta(minutes=120)):
                    decision = "BAN"
                else:
                    decision = "UNBAN"

            print(f'{int(timestamp)},{decision},{ip}')


# main
format = '[%d/%b/%Y:%H:%M:%S%z]'
utc = pytz.UTC
epoch = datetime.datetime(1970,1,1,0,0,0,tzinfo=utc)
r = redis.Redis(host='localhost', port=6379, db=0)
parse_input("test.log")
