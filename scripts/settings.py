# settings.py
import os


BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

DBNAME = os.path.join(BASE_DIR, 'db', 'temperatures_log.db')

DEVICEFILE_FORMAT = '/sys/bus/w1/devices/{id}/w1_slave'

DEVICES = [
    {'id': '28-000004c0656e', 'label': 'water'},
]

FOOD_SENSORS = [
    {'channel': '17', 'label': 'wafers'},
    {'channel': '23', 'label': 'tablets'},
]

PICAM_PARAMS = ['hflip', 'vflip']
