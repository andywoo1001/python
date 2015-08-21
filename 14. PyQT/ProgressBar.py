import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
# The QWidget widget is the base class of all user interface objects in PyQt4.


# ==========================================================
class QProgBar(QProgressBar):
	value = 0

	@pyqtSlot()
	def increaseValue(progressBar):
		progressBar.setValue(progressBar.value)
		progressBar.value = progressBar.value+1
 

window = QWidget()
 
# Set window size. 
window.resize(320, 240)
 
# Set window title  
window.setWindowTitle("Hello World!") 
 

# Create progressBar. 
bar = QProgBar(window)
bar.resize(320,50)    
bar.setValue(0)
bar.move(0,20)
 
# create timer for progressBar
timer = QTimer()
bar.connect(timer,SIGNAL("timeout()"),bar,SLOT("increaseValue()"))
timer.start(400) 
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
