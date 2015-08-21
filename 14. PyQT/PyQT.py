import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)
label = QLabel("Hell PyQt")
label.show()
app.exec_()