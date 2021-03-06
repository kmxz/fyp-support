#!/usr/bin/env python

from communication import WsReceiver
from ultrasonic import Ultrasonic
from qr import QR, Program
import RPi.GPIO as GPIO
from pservo import Turning
from switch import Switch
from time import sleep
import sys

# pin connections (refer to http://goo.gl/a9SVCb please)
# 1-, 2-, 3- stands for ultrasonic sensors
# S- stands for servo
# M- stands for motor switch
# F- stands for flight controller board
#          [ 1][ 2]$-VCC(Sensors)
#          [ 3][ 4]$-S-5V
#          [ 5][ 6]$-S-GND
#  1-TRIG-$[ 7][ 8]$-S-PWM
#   1-GND-$[ 9][10]
#  1-ECHO-$[11][12]$-3-TRIG
#          [13][14]$-3-GND
#          [15][16]$-3-ECHO
#          [17][18]$-2-TRIG
#          [19][20]$-2-GND
#          [21][22]$-2-ECHO
#          [23][24]
#          [25][26]
#          [27][28]
#          [29][30]
# B-THROT-$[31][32]
#  B-ROLL-$[33][34]$-M-GND
# B-PITCH-$[35][36]$-M-SIG
#   B-YAW-$[37][38]
#   B-GND-$[39][40]

if len(sys.argv) >= 2 and ("-n" in sys.argv[1]):
    pass
else:
    print "Run with -n to remove 10 sec delay before start!"
    sleep(10)

GPIO.setmode(GPIO.BCM) # set GPIO pin numbering

# UltraSonic Sensors
#usss = [Ultrasonic(4, 17),  Ultrasonic(24, 25),  Ultrasonic(18, 23)]
usss = []

# PWM Servo
turning = Turning(14)

# Switch for DC motor
switch = Switch(26)

# program flow
program = Program(switch, turning)

# QR code scanne
qr = QR(switch, program)

# Communication service
comm = WsReceiver(usss, qr, turning, switch, program)

# Start all threads

for uss in usss:
    uss.start()

qr.start()

comm.start()
