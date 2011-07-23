import gobject, pygst, gtk, pygtk
import glib
pygst.require("0.10")
import gst
import os,sys 
import time
import thread,threading

global actress
actress = [('jessica','pomano','1981'),('jol','fog','2001')]

global actress1 
actress1=[]
global Flag
Flag = False
global myport
myport=[]
from chat_client import ChatConnect
			
						
class Stream:
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Webcam")
		window.set_default_size(500,400)
		window.connect("destroy",gtk.main_quit,"WM destroy")
		hBox = gtk.HBox()
		hBox.set_border_width(10)
		hBox.set_spacing(10)
		window.add(hBox)
		
		vbox = gtk.VBox(False,4)
		vbox.set_size_request(300,400)
		hBox.pack_start(vbox,False)
		
		self.movie_window=gtk.DrawingArea()
		self.movie_window.set_size_request(200,150)
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox,False)
		hbox.set_border_width(20)
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("Stream")
		self.button.connect("clicked",self.start_stop)
		hbox.pack_start(self.button,False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked",self.exit)
		hbox.pack_start(self.button2,False)
		self.button3 =gtk.Button("Connect To Server")
		self.button3.connect("clicked",self.connect)
		hbox.pack_start(self.button3,False)
		hbox.add(gtk.Label())
		vbox1 = gtk.VBox(False,8)
			
	
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		#self.sw.show()
		vbox1.pack_start(sw,True,True,0)
		store = self.create_model()
		treeView = gtk.TreeView(store)
		treeView.connect("row-activated",self.on_activated)
		treeView.set_rules_hint(True)
		#self.treeView.show()
		sw.add(treeView)
		
		self.create_columns(treeView)
		self.statusbar = gtk.Statusbar()
		vbox1.pack_start(self.statusbar,False,False,0)
		hBox.pack_start(vbox1)
		
		
		
		
		gobject.timeout_add(7000,self.call_b,treeView,store)	
		
		window.show_all()
		
		
		self.pipeline = gst.Pipeline("client")
 
		self.src = gst.element_factory_make("v4l2src", "source")
		self.pipeline.add(self.src)

		self.mpeg = gst.element_factory_make("ffmpegcolorspace","mpeg")
		self.pipeline.add(self.mpeg)
		self.src.link(self.mpeg)

		self.tee=gst.element_factory_make("tee","tee0")
		self.pipeline.add(self.tee)
		self.mpeg.link(self.tee)

		self.queue0 = gst.element_factory_make("queue","queue0")
		self.pipeline.add(self.queue0)
		self.tee.link(self.queue0)

		self.sink = gst.element_factory_make("autovideosink","sink")
		self.pipeline.add(self.sink)
		self.queue0.link(self.sink)

		self.queue1 = gst.element_factory_make("queue","queue1")
		self.pipeline.add(self.queue1)
		self.tee.link(self.queue1)

		self.theora = gst.element_factory_make("theoraenc","theora")
		self.pipeline.add(self.theora)
		self.queue1.link(self.theora)

		self.mux = gst.element_factory_make("oggmux","mux")
		self.pipeline.add(self.mux)
		self.theora.link(self.mux)

		self.audiosrc = gst.element_factory_make("audiotestsrc","audiosrc")
		self.pipeline.add(self.audiosrc)
		

		self.audioconvert = gst.element_factory_make("audioconvert","audioconvert")
		self.pipeline.add(self.audioconvert)
		self.audiosrc.link(self.audioconvert)

		self.queue2 = gst.element_factory_make("queue","queue2")
		self.pipeline.add(self.queue2)
		self.audioconvert.link(self.queue2)

		self.vorbisenc = gst.element_factory_make("vorbisenc","vorbisenc")
		self.pipeline.add(self.vorbisenc)
		self.queue2.link(self.vorbisenc)

		self.vorbisenc.link(self.mux)

		self.queue3  = gst.element_factory_make("queue","queue3")
		self.pipeline.add(self.queue3)
		self.mux.link(self.queue3)
 
		self.client = gst.element_factory_make("tcpserversink", "client")
		self.pipeline.add(self.client)
		self.client.set_property("host", "127.0.0.1")
		self.client.set_property("port", 3000)
		self.queue3.link(self.client)
 
		#self.pipeline.set_state(gst.STATE_PLAYING)
		
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message",self.on_message)
		bus.connect("sync-message::element",self.on_sync_message)
		
	def call_b(self,treeView,store):
		self.net.getlist()
		self.create_model1(store,treeView)	
		return True
		
	def create_model(self):
		store = gtk.ListStore(str,str,str)
		for act in actress:
			store.append([act[0],act[1],act[2]])
		return store
	
	def create_model1(self,store,treeView):
		store.clear()
		for act in actress1:
			store.append([act[0],act[1],act[2]])	
		treeView.show()
					
		
	def create_columns(self,treeView):
		renderText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("ip",renderText,text=0)
		column.set_sort_column_id(0)
		treeView.append_column(column)			
		
		renderText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("port",renderText,text=1)
		column.set_sort_column_id(1)
		treeView.append_column(column)
		
		renderText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Year",renderText,text=2)
		column.set_sort_column_id(2)
		treeView.append_column(column)
		
		
	def on_activated(self,widget,row,col):
		
		model = widget.get_model()
		text = model[row][0]+"."+model[row][1]+","+model[row][2]
		self.statusbar.push(0,text)	
		#Dialog("127.0.0.1","4455")
		print myport[0]
		self.net.stream(model[row][0],model[row][1],"127.0.0.1",myport[0])
		#self.show("127.0.0.1","7000")
		
	def start_stop(self,w):
		if self.button.get_label()=="Stream":
			self.button.set_label("Streaming")
			self.pipeline.set_state(gst.STATE_PLAYING)
		else:
			self.pipeline.set_state(gst.STATE_NULL)
			self.button.set_label("Stream")		
			
	
	def exit(self,widget,data=None):
		self.connect("quit")
	def show1(self,ip,port):
		pass
		#t1=threading.Thread(target=show,args=[ip,port])
		#t1.start()
		#t1.join()
		
	
				
	
	
	def on_message(self,bus,message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.pipeline.set_state(gst.STATE_NULL)	
			self.button.set_label("Stream")
		elif t == gst.MESSAGE_ERROR:
			err,debug = message.parse_error()
			print "Error: %s" % err,debug
			self.pipeline.set_state(gst.STATE_NULL)	
			self.button.set_label("Stream")
	
	
	def on_sync_message(self,bus,message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()			
		if message_name == "prepare-xwindow-id":
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio",True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)
	
	def connect(self,w):
		if w=="quit":
			self.net.disconnect()
			self.net.join()
			gtk.main_quit()
		else:	
			
			self.net=ChatConnect("127.0.0.1",actress1,self.show1,myport)	
			self.net.start()	
		
			
	def main(self):
		gtk.gdk.threads_init()
		gtk.main()
		
def show(ip,port):	
	dialog=gtk.Dialog("Request",None,0,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
	dialog.set_default_size(200,150)
	label = gtk.Label(ip+" : "+port+" "+"wants the permission to view your webcam")
	dialog.vbox.pack_start(label,True,True,0)
	dialog.show_all()
		

	dialog.destroy()	
				
if __name__ == "__main__":
	stream = Stream()
	stream.main()
