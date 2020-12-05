#!/usr/bin/python3

def convert_unix_timestamp(arg):
    pass

def parse_input(input_file):
    with open(input_file, 'r') as in_file:
        for line in in_file:
            log_list = line.split()
            timestamp = log_list[3].strip("[")
            ip = log_list[0]
            decision = "BAN"
            print(timestamp, decision, ip)


# main
parse_input("test.log")
