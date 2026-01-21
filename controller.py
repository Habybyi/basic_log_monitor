#!usr/bin/env python3
import re
from datetime import datetime
from datetime import timedelta
import yaml
invalid = 0; valid = 0
words=["failed password"]
activity = {}
pattern_invalid=r"Failed password for invalid user (\w+) from (\S+) port (\d+)"; pattern_valid=r"Failed password for (\w+) from (\S+) port (\d+)"

with open('./config.yml',"r") as f:
    config = yaml.load(f,Loader=yaml.FullLoader)

def check_algorithm(times, type, user, ip):
    window = timedelta(config['window'])
    limit=config['limit']
    
with open("./test_log.txt","r") as file:
    for line in file:
        if "]:" not in line:
            continue
        else:
            header, message = line.split("]:",1)
            if any(word in message.lower() for word in words):
                month, day, time, hostname, process = header.split()
                if "invalid user" in message.lower():
                    type = "invalid"
                else:
                    type = "valid"
                if type == "valid":
                    match = re.search(pattern_valid, message)
                elif type == "invalid":
                    match = re.search(pattern_invalid,message)

                if match:
                    ip = match.group(2); user = match.group(1); port=match.group(3)
                    timestamp = datetime.strptime(f"{datetime.now().year} {month} {day} {time}","%Y %b %d %H:%M:%S")
                    if ip not in activity:
                        activity[ip] = {
                                'users_tried' : set(),
                                'timestamps':[],
                                'types':[]
                            }
                    print(f"[FAILED][{type.upper()}] {month} {day} {time} - user: {user}, ip: {ip}:{port}")
                else:
                    print("match was not found")
                    continue
                if type == "valid":
                    valid += 1
                else:
                    invalid += 1
    print(valid, "VALID")
    print(invalid, "INVALID")
