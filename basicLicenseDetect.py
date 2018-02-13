import microgear.client as microgear
import time
import logging
import picamera
import cv2
import RPi.GPIO as GPIO     
            
appid = "Kornbot"
gearkey = "wBHqON1EtNqlTzu"
gearsecret =  "nt0utSlDrPEOiYOFFfHYJDbEw"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
def connection():
    logging.info("License place detector  connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("VisualStudio")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/topic")
microgear.connect(False)

GPIO.setmode(GPIO.BCM)           

TRIG = 18                                  #Associate pin 18 to TRIG
ECHO = 24                                  #Associate pin 24 to ECHO


print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
camera = picamera.PiCamera() 
camera.resolution = (800,600) 

def detector():

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  
  time.sleep(2)                            #Delay of 2 seconds

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

  if distance > 20 and distance < 50:      #Check whether the distance is within range
                                           #Print distance with 0.5 cm calibration
    camera.capture('license.jpg',resize=(640,480)) 
    camera.start_preview() 
    time.sleep(5) 
    camera.stop_preview() 
    return distance - 0.5 
  else:

    print "Out Of Range"                   #display out of range

	
while True: 
 
  microgear.chat("VisualStudio",detector())


