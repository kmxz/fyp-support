#!/usr/bin/env python

from communication import Communication
from ultrasonic import Ultrasonic
from qr import QR
from pservo import PServo

# pin connections (refer to http://goo.gl/a9SVCb please)
#         [ 1][ 2]$-VCC(Sensors)
#         [ 3][ 4]$-S-5V
#         [ 5][ 6]$-S-GND
# 1-TRIG-$[ 7][ 8]
#  1-GND-$[ 9][10]
# 1-ECHO-$[11][12]$-3-TRIG
#         [13][14]$-3-GND
#  S-PWM-$[15][16]$-3-ECHO
#         [17][18]$-2-TRIG
#         [19][20]$-2-GND
#         [21][22]$-2-ECHO
#         [23][24]
#         [25][26]

# UltraSonic Sensors
#usss = [Ultrasonic(4, 17),  Ultrasonic(24, 25),  Ultrasonic(18, 23)]
usss = [Ultrasonic(4, 17),  Ultrasonic(24, 25),  Ultrasonic(18, 23)]

# QR code scanner
qr = QR()

# PWM Servo testing
pservo = PServo(22)

# Communication service
comm = Communication(usss, qr, pservo)

# Start all threads

for uss in usss:
    uss.start()

qr.start()

comm.start()
