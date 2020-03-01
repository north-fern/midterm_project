#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Write your program here
ev3 = EV3Brick()
import ubinascii, ujson, urequests, utime

Key = 'bNi6jbO9pZYEvKqjxCbYwplIEcwB9oFhv-ARUmyC9z'


print("Setting up Sensors")
driver = Motor(Port.D)
thrower = Motor(Port.C)
eyes = UltrasonicSensor(Port.S4)


def setup_systemlink():
    print("SETTING UP SYSTEMLINK")
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags"
    headers = {"Accept": "application/json", "x-ni-api-key": Key}
    return urlBase, headers


def send_to_system_link(Tag, Type, Value):
    print("Sending to system link")
    urlBase, headers = setup_systemlink()
    urlVal = urlBase + Tag + "/values/current"
    propVal = {"value":{"type": Type, "value": Value}}
    try:
        reply = urequests.put(urlVal, headers = headers, json = propVal).text
    except Exception as e:
        print(3)
        reply = 'failed'
    return reply

def get_from_system_link(Tag):
    urlBase, headers = setup_systemlink()
    urlVal = urlBase + Tag + "/values/current"
    try:
        value = urequests.get(urlVal, headers = headers).text
        data = ujson.loads(values)
        print(data)
        result = data.get("value").get("value")
    except Exception as e:
        print(e)
        result = 'failed'
    return result

def get_sensor_value():
    dist = eyes.distance()
    print("Distnce is: " , dist/10)
    return dist/10

def throw_object(distance):
    print("throwing object")
    thrower.run(600)
    wait(1500)


url, headers = setup_systemlink()
wait(1000)
dis = get_sensor_value()
send_to_system_link("DISTANCE", "INTEGER", dis)
mode = get_from_system_link("MODE")
    if mode == 0:
        print("MODE IS PHYSICS")
    elif mode == 1:
        print("MODE IS AI")
    elif mode == 2:
        print("MODE IS MOVE CLOSER")
go = False
while go == False:
    throw = get_from_system_link("THROW")
    if throw == 'false':
        go = True
        print("THROWING OBJECT")
#throw_object(4)
