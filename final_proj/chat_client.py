import socket
import threading,thread

import time
from test import Recieve
defaulthost ='localhost'
port=7000
sock = []

import sys,os
import pygtk,gtk,gobject
import pygst
pygst.require("0.10")
import gst
# Callback for the decodebin source pad

		

	
		
class ChatConnect(threading.Thread):
	"""
	Run as a separate thread to make and manage the socket connection to the
	chat server
	"""
	def __init__(self,host,actress1,show,myport):
		threading.Thread.__init__(self)
		self.host=host
		self.actress1 = actress1
		self.show=show
		self.myport=myport
		
		
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
		
		try:
			self.socket.connect((self.host,port))
			print "we are connected"
			sock.append(self.socket)
			
			
			
		except:
			return
		while True:
			try:
				data = self.socket.recv(4096)
			except socket.timeout:
				continue
			except socket.error:
				print "server shutdown"
				return	
			except:
				break
			if data.startswith("stream"):
				data=data.split(':')
				print data
				self.show("127.0.0.1","4000")
				#self.ack("127.0.0.1","3001",data[1],data[2],"4000")
				#self.show1(data[1],data[2])
				#self.th()
				#t = threading.Thread(target=handlechild,args=["127.0.0.1","3200"])
	
				#t.start()	
				#t.join()
			elif data.startswith("ack"):
				print "ack" 
				print data
				#self.th()
				
				
			elif data.startswith("peer"):
				data = data.split(':')
				del self.myport[:]
				self.myport.append(data[1])
				print self.myport[0]	
			elif data.startswith("disc"):
				self.socket.close()
				print "closed socket"
				return
			elif data.startswith("/"):
				self.update(data)	
				
	def stream(self,sendto_ip,sendto_port,from_ip,from_port):
		data="stream"+":"+str(sendto_ip)+":"+str(sendto_port)+":"+str(from_ip)+":"+str(from_port)
		self.sock = sock[0]
		self.sock.send(data)
		
	def ack(self,from_ip,from_port,to_ip,to_port,streaming_port):
		data = 	"ack"+":"+str(from_ip)+":"+str(from_port)+":"+str(to_ip)+":"+str(to_port)+":"+str(streaming_port)
		self.sock=sock[0]
		self.sock.send(data)
		

							
	def disconnect(self):
		print sock[0]
		self.sock=sock[0]
		self.sock.send("disc")
		print"quit called"	
		
	def update(self,data):
		
		data = data.split("/")
		del data[0]
		data = eval(data[0])
		#data1=[]
		#data1.extend(data)
		print type(data)
		
		del self.actress1[:]
		for x in data:
			
			
			x=x.split(':')
			#print x
			t=(x[0],x[1],'')
			
			
			self.actress1.append(t)
			print self.actress1
	
	def getlist(self):
		self.sock=sock[0]
		self.sock.send("clients")	
		
	def th(self):
		t = threading.Thread(target=handlechild)
		t.start()
		t.join()
		
				
								

		
	
