#!usr/bin/env python3
import re
from datetime import datetime
invalid = 0; valid = 0
words=["failed password"]
pokusy_ip = {}; pokusy_user = {}; datetimes_ip = {}
pattern_invalid=r"Failed password for invalid user (\w+) from (\S+) port (\d+)"; pattern_valid=r"Failed password for (\w+) from (\S+) port (\d+)"
with open("./test_log.txt","r") as file:
    for line in file:
        if "]:" not in line:
            continue
        else:
            hlavicka, sprava = line.split("]:",1)
            if any(word in sprava.lower() for word in words):
                month, day, time, hostname, process = hlavicka.split()
                if "invalid user" in sprava.lower():
                    type = "FAILED_PASSWORD_INVALID_USER"
                    match = re.search(pattern_invalid, sprava)
                    if match:
                        ip = match.group(2); user = match.group(1)
                        if ip not in pokusy_ip:
                            pokusy_ip[ip] = 1
                        else:
                            pokusy_ip[ip] += 1
                        if user not in pokusy_user:
                            pokusy_user[user] = 1
                        else:
                            pokusy_user[user] += 1
                        timestamp = datetime.strptime(f"{month} {day} {time}", "%b %d %H:%M:%S").replace(year=datetime.now().year)
                        if ip not in datetimes_ip:
                            datetimes_ip[ip] = [timestamp]
                        else:
                            datetimes_ip[ip].append(timestamp)
                        print(f"[FAILED][INVALID] {month} {day} {time} - user: {match.group(1)}, ip: {match.group(2)}:{match.group(3)}")
                    else:
                        print("match was not found")
                        continue
                    invalid += 1
                else:
                    type = "FAILED_PASSWORD_VALID_USER"
                    match = re.search(pattern_valid, sprava)
                    if match:
                        ip = match.group(2); user = match.group(1)
                        if ip not in pokusy_ip:
                            pokusy_ip[ip] = 1
                        else:
                            pokusy_ip[ip] += 1
                        if user not in pokusy_user:
                            pokusy_user[user] = 1
                        else:
                            pokusy_user[user] += 1
                        if ip not in datetimes_ip:
                            datetimes_ip[ip] = [timestamp]
                        else:
                            datetimes_ip[ip].append(timestamp)
                        print(f"[FAILED][VALID] {month} {day} {time} - user: {match.group(1)}, ip: {match.group(2)}:{match.group(3)}")
                    else:
                        print("match was not found")
                        continue
                    valid += 1
    print(valid, "VALID")
    print(invalid, "INVALID")
    print(pokusy_ip)
    print(pokusy_user)
    print(datetimes_ip)

def ulozene(ip,user):
    if ip not in pokusy_ip:
        pokusy_ip[ip] = 1
    else:
        pokusy_ip[ip] += 1
    if user not in pokusy_user:
        pokusy_user[user] = 1
    else:
        pokusy_user[user] += 1
