import sys
from PyQt4.QtGui import *
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
window = QMainWindow()
 
# Set window size. 
window.resize(320, 240)
 
# Set window title  
window.setWindowTitle("Hello World!") 
 

# ==========================================================


# ==========================================================

 
# Create a button in the window
button = QPushButton('change button size', window)
button.move(20,20)
button.resize(button.sizeHint())


# Create the actions 
def on_click():
	print("Button clicked.")
	button.resize(button.size().width(),100) 
    
def on_press():
	print('on_press()')

def on_release():
	print('on_release()')
 
# connect the signals to the slots
button.clicked.connect(on_click)
button.pressed.connect(on_press)
button.released.connect(on_release)
# ==========================================================

# Show window
window.show() 
 
sys.exit(app.exec_())
