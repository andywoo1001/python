import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

 

app = QApplication(sys.argv)       
label = QLabel('Output here.')
label.show()
app.exit(app.exec_())
