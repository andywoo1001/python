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
# Show a message box
result = QMessageBox.question(window, 'Message', "Do you like Python?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
 
if result == QMessageBox.Yes:
    print 'Yes.'
else:
    print 'No.'        
 
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
