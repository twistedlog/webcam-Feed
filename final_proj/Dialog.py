import gtk

class Dialog(object):
	def __init__(self):

		dialog = gtk.MessageDialog(parent = None,
		buttons = gtk.BUTTONS_YES_NO,
		flags =gtk.DIALOG_DESTROY_WITH_PARENT,
		type = gtk.MESSAGE_QUESTION,
		message_format = "Is this a good example?")
		dialog.set_title("MessageDialog Example")
		result = dialog.run()
		dialog.destroy()
		if result == gtk.RESPONSE_YES:
			print "Yes was clicked"
		elif result == gtk.RESPONSE_NO:
			print "No was clicked"
		


				
		
