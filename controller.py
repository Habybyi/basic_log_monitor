#!usr/bin/env python3
import re
from datetime import datetime
from datetime import timedelta
invalid = 0; valid = 0
words=["failed password"]
pokusy_ip = {}; pokusy_user = {}; datetimes_ip = {}
activity = {}
pattern_invalid=r"Failed password for invalid user (\w+) from (\S+) port (\d+)"; pattern_valid=r"Failed password for (\w+) from (\S+) port (\d+)"

sus_act={}
def check_times_ip(times, type, user, ip):
    window = timedelta(minutes=5)
    limit=3
    count=0 
    latest = times[-1]
    print("type >>", type)
    start= latest - window
    print("user >>",user)

    for t in times:
        if t >= start:
            count += 1
        if ip not in sus_act:
            sus_act[ip] = [[user, [t]]]
        elif ip in sus_act:
            for i in sus_act[ip]:
                if user not in i:
                    sus_act[ip].append([user, [t]])
                elif user in i:
                    i[i.index(user)+1].append(t)

    if (type == "valid" and count < 4):
        return False
    elif (type == "valid" and count >=4):
        return True
    
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
                    if user not in activity:
                        activity[user] = [[ip,[timestamp]]]
                    else:
                        found=False
                        for i in activity[user]:
                            if i[0] ==ip:
                                i[1].append(timestamp)
                                found=True
                                break
                        if not found:
                            activity[user].append([ip,[timestamp]])
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
    print(activity)
