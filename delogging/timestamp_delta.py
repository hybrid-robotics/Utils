#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv
import datetime

usage = """

This script plots the time difference between the current and the previous sample's timestamp
and prints the mean of these delta values to the terminal.

To extract the timestamps you want to plot, e.g. for the imu timestamps, invoke

    pocolog imu.log -s /imu_stim300.orientation_samples_out --fields time > timestamps.txt

and plot the timestamp delta via

    python timestamp_delta.py timestamps.txt

"""

if len(argv) == 2:
    script, filename = argv
else:
    print(usage)
    exit()

fields = [ "timestamp" ]
readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        regex = re.match('^(\d+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            readings.append(dict(zip(fields, values)))

x = []
y = []

plot_outputs = ["timestamp_delta"]

timestamp_start = float(int(readings[0]["timestamp"]) / 1000000.0)
timestamp_end = float(int(readings[len(readings) - 1]["timestamp"]) / 1000000.0)

time_start = datetime.datetime.fromtimestamp(timestamp_start).strftime("%H:%M:%S")
time_end = datetime.datetime.fromtimestamp(timestamp_end).strftime("%H:%M:%S")

frequency = len(readings) / (timestamp_end - timestamp_start)

print "Name: %s, log start: %s, log end: %s, frequency: %.3f" % (filename, time_start, time_end, frequency)

for i in range(1,len(readings)):
    x.append(datetime.datetime.fromtimestamp(float(int(readings[i]["timestamp"]) / 1000000.0)))
    y.append(int(readings[i]["timestamp"]) - int(readings[i-1]["timestamp"]) )

plt.title(filename)
plt.ylabel("Timestamp Delta [usecs]")
plt.xlabel("Time [date]")
plt.plot(x, y, marker='o')
plt.legend(plot_outputs)
plt.show()
