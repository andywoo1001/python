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
# Create textbox
textbox = QLineEdit(window)
textbox.move(20, 20)
textbox.resize(280,40)

# Create textbox
label = QLabel('Output here.',window)
label.move(20,80)
label.resize(280,40)
label.show()
 

# ==========================================================

 
# Create a button in the window
button = QPushButton('Click me', window)
button.move(20,160)
 
# Create the actions 
def on_click():
    textbox.setText("Button clicked.")
    #label.setText('on_click()')
 
def on_press():
	textbox.setText("")
	label.setText('on_press()')
	print('on_press()')

def on_release():
	label.setText('on_release()')
	print('on_release()')
 
# connect the signals to the slots
button.clicked.connect(on_click)
button.pressed.connect(on_press)
button.released.connect(on_release)
# ==========================================================

# Show window
window.show() 
 
sys.exit(app.exec_())
