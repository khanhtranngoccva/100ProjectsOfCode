import os
import random
import re
from collections import Counter

os.chdir(os.path.realpath(os.path.dirname(__file__)))


def ipv4_generator():
    while True:
        ip = random.randrange(0, 256 ** 4)
        # print(ip)
        w = int(ip // 16777216) % 256
        x = int(ip // 65536) % 256
        y = int(ip // 256) % 256
        z = int(ip) % 256
        ipv4_address = f"{w}.{x}.{y}.{z}"
        yield ipv4_address


def ip_to_number(ip_addr: str):
    input_ = list(map(int, ip_addr.split(".")))
    return sum(v * 256 ** i for i, v in enumerate(reversed(input_)))


def convert_to_int(val):
    try:
        return int(val)
    except:
        return val


with open("IP2LOCATION-LITE-DB1.CSV") as file:
    ip_database = file.read()

processed_ip_database = [tuple(map(convert_to_int, eval(f"[{row}]"))) for row in ip_database.split("\n") if row]


def lookup(ip_addr="8.8.8.8"):
    ip_num = ip_to_number(ip_addr)
    for entry in processed_ip_database:
        if entry[0] <= ip_num <= entry[1]:
            return entry[3]
    else:
        return None


a = ipv4_generator()

ip_input = [next(a) for i in range(20)]
# ip_input = ["27.3.73.93"]
# ip_input = [f'{w}.{x}.{y}.{z}' for w in range(256) for x in range(256) for y in range(256) for z in range(256)]
print(ip_input)

for ip_addr in ip_input:
    print(ip_addr, lookup(ip_addr))
# with open("os.ch")
