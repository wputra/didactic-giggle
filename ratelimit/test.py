#!/usr/bin/python3
import datetime
import pytz
import dateutil.parser

def convert_unix_timestamp(datestring):
    format = '[%d/%b/%Y:%H:%M:%S%z]'
    utc = pytz.UTC
    epoch = datetime.datetime(1970,1,1,0,0,0,tzinfo=utc)
    d = datetime.datetime.strptime(datestring, format)
    d = d.astimezone(utc)
    ts = (d - epoch).total_seconds()
    return int(ts)

def parse_input(input_file):
    with open(input_file, 'r') as in_file:
        for line in in_file:
            log_list = line.split()
            log_timestamp = log_list[3] + log_list[4]
            timestamp = convert_unix_timestamp(log_timestamp)
            ip = log_list[0]
            decision = "BAN"
            print(timestamp, decision, ip)


# main
parse_input("test.log")
