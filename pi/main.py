import threading
import ultrasonic.Ultrasonic as Ultrasonic

# <- board
#         [ 1][ 2]$ VCC
#         [ 3][ 4]
#         [ 5][ 6]
#         [ 7][ 8]
# 1-TRIG $[ 9][10]
#  1-GND $[11][12]$ 3-TRIG
# 1-ECHO $[13][14]$ 3-GND
#         [15][16]$ 3-ECHO
#         [17][18]$ 2-TRIG
#         [19][20]$ 2-GND
#         [21][22]$ 2-ECHO
#         [23][24]
#         [25][26]

# UltraSonic SensorS
usss = [Ultrasonic(4, 17),  Ultrasonic(24, 25),  Ultrasonic(18, 23)]

