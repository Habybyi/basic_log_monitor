#!usr/bin/env python3
import re
words=["failed","invalid"]
pattern=r"Failed password for invalid user (\w+) from (\S+) port (\d+)"
with open("./test_log.txt","r") as file:
    for line in file:
        if any(word in line.lower() for word in words):
            hlavicka, sprava = line.split("]:",1)
            match = re.search(pattern, sprava)
            if match:
                user = match.group(1)
                ip = match.group(2)
                port = match.group(3)
                month, day, time, hostname, process = hlavicka.split()
                print(user, ip, port)
                print(month, day, time, hostname, process+"]")

