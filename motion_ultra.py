#!/usr/bin/python

from gpiozero import MotionSensor
import time
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 3
GPIO_ECHO = 2
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


pir = MotionSensor(4) # MotionSensor (GPIO PIN Number)
n = 0
presence = 0

pir.wait_for_motion()
distance()
print("You Moved " + str(n))
presence += 1
n += 1
        
time.sleep(0.5)
 
if __name__ == '__main__':
    
    try:
        motion_count = 0
        idle_count = 0
        while True:
            dist = distance()
            if dist < 125:
                if motion_count > 50:
                    # Activate Camera
                    print("Activate Camera")
                else:
                    motion_count += 1
                    print ("Measured Distance = %.1f cm" % dist)
                    print("Move " + str(motion_count))
                    idle_count = 0
                
            else:
                if idle_count > 50:
                    # Put sensors in Standby Mode
                    print("STANDBY")
                else:
                    idle_count += 1
                    print("Idle " + str(idle_count))
                    motion_count = 0
            time.sleep(0.1)
 

# Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        #GPIO.cleanup()

