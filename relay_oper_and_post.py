import RPi.GPIO as GPIO
import requests
import time
import logging
from settings import settings


def read_duration(_settings):
    params = {"api_key": _settings['read_key'], "results": 1}
    final_read_url = _settings['read_url'] + str(_settings['read_channel_id']) + '/fields/1.json'
    response = requests.get(final_read_url, params=params)
    data = response.json()
    print(data)
    return int(data['feeds'][0]['field1'])


def write_duration(_settings, _duration):
    params = {"api_key": _settings['write_key'], "field1": _duration}
    response = requests.get(_settings['write_url'], params=params)


logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.warning('This will get logged to a file')

try:
    duration = read_duration(settings)
except:
    print('An exception occurred')
    duration = settings['default_duration']

if 0 >= duration >= 300:
    duration = settings['default_duration']

try:
    write_duration(settings, duration)
except:
    print('An exception occurred')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(settings['pin_out'], GPIO.OUT)
print("Setting low")
GPIO.output(settings['pin_out'], GPIO.LOW)
time.sleep(1)
print("Setting high")
GPIO.output(settings['pin_out'], GPIO.HIGH)
time.sleep(duration)
print("Setting low")
GPIO.output(settings['pin_out'], GPIO.LOW)
print(duration)
