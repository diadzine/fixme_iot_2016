#!/usr/bin/env python
import time
import subprocess
import settings
import sqlite3
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
FOOD_STATES = getattr(settings, 'FOOD_STATES', None)
FOOD_SENSORS = getattr(settings, 'FOOD_SENSORS', None)


def setup_sensors():
    for sensor in FOOD_SENSORS:
        GPIO.setup(
            sensor['channel'],
            GPIO.IN,
            pull_up_down=GPIO.PUD_DOWN
        )
        GPIO.add_event_detect(
            sensor['channel'],
            GPIO.BOTH,
            callback=food_callback,
            bouncetime=200
        )


def food_state_log(channel, state):
    try:
        dbname = getattr(settings, 'DBNAME', None)
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        curs.execute(
            "INSERT INTO food_status VALUES ((?), datetime('now'), (?))",
            (channel, FOOD_STATES[state],)
        )

        # commit the changes
        conn.commit()
        conn.close()

    except Exception as e:
        print 'Error: %s' % e


def food_up(channel):
    food_state_log(channel, 'UP')


def food_back(channel):
    food_state_log(channel, 'BACK')
    subprocess.call("./picam_animation.py")


def food_callback(channel):
    time.sleep(0.1)

    if GPIO.input(channel):
        # Food are back
        food_back(channel)
    else:
        # Food have been picked up
        food_up(channel)


if __name__ == '__main__':
    try:
        setup_sensors()
    except Exception as e:
        print 'Error: %s' % e
S
