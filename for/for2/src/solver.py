#!/usr/bin/env python3
from IPython import embed
import struct

lines = []
with open("ip_addresses.txt") as f:
    lines = [x.strip().split(".") for x in f.readlines()]
coords = []
for line in lines:
    coords.append(''.join([hex(int(y))[2:].zfill(2) for y in line]))

coords2 = [struct.unpack(">f", bytes.fromhex(x))[0] for x in coords]

for i in range(0, len(coords2), 2):
    print("{} {}".format(coords2[i], coords2[i+1]))

embed(banner1='')

