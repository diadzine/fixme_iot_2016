#!/usr/bin/env python
import os
import glob
import time
import subprocess
import settings
import sqlite3


# load the kernel modules needed to handle the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def read_temp_raw(devicefile):
    try:
        with open(devicefile, 'r') as fileobj:
            lines = fileobj.readlines()
        return lines
    except:
        return None


def read_temp(devicefile):
    lines = read_temp_raw(devicefile)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(devicefile)

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
	return temp_c


def log_temperatures(temps):
    try:
        dbname = getattr(settings, 'DBNAME', None)
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        for temp in temps:
            curs.execute("INSERT INTO temperatures VALUES ((?), datetime('now'), (?))", (temp["id"], temp["value"],))

        # commit the changes
        conn.commit()
        conn.close()
        
    except Exception as e:
        print 'Error: %s' % e


if __name__ == '__main__':
    try:
        devicefile = settings.DEVICEFILE_FORMAT

        temps = []
        for device in getattr(settings, 'DEVICES', None):
            temp = read_temp(devicefile.format(id=device["id"]))
            temps.append(dict(id=device["id"], value=temp))

        log_temperatures(temps)
    except Exception as e:
        print 'Error: %s' % e


