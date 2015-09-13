import sys
from PyQt4 import QtCore, QtGui
from Form2 import Ui_Dialog
 
 
class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
    def slot_1st():
    	print ('slot_1st')
    def slot_2nd():
    	print ('slot_2nd')
    def slot_3rd():
    	print ('slot_3rd')
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyDialog()
    myapp.show()
    sys.exit(app.exec_())