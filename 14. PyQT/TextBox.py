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
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
