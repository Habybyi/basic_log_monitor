#!usr/bin/env python3
import re
from datetime import datetime, timedelta
import yaml ; import logging
invalid = 0; valid = 0
words=["failed password"]
activity = {}; actual_activity={}; scores={}
lat_ip = None
pattern_invalid=r"Failed password for invalid user (\w+) from (\S+) port (\d+)"; pattern_valid=r"Failed password for (\w+) from (\S+) port (\d+)"

with open('./config.yml',"r") as f:
    config = yaml.load(f,Loader=yaml.FullLoader)

logging.basicConfig(
            filename=config['log_filename'],
            format=config['log_format'],
            filemode='w',
            level=logging.DEBUG
        )

def scoring(activity, ip):
    score:int = 0; 
    users = activity['users']; times = activity['timestamps']; types=activity['types']
    dlzka:int = len(activity['timestamps']) 
    #scoring by valid/invalid user type
    for i in activity['types']:
        match i:
            case "invalid":
                score += int(config['sc_invalid'])
            case "valid":
                score += int(config['sc_valid'])
    #print(score)
    #scoring by time between the last and first time
    s60 = timedelta(minutes=1)
    s30 = timedelta(seconds=30)
    s10 = timedelta(seconds=10)
    #print(times[-1] - times[0])
    dif = times[-1] - times[0]
    if (dif >= s60) and dlzka >= config['max_per_60']:
        score += config['up_60_bot'] * dlzka
    elif dif >= s60:
        score += config['un_60'] * dlzka
    elif dif <= s30:
        score += config['un_20'] * dlzka
    elif dif <= s10:
        score += config['un_10'] * dlzka
    if ip in scores :
        scores[ip] = scores[ip] + score
    else:
        scores[ip] = score

    score = scores[ip]
    if score >= 120:
        logging.critical(f"{ip} has score {score}. Critical actions needed")
    elif score >= 50 and score < 120:    
        logging.warning(f"{ip} has score {score}. Maybe consider some actions")
    elif score >= 30 and score < 50:
        logging.info(f"{ip} has score {score}. Consider observation")

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
                    match = re.search(pattern_invalid, message)
                else:
                    type = "valid"
                    match = re.search(pattern_valid,message)
                if match:
                    ip = match.group(2); user = match.group(1); port=match.group(3)
                    timestamp = datetime.strptime(f"{datetime.now().year} {month} {day} {time}","%Y %b %d %H:%M:%S")
                   
                    if not ip == lat_ip :
                        if actual_activity:
                            scoring(actual_activity[lat_ip],lat_ip)
                        lat_ip = ip
                        actual_activity[ip] = {
                                'users' : set(),
                                'timestamps' : [],
                                'types' : [],
                                }
                    
                    actual_activity[ip]['users'].add(user)
                    actual_activity[ip]['timestamps'].append(timestamp)
                    actual_activity[ip]['types'].append(type)
                    
                    if ip not in activity:
                        activity[ip] = {
                                'users' : set(),
                                'timestamps':[],
                                'types':[],
                                }            
                    activity[ip]['users'].add(user)
                    activity[ip]['timestamps'].append(timestamp)
                    activity[ip]['types'].append(type)
                
                    print(f"[FAILED][{type.upper()}] {month} {day} {time} - user: {user}, ip: {ip}:{port}")
                else:
                    print("Match was not found")
                    continue
                if type == "valid":
                    valid += 1
                else:
                    invalid += 1
    if ip:
        scoring(actual_activity[ip],ip)
    print(valid, "VALID")
    print(invalid, "INVALID")
print(scores)
