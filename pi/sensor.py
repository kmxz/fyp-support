import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library

# SENSOR 1:                                #Pin 9 for GND
TRIG_1 = 4                                 #Associate pin 7 to TRIG
ECHO_1 = 17                                #Associate pin 11 to ECHO

# SENSOR 2:                                #Pin 20 for GND
TRIG_2 = 24                                #Associate pin 18 to TRIG
ECHO_2 = 25                                #Associate pin 22 to ECHO

# SENSOR 3:                                #Pin 14 for GND
TRIG_3 = 18                                #Associate pin 12 to TRIG
ECHO_3 = 23                                #Associate pin 16 to ECHO
 
print "Distance measurement in progress"

def sense (TRIG, ECHO):

  GPIO.setmode(GPIO.BCM)                   #Set GPIO pin numbering 

  GPIO.setup(TRIG,GPIO.OUT)                #Set pin as GPIO out
  GPIO.setup(ECHO,GPIO.IN)                 #Set pin as GPIO in

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print "Waitng For Sensor To Settle"
  time.sleep(0.5)                          #Delay of 0.5 seconds

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  if distance > 2 and distance < 400:      #Check whether the distance is within range
    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
  else:
    print "Out Of Range"                   #display out of range

  GPIO.cleanup()

while True:
  print "Sensor 1"
  sense(TRIG_1, ECHO_1)  
  print "Sensor 2"
  sense(TRIG_2, ECHO_2)  
  print "Sensor 3"
  sense(TRIG_3, ECHO_3)  
