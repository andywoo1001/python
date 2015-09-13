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
label = QLabel('Output here.',window)
label.move(20,80)
label.resize(280,40)
label.show()
# ==========================================================

# Show window
window.show() 
 
sys.exit(app.exec_())
