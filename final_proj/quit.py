import gtk

class Window:
    def __init__(self):
        window = gtk.Window()
        window.set_title("Window Example")
        window.connect("destroy", lambda w: window.destroy())
        window.show()

Window()
gtk.main()
