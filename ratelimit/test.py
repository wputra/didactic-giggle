#!/usr/bin/python3
import datetime
import pytz
import dateutil.parser

def convert_unix_timestamp(datestring):
    format = '[%d/%b/%Y:%H:%M:%S%z]'
    d = datetime.datetime.strptime(datestring, format)
    #d = d.replace(tzinfo=utc) - d.utcoffset()
    return d

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
