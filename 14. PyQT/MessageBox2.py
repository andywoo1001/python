import sys
from PyQt4.QtGui import *
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
window = QMainWindow()
 
# Set window size. 
window.resize(320, 240)
 
# Set window title  
window.setWindowTitle("Message box example") 
 

# ==========================================================
# Create a button in the window
button0 = QPushButton('About Box', window)
button1 = QPushButton('Question Box', window)
button2 = QPushButton('Warning', window)
button3 = QPushButton('Information', window)
button4 = QPushButton('Critical Box', window)
button0.move(20,20)
button1.move(20,60)
button2.move(20,100)
button3.move(20,140)
button4.move(20,180)


# Create the actions 
def on_click0():
	QMessageBox.about(w, "About", "An example messagebox ")


def on_click1():
	QMessageBox.question(window, 'Message', "Do you like Python?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)



def on_click2():
	QMessageBox.warning(window, "Message", "Are you sure you want to continue?")

 
def on_click3():
	QMessageBox.information(window, "Message", "An information messagebox")


def on_click4():
	QMessageBox.critical(window, "Message", "No disk space left on device.")


button1.clicked.connect(on_click0)
button1.clicked.connect(on_click1)
button2.clicked.connect(on_click2)
button3.clicked.connect(on_click3)
button4.clicked.connect(on_click4)

# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
