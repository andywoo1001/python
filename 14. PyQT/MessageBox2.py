#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
 
# Create an PyQT4 application object.
app = QApplication(sys.argv)    
 
# The QWidget widget is the base class of all user interface objects in PyQt4.
window = QWidget()
 
# Set window size. 
window.resize(640,480)
 
# Set window title  
window.setWindowTitle("Hello Window")
 
def messagebox():
	#Show a message box
	result = QMessageBox.question(window, 'Message', "Do you like Python?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	if result == QMessageBox.Yes:
		print ('Yes')
	else:
		print ('No')


# Add a button
btn = QPushButton('Click for msg function!', window)
btn.setToolTip('Click to quit!')
btn.clicked.connect(messagebox)
btn.resize(btn.sizeHint())
btn.move(200,160)

# Show window
window.show() 
 
sys.exit(app.exec_())

