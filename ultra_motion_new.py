from gpiozero import MotionSensor
import time
import RPi.GPIO as GPIO
import cv2

motion_count = 0
idle_count = 0

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


def standby():
    # print("~~~ ENTERING STANDBY. VARIABLES RESET")
    time.sleep(1)
    pir = MotionSensor(4) # MotionSensor (GPIO PIN Number)
    print("STBY\t: MOTION")
    pir.wait_for_motion()
    distance()
    print("TRIG\t: MOTION SENSOR")
    time.sleep(0.5)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 3
GPIO_ECHO = 2
image_counter = 0

 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
standby()

def start_camera(img):
    image_counter = img
    # sudo modprobe bcm2835-v412
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    # cv2.imshow('frame', frame)
    img_filename = "capture_{}.png".format(image_counter)
    cv2.imwrite(img_filename, frame)
    image_counter += 1
    print("File {} written".format(img_filename))
    capture.release()
    cv2.destroyAllWindows()
    print("SEND >> STBY\n")
    time.sleep(1)
 
if __name__ == '__main__':
    
    try:
        
        time.sleep(0.5)
        
        while True:
            print("TRIG\t: ULTRASONIC")
            dist = distance()
            if dist < 125:
                idle_count = 0
                if motion_count > 10:
                    # Activate Camera
                    print("\nTRIG\t: CAMERA")
                    start_camera(image_counter)
                    image_counter += 1
                    motion_count = 0
                    standby()
                    
                else:
                    motion_count += 1
                    # print ("Measured Distance = %.1f cm" % dist)
                    print("ENGAGE CAM IN " + str(11-motion_count))
                    idle_count = 0
                
            else:
                motion_count = 0
                if idle_count > 10:
                    # Put sensors in Standby Mode
                    print("NO MOVEMENT TIMEOUT")
                    idle_count = 0
                    standby()
                    
                else:
                    idle_count += 1
                    # print("Idle " + str(idle_count))
                    
            time.sleep(0.2)
 

# Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("### STOP ###")
        #GPIO.cleanup()