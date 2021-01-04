try:
	import RPi.GPIO as GPIO
except:
	class GPIO :
		def setwarnings( enable ):
			return
		def setmode( mode ):
			return
		def setup( pin, mode, initial ):
			return
		def output( pin, level):
			return
	pass

import sys
import os, re
import time
import fcntl
import threading
import signal


LED_PIN = 14 #TXD
LED_BLINK_PERIOD=0.1
INPUT_DEVICE_PATH="/dev/input/by-path/"
WATCHDOG_RUNPID="/var/run/gamepad_watchdog_pid"

PORT_MANIPULATION_COMMAND="echo {0} > /sys/bus/usb/devices/1-{1}/bConfigurationValue"
INTER_DELAY=0.5

CORRECT_ORDER=['1.2', '1.3', '1.0', '1.1']

#initialize GPIO settings
def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.HIGH)

def ledBlink( seconds ):
	for i in range(int(seconds / LED_BLINK_PERIOD)):
		time.sleep(LED_BLINK_PERIOD / 2)
		GPIO.output(LED_PIN, GPIO.LOW)
		time.sleep(LED_BLINK_PERIOD / 2)
		GPIO.output(LED_PIN, GPIO.HIGH)

def compareOrders( correctOrderList, actualOrder):

	if ( len( actualOrder ) == 0 ):
		return None

	maxKey = max(actualOrder.keys())
	actualOrderList=list()
	for k in sorted(actualOrder.keys()):
		actualOrderList.append( actualOrder[ k ] )

	if ( correctOrderList == actualOrderList and maxKey < len(correctOrderList)):
		return None

	sortedActualOrderList = sorted(actualOrderList)
	if ( sorted(correctOrderList) == sortedActualOrderList ):
		print( 'List are just misordered')
		return correctOrderList

	intersection=list()
	for item in correctOrderList :
		if item in actualOrderList:
			intersection.append( item )
		else:
			break
	
	if (intersection == actualOrderList and maxKey < len(intersection) ):
		return None

	if ( sorted(intersection) == sortedActualOrderList ):
		return intersection

	if ( intersection == correctOrderList ):
		#need to append absent
		reorderNeed=False
		for order in range( len(intersection) ):
			if ( actualOrder[order] != correctOrderList[order] ):
				reorderNeed = True
				break

		if ( not reorderNeed ):
			return None

		for key in actualOrder.keys() :
			if actualOrder[key] not in intersection:
				intersection.append( actualOrder[key] )
		
		return intersection

	return None

def parseInputAndDevice( str ):
	result = re.match( r".*:([^:]+):.*-event.*/event([0-9]+)$", str )
	if ( result and result.lastindex == 2 ):
		return [ int(result.group(2)),  result.group(1) ]
	return None

def getActualOrder():
	
	res = dict()
	try:
		for link in filter( os.path.islink, [ os.path.join( INPUT_DEVICE_PATH, file ) for file in os.listdir(INPUT_DEVICE_PATH) ] ):
			device = parseInputAndDevice( link + os.readlink( link ) )
			if ( device ):
					res[device[0]] = device[1]
	except OSError:
		pass

	return res

def dumpGamePads( d ):
	for i in sorted(d.keys()):
			print( "  Port #{0} is {1}". format(i, d[i]))

def manupulateDevice( devices, enable=1 ):
	for device in devices:
		print("    " + PORT_MANIPULATION_COMMAND.format(enable, device))
		os.system( PORT_MANIPULATION_COMMAND.format(enable, device) )
		if ( enable ) :
			ledBlink( INTER_DELAY )

def doReorderGamepads():
	actualOrder = getActualOrder()
	needReorder = compareOrders( CORRECT_ORDER, actualOrder )
	if ( needReorder ):
		print( "Gamepad misordering is detected: ")
		dumpGamePads( actualOrder )
		
		# poweroff devices
		manupulateDevice( needReorder, enable = 0 )
		# wait after turn off devices
		ledBlink( INTER_DELAY )

		# poweron devices
		manupulateDevice( needReorder, enable = 1 )
		
		actualOrder = getActualOrder()
		needReorder = compareOrders( CORRECT_ORDER, actualOrder )

		if ( not needReorder ) :
			print ( "Gamepad misordered is fixed: " )
		else:
			print ( "Gamepad misordered fix failed: " )
		dumpGamePads( actualOrder )

		print ( "" )

exitFlag=False

def receiveUpdate(signalNumber, frame):
	wakeupEvent.set()
	return

def terminateProcess(signalNumber, frame):
	global exitFlag
	exitFlag=True
	wakeupEvent.set()
	return

def reorderGamepads():
	global exitFlag
	global wakeupEvent
	while not exitFlag :
		wakeupEvent.clear()
		doReorderGamepads()
		wakeupEvent.wait(timeout=600)

if __name__ == "__main__":

	if ( len( sys.argv ) > 1):
		try:
			f=open(WATCHDOG_RUNPID, 'r')
			pid = f.read()
			f.close()
			os.system( "kill -1 " + pid )
		except:
			os._exit(os.EX_OK) 

		os._exit(os.EX_OK) 

	fh=os.open(os.path.realpath(__file__), os.O_RDONLY )
	try:
		fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
	except:
		os._exit(os.EX_USAGE)

	f=open(WATCHDOG_RUNPID, 'w')
	f.write( str(os.getpid()) )
	f.close()
	print("My Pid:" + str(os.getpid()))

	wakeupEvent = threading.Event()
	signal.signal(signal.SIGHUP, receiveUpdate)
	signal.signal(signal.SIGINT, terminateProcess)
	signal.signal(signal.SIGTERM, terminateProcess)
	init()
	reorderProcess = threading.Thread(	name='processing',
								target = reorderGamepads )

	reorderProcess.start()
	while not exitFlag:
		signal.pause()

	reorderProcess.join()
	try:
		os.remove(WATCHDOG_RUNPID)
	except:
		os._exit(os.EX_OK) 

