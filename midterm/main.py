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
    #print("SETTING UP SYSTEMLINK")
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
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
        print(e)
        reply = 'failed'
    return reply

def get_from_system_link(Tag):
    urlBase, headers = setup_systemlink()
    urlVal = urlBase + Tag + "/values/current"
    try:
        value = urequests.get(urlVal, headers = headers).text
        data = ujson.loads(value)
        #print(data)
        result = data.get("value").get("value")
    except Exception as e:
        print(e)
        result = 'failed'
    return result

def get_sensor_value():
    dist = eyes.distance()
    print("Distance is: " , dist/10)
    return dist/10

def throw_object(spd):
    print("throwing object")
    thrower.run(spd)
    wait(4000*(100/spd))

def physics_model(dist):
    dist = dist / 100
    spd = (dist * 9.81 / (.90189))**(1/2)
    spd = (spd * 180 / (.14 * 3.141592653)) -110 ## correction factor from testing
    # eqns based on http://aboutscience.net/projectile-motion-equations/
    print(spd)
    return spd




# url, headers = setup_systemlink()
# print("SETUP SYSLINK")
# wait(1000)
# dis = get_sensor_value()
# wait(1000)
# rep = send_to_system_link('DIST', 'STRING', str(dis))
# print(rep)
# print("SENT SENSOR VALUE")
# mode = get_from_system_link('MODE')
# print(type(mode))
# print("GOT MODE")
# if mode == '0':
#     print("MODE IS PHYSICS")
#     spd = physics_model(dis)
# elif mode == '1':
#     print("MODE IS AI")
#     spd = 600
# else:
#     print("MODE IS MOVE CLOSER")
#     spd = 600
# go = False
# while go == False:
#     throw = get_from_system_link('THROW')
#     if throw == 'false':
#         go = True
#         print("THROWING OBJECT")
#         throw_object(spd)
dist = get_sensor_value() / 10
print(dist)
throw_object(350)