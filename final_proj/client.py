import asyncore,socket

class Client(asyncore.dispatcher_with_send):
	def __init__(self,host,port,message):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connect((host,port))
		self.out_buffer = message
		
	def handle_close(self):
		self.close()
		
	def handle_read(self):
		print "Recieved",self.recv(1024)
			
	
	def handle_write(self):
	
		text = raw_input()
		text = str(text)
		if text.startswith("disc"):
			self.close()
		else:
			self.send(text)
			
		
c = Client('',5007,"hello world")
asyncore.loop()			
