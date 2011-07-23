import sys,os
import pygtk,gtk,gobject
import pygst
pygst.require("0.10")
import gst
 
# Callback for the decodebin source pad

class Recieve:
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Recieving")
		window.set_default_size(400,400)
		window.connect("destroy",gtk.main_quit,"WM destroy")
		
		vbox = gtk.VBox()
		vbox.set_border_width(10)
		#vbox.set_size_request(350,350)
		window.add(vbox)
		self.movie_window=gtk.DrawingArea()
		self.movie_window.set_size_request(200,200)
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox,False)
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("quit")
		self.button.connect("clicked", self.exit)
		hbox.pack_start(self.button, False)
		hbox.add(gtk.Label())
		
		
		window.show_all()
		
		self.pipeline = gst.Pipeline("server")
 
		self.tcpsrc = gst.element_factory_make("tcpclientsrc", "source")
		self.pipeline.add(self.tcpsrc)
		self.tcpsrc.set_property("host", "127.0.0.1")
		self.tcpsrc.set_property("port", 3000)
 
		self.oggdemux = gst.element_factory_make("oggdemux","oggdemux")
		self.oggdemux.connect("pad-added",self.demuxer_callback)
		self.pipeline.add(self.oggdemux)

		self.queue0 =  gst.element_factory_make("queue","queue0")
		self.pipeline.add(self.queue0)

		self.theoradec = gst.element_factory_make("theoradec","theoradec")
		self.pipeline.add(self.theoradec)
		self.queue0.link(self.theoradec)

		self.autovideosink = gst.element_factory_make("xvimagesink","autovideosink")
		self.pipeline.add(self.autovideosink)
		self.theoradec.link(self.autovideosink)

		self.queue1 =  gst.element_factory_make("queue","queue1")
		self.pipeline.add(self.queue1)

		self.vorbisdec = gst.element_factory_make("vorbisdec","vorbisdec")
		self.pipeline.add(self.vorbisdec)
		self.queue1.link(self.vorbisdec)

		self.audioconvert = gst.element_factory_make("audioconvert","audioconvert")
		self.pipeline.add(self.audioconvert)
		self.vorbisdec.link(self.audioconvert)

		self.alsasink = gst.element_factory_make("alsasink","alsasink")
		self.pipeline.add(self.alsasink)
		self.alsasink.set_property("sync","false")
		self.audioconvert.link(self.alsasink)
		gst.element_link_many(self.tcpsrc,self.oggdemux)
		
		bus=self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message",self.on_message)
		bus.connect("sync-message::element",self.on_sync_message)

 		self.pipeline.set_state(gst.STATE_PLAYING)
 		
 	def exit(self,w):
 		self.pipeline.set_state(gst.STATE_NULL)
 		gtk.main_quit()
 	
 	def demuxer_callback(self,demuxer,pad):
		if  pad.get_caps().to_string().startswith("video"):
			qv_pad = self.queue0.get_pad("sink")
			pad.link(qv_pad)
		elif pad.get_caps().to_string().startswith("audio"):
			qa_pad = self.queue1.get_pad("sink")
			pad.link(qa_pad)	
	
	def	on_message(self,bus,message):
		t=message.type
		if t == gst.MESSAGE_EOS:
			self.pipeline.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			err,debug = message.parse_error()
			print "Error: %s"% err,debug	
			self.pipeline.set_state(gst.STATE_NULL)	
	
	def on_sync_message(self,bus,message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			#ASSIGN THE VIEWPORT
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio",True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)	
			
	def main(self):
		gtk.gdk.threads_init()
		gtk.main()				
 
# enter into a mainloop
if __name__ == "__main__":
	recv = Recieve()
	recv.main()

