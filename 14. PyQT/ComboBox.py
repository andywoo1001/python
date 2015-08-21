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

# Create combobox
combo = QComboBox(window)
combo.addItem("Python")
combo.addItem("Perl")
combo.addItem("Java")
combo.addItem("C++")
combo.move(20,20)

print combo.x()
print combo.y() 
print combo.size().width()
print combo.size().height()
 
# ==========================================================

 
# Show window
window.show() 
 
sys.exit(app.exec_())
