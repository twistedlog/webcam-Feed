import socket
import thread,threading
import sys
import time
import gtk

global clients_online
clients_online={}
	
		
class users_online():
	def __init__(self,address,client_socket):
		clients_online[client_socket.getpeername()[0]+":"+str(client_socket.getpeername()[1])]=client_socket
		print clients_online
		
class bridge(object):
	def __init__(self):
		pass
		
	def stream(self,sendto_ip,sendto_port,from_ip,from_port):
		self.key=sendto_ip+":"+sendto_port
		socket=clients_online[self.key]
		data = "stream"+":"+str(from_ip)+":"+str(from_port)
		socket.send(data)	
		
	def reply(self,from_ip,from_port,to_ip,to_port,streaming_port):
		self.key=to_ip+":"+to_port
		socket=clients_online[self.key]
		data = "ack"+":"+str(from_ip)+":"+str(from_port)+":"+str(streaming_port)
		socket.send(data)	
		
					
		
def handlechild(clientsock):
	peer = clientsock.getpeername()
	print "Got connection from ",peer
	clientsock.send("peer"+":"+str(clientsock.getpeername()[1]))
	
	while 1:
		# send users online list
		#sendAll(clientsock)
		try:
			data=clientsock.recv(4096)
		
		except socket.error:
			print "server shutdown"
			return		
		except:
			clientsock.close()
			
			break
		if data.startswith("stream"):
			data=data.split(':')
			bridge.stream(data[1],data[2],data[3],data[4])
			
		elif data.startswith("disconnect"):
			print "client quitting"
			clientsock.close()
			return	
			
		elif data.startswith("ack"):
			data=data.split(':')
			print "ack data" 
			print data
			bridge.reply(data[1],data[2],data[3],data[4],data[5])
			
		elif data.startswith("clients"):
			clientsock.send("/"+str(clients_online.keys()))
			
		elif data.startswith("disc"):
			print "quitting client"
			clientsock.send("disc")
			clientsock.close()	
			break
			
		if not len(data):
			clientsock.close()
			break	
					

def main():
	# the parent thread
	global clients
	clients=[]
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server.bind((socket.gethostname(),7000))
	server.listen(5)
	
	while 1:
		print "Waiting for connections"
		try:
			clientsock,clientaddr = server.accept()
			users_online(clientaddr,clientsock)
		
		except KeyboardInterrupt:
			server.close()
			for sock in clients:
				sock.close()
			break	
		clients.append(clientsock)
		t = threading.Thread(target=handlechild,args=[clientsock])
		t.setDaemon(1)
		t.start()
		
		
if __name__ =='__main__':
	bridge=bridge()	

	main()	
	
			
