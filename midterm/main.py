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
import ubinascii, ujson, urequests, utime, math

Key = 'bNi6jbO9pZYEvKqjxCbYwplIEcwB9oFhv-ARUmyC9z'


print("Setting up Sensors")
driver = Motor(Port.D)
thrower = Motor(Port.C)
eyes = UltrasonicSensor(Port.S4)
filename = 'trainingdata'
f = open(filename + '.txt', "r")
data = []
j = 0
for line in f:
    j += .3332
    line = line.split(",")
    data.append((math.floor(j),float(line[1])))
f.close()
print(data)

def k_nearest_neighbor(data, val, neighbs):
    dist = []
    for data in data:
        euclid = 0
        dist.append((abs(data[1]-val), data[0]))
    dist.sort()
    print(dist)
    speds = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(neighbs):
        labl = int(dist[i][1])
        speds[labl] += 1

    index = 0
    maxval = 0
    print(speds)
    for i, val in enumerate(speds):
        if val > maxval:
            maxval = val
            index = i
    if index == 0:
        spd = 180
    elif index == 1:
        spd = 200
    elif index == 2:
        spd = 225
    elif index == 3:
        spd = 250
    elif index == 4:
        spd = 275
    elif index == 5:
        spd = 300
    elif index == 6:
        spd = 350
    elif index == 7:
        spd = 400
    elif index == 8:
        spd = 450
    elif index == 9:
        spd = 500
    elif index == 10:
        spd = 550
    elif index == 11:
        spd = 600
    elif index == 12:
        spd = 650
    elif index == 13:
        spd = 700
    elif index == 15:
        spd = 750

    return spd


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

def move_closer(dist):
    if dist < 10:
        return
    difference = dist%10
    print(dist)
    goaldist =  dist - difference
    distn = get_sensor_value()
    print(goaldist)
    while distn >= goaldist:
        print(distn)
        wait(50)
        driver.dc(30)
        distn = get_sensor_value()
    driver.stop()



url, headers = setup_systemlink()
print("SETUP SYSLINK")
wait(500)
dis = get_sensor_value()
wait(50)
rep = send_to_system_link('DIST', 'STRING', str(dis))
mode = get_from_system_link('MODE')
wait(50)
if mode == '0':
    print("MODE IS PHYSICS")
    spd = physics_model(dis)
    send_to_system_link('SPEED', 'STRING', str(int(spd)))
elif mode == '1':
    print("MODE IS AI")
    dist = get_sensor_value()
    spd = k_nearest_neighbor(data, dist, 3)
    send_to_system_link('SPEED', 'STRING',str(int(spd)))
else:
    print("MODE IS MOVE CLOSER")
    move_closer(dis)
    dist = get_sensor_value()
    spd = physics_model(dist)
    rep = send_to_system_link('SPEED', 'STRING', str(int(spd)))
    print(rep)
go = False
while go == False:
    dis = get_sensor_value()
    wait(50)
    rep = send_to_system_link('DIST', 'STRING', str(dis))
    throw = get_from_system_link('THROW')
    if throw == 'false':
        go = True
        print("THROWING OBJECT")
        throw_object(spd)
