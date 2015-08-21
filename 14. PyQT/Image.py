import os
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
# Create widget
label = QLabel(window)
pixmap = QPixmap(os.getcwd() + '/logo.jpg')
label.setPixmap(pixmap)
window.resize(pixmap.width(),pixmap.height())
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
