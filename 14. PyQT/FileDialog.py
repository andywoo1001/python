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
# Get filename using QFileDialog
filename = QFileDialog.getOpenFileName(window, 'Open File', './')
print filename
 
# print file contents
with open(filename, 'r') as f:
    print(f.read())
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
