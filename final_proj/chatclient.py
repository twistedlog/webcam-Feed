import socket
import threading

defaulthost = 'localhost'
port = 6000

class ChatConnect(threading.Thread):

	def __init__(self,host,connected,display,lost):
		threading.Thread.__init__(self)
		self.host = host
		self.connected = connected
		self.display = display
		self.lost = lost
		self.msgLock = threading.Lock()
		self.numMsg =0
		self.msg=[]
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET)
		self.socket.settimeout(1)
		try:
			self.socket.connect((self.host,port))
		except:
			self.lost("Unable to connect to %s. Check the server ." % self.host)
			return
		self.connected()	
		while True:
			self.__send()
			try:
				data = self.socket.recv(4096)
			except socket.timeout:
				continue
			except:
				self.lost("Network Connection closed by server....")
				break
			if len(data):
				self.display(data)
			else:
				self.lost("Network Connection closed")
				break
		self.socket.close()								
