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
 
# Show window
window.show() 
 
sys.exit(app.exec_())

