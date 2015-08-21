import sys
from PyQt4.QtGui import *
from PyQt4 import QtGui
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)       
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
#window = QMainWindow()
 
# Set window size. 
#window.resize(320, 240)
 
# Set window title  
#window.setWindowTitle("Hello World!") 
 

# ==========================================================
tabs = QtGui.QTabWidget()
    
 # Create tabs
tab1 = QtGui.QWidget() 
tab2 = QtGui.QWidget()
tab3 = QtGui.QWidget()
tab4 = QtGui.QWidget()
 
 # Resize width and height
tabs.resize(250, 150)
    
# Set layout of first tab
vBoxlayout = QtGui.QVBoxLayout()
pushButton1 = QtGui.QPushButton("Start")
pushButton2 = QtGui.QPushButton("Settings")
pushButton3 = QtGui.QPushButton("Stop")
vBoxlayout.addWidget(pushButton1)
vBoxlayout.addWidget(pushButton2)
vBoxlayout.addWidget(pushButton3)
tab1.setLayout(vBoxlayout)   
     
# Add tabs
tabs.addTab(tab1,"Tab 1")
tabs.addTab(tab2,"Tab 2")
tabs.addTab(tab3,"Tab 3")
tabs.addTab(tab4,"Tab 4") 
    
# Set title and show
tabs.setWindowTitle('PyQt QTabWidget @ pythonspot.com')
tabs.show()
 
# ==========================================================

 
# Show window
#window.show() 
 
sys.exit(app.exec_())
