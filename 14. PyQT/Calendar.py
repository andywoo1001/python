import sys
from PyQt4.QtGui import *
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
window = QMainWindow()
 
# Set window size. 
window.resize(320, 240)
 
# Set window title  
window.setWindowTitle("PyQT ComboBox") 
 

# ==========================================================

# Create calendar
cal = QCalendarWidget(window)
cal.setGridVisible(False)
cal.move(0, 0)
cal.resize(320,240) 
 
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
