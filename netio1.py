# coding=utf-8
import socket
import SocketServer
import os
import RPi.GPIO as GPIO
import time
import serial
import json
import MySQLdb

# Setup serial connection to arduino
DEVICE = "/dev/ttyAMA0"
BAUD = 9600
ser = serial.Serial(DEVICE, BAUD)

#Variables
comingHomeStatus = 0
id = 0
temperature = 0
humidity = 0
solar = 0
line = 0
val = 0

class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for our server.
	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	def handle(self):
		global comingHomeStatus, ser
		while 1:
			# self.request is the TCP socket connected to the client
			self.data = self.request.recv(1024).strip()
			if not self.data: break
			print "Incoming connection from: {}".format(self.client_address[0])
			print "Received data:", self.data
#LED1
			if self.data == 'led1 on':
				#ser.flushOutput()
				ser.write('{"ID":1,"things":"light","command":"on"}')
				print 'received on'
				self.request.sendall('led1 open')
			elif self.data == 'led1 off':
				#ser.flushOutput()
				ser.write('{"ID":1,"things":"light","command":"off"}')
				print 'received off'
				self.request.sendall('led1 close')
#LED2
			if self.data == 'led2 on':
				#ser.flushOutput()
				ser.write('{"ID":2,"things":"light","command":"on"}')
				print 'received on'
				self.request.sendall('led2 open')
			elif self.data == 'led2 off':
				#ser.flushOutput()
				ser.write('{"ID":2,"things":"light","command":"off"}')
				print 'received off'
				self.request.sendall('led2 close')
#Light_W2812
			if self.data == 'white':
				ser.write('{"ID":3,"things":"light","command":"white"}')
				print 'white light'
				self.request.sendall('white')
			elif self.data == 'red':
				ser.write('{"ID":3,"things":"light","command":"red"}')
				print 'red light'
				self.request.sendall('red')
			elif self.data == 'orange':
				ser.write('{"ID":3,"things":"light","command":"orange"}')
				print 'orange light'
				self.request.sendall('orange')
			elif self.data == 'green':
				ser.write('{"ID":3,"things":"light","command":"green"}')
				print 'green light'
				self.request.sendall('green')
			elif self.data == 'blue':
				ser.write('{"ID":3,"things":"light","command":"blue"}')
				print 'blue light'
				self.request.sendall('blue')
			elif self.data == 'black':
				ser.write('{"ID":3,"things":"light","command":"black"}')
				print 'black light'
				self.request.sendall('black')
			elif self.data == 'rainbow':
				ser.write('{"ID":3,"things":"light","command":"rainbow"}')
				print 'rainbow'
				self.request.sendall('rainbow')
			elif self.data == 'strip off':
				ser.write('{"ID":3,"things":"light","command":"off"}')
				print 'strip off'
				self.request.sendall('strip off')
			elif self.data == 'brightness':
				ser.write('{"ID":3,"things":"light","command":"bri","val":val}')
				print 'brightness'
				self.request.sendall('brightness')
#DoubanFM
			if self.data == 'radio on':
				os.system("sudo /etc/init.d/doubanfm start")
			elif self.data == 'radio off':
				os.system("sudo /etc/init.d/doubanfm stop")
				os.system("sudo killall -9 mpg123")
#Get wheather
			if self.data == 'get temperature':
				ser.flushInput()
				line = ser.readline()
				s = json.loads(line)
				temperature = s["temp"]
				print  'read temperature'
				temp = str(temperature)
				self.request.sendall(temp)

			if self.data == 'get humidity':
				#ser.flushInput()
				#line = ser.readline()
				#s = json.loads(line)
				humidity = s["hum"]
				print 'read humidity'
				hum = str(humidity)
				self.request.sendall(hum)

			if self.data == 'get solar':
				#ser.flushInput()
				#line = ser.readline()
				#s = json.loads(line)
				solar = s["solar"]
				print 'read solar'
				sol = str(solar)
				self.request.sendall(sol)
 
### GROUPED LIGHTS
			#Coming-home-lights
			if self.data == 'comingHomeOn':
				self.request.sendall('On')
				GPIO.output(5, True)
				GPIO.output(11, True)
				GPIO.output(12, True)
				comingHomeStatus = 1
			elif self.data == 'comingHomeOff':
				self.request.sendall('Off')
				GPIO.output(5, False)
				GPIO.output(11, False)
				GPIO.output(12, False)
				comingHomeStatus = 0
				
			#Turn all indoor lights off
			if self.data == 'allIndoorLightsOff':
				print "Turning all indoor lights off"
				GPIO.output(5, False)	#Garage roof light
				GPIO.output(7, False)	#Workshop roof light
				GPIO.output(8, False)	#Storage roof light
				self.request.sendall('.')
			#Turn all outdoor lights off
			if self.data == 'allOutdoorLightsOff':				
				print "Turning all outdoor lights off"
				GPIO.output(11, False)	#Driveway light
				GPIO.output(12, False)	#Carport light
				GPIO.output(13, False)	#Workshop light
				GPIO.output(16, False)	#Storage light
				self.request.sendall('.')
				
### INDOOR LIGHTS
			#Garage roof light
			if self.data == 'garageRoofOn':
				print "Turning garage roof light on"
				GPIO.output(5, True)
				self.request.sendall('.')
			elif self.data == 'garageRoofOff':
				print "Turning garage roof light off"
				GPIO.output(5, False)
				self.request.sendall('.')
			
			#Workshop roof light
			if self.data == 'workshopRoofOn':
				print "Turning workshop roof light on"
				GPIO.output(7, True)
				self.request.sendall('.')
			elif self.data == 'workshopRoofOff':
				print "Turning workshop roof light off"
				GPIO.output(7, False)
				self.request.sendall('.')
			#Storage roof light
			if self.data == 'storageRoofOn':
				print "Turning storage roof light on"
				GPIO.output(8, True)
				self.request.sendall('.')
			elif self.data == 'storageRoofOff':
				print "Turning storage roof light off"
				GPIO.output(8, False)
				self.request.sendall('.')						
### OUTDOOR LIGHTS
			#Driveway light
			if self.data == 'drivewayOn':
				print "Turning driveway light on"
				GPIO.output(11, True)
				self.request.sendall('.')
			elif self.data == 'drivewayOff':
				print "Turning driveway light off"
				GPIO.output(11, False)
				self.request.sendall('.')
			#Carport light
			if self.data == 'carportOn':
				print "Turning carport light on"
				GPIO.output(12, True)
				self.request.sendall('.')
			elif self.data == 'carportOff':
				print "Turning carport light off"
				GPIO.output(12, False)
				self.request.sendall('.')
				
			#Workshop light
			if self.data == 'workshopOn':
				print "Turning workshop light on"
				GPIO.output(13, True)
				self.request.sendall('.')
			elif self.data == 'workshopOff':
				print "Turning workshop light off"
				GPIO.output(13, False)
				self.request.sendall('.')
				
			#Storage light
			if self.data == 'storageOn':
				print "Turning storage light on"
				GPIO.output(16, True)
				self.request.sendall('.')
			elif self.data == 'storageOff':
				print "Turning storage light off"
				GPIO.output(16, False)
				self.request.sendall('.')
### STATUS SENDS
			#Garagedoor button text
			if self.data == 'door_button':
				if GPIO.input(15):
					self.request.sendall('Close')
					#GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
					print "Sending buttontext: Close"
				else:
					self.request.sendall('Open')
					#GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
					print "Sending buttontext: Open"
			#Garagedoor position
			if self.data == 'door_status':
				#print "Sending Door status: ", GPIO.input(15)
				if GPIO.input(15):
					print "Sending that garagedoor is open"
					self.request.sendall('open')
				else:
					print "Sending that garagedoor is closed"
					self.request.sendall('closed')
			#Coming-home-lights status		
			if self.data == 'comingHomeStatus':
				if comingHomeStatus == 1:
					self.request.sendall('On')
					print "Sending that coming home lights are on"
				else:
					self.request.sendall('Off')
					print "Sending that coming home lights are off"
			
if __name__ == "__main__":
	HOST, PORT = "", 54321
    # Create the server, binding to localhost on port 54321
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
	server.serve_forever()
