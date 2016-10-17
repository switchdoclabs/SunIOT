#
#
# SunIOT - SwitchDoc Labs
#
# October 2016
#
import sys
import os

sys.path.append('./SDL_Pi_SI1145');
import time

import RPi.GPIO as GPIO


#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

LED = 4

GPIO.setup(LED, GPIO.OUT, initial=0)

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


import SDL_Pi_SI1145

sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()
#LED Line definitation (BCM Model)

# setup apscheduler

def tick():
    print('Tick! The time is: %s' % datetime.now())


def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown...."
    exit()

def blinkLED(times,length):

	for i in range(0, times):
		GPIO.output(LED, 1)
		time.sleep(length)
		GPIO.output(LED, 0)
		time.sleep(length)



def readSunLight():
	
        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        print('SunLight Sensor read at time: %s' % datetime.now())
        print '		Vis:             ' + str(vis)
        print '		IR:              ' + str(IR)
        print '		UV Index:        ' + str(uvIndex)

	blinkLED(2,0.200)

	returnValue = []
	returnValue.append(vis)
	returnValue.append(IR)
	returnValue.append(uvIndex)
	return returnValue


print "-----------------"
print "SunIOT"
print ""
print "SwitchDoc Labs" 
print "-----------------"
print ""


if __name__ == '__main__':

    	scheduler = BackgroundScheduler()


	# DEBUG Mode - because the functions run in a separate thread, debugging can be difficult inside the functions.
	# we run the functions here to test them.
	#tick()
	#print readSunLight()
	


	# prints out the date and time to console
    	scheduler.add_job(tick, 'interval', seconds=60)
    	# blink life light
	scheduler.add_job(blinkLED, 'interval', seconds=5, args=[1,0.250])

	# IOT Jobs are scheduled here (more coming next issue) 
	scheduler.add_job(readSunLight, 'interval', seconds=10)
	
    	# start scheduler
	scheduler.start()
	print "-----------------"
	print "Scheduled Jobs" 
	print "-----------------"
    	scheduler.print_jobs()
	print "-----------------"

    	print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    	try:
        	# This is here to simulate application activity (which keeps the main thread alive).
        	while True:
            		time.sleep(2)
    	except (KeyboardInterrupt, SystemExit):
        	# Not strictly necessary if daemonic mode is enabled but should be done if possible
        	scheduler.shutdown
