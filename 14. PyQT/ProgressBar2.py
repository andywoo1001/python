import sys
from PyQt4 import QtGui, QtCore, Qt
import math
 
class QtGauge(QtGui.QWidget):
 
    value = 1
 
    def __init__(self):
        super(QtGauge, self).__init__()
        self.initUI()
 
    def setValue(self,value):
        self.value = value
 
    def getValue(self):
        return self.value
 
    def initUI(self):      
 
        hbox = QtGui.QHBoxLayout(self)
        lbl = QtGui.QLabel(self)
 
        hbox.addWidget(lbl)
        self.setLayout(hbox)
        self.setGeometry(0, 0,600,600)
       
        self.move(300, 200)
        self.setWindowTitle('Dial Guage')
        self.show()  
       
    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        dial = QtGui.QPixmap("bg.png")
        #painter.drawPixmap(50, 50, 600, 600, dial)
       
        painter.setRenderHint(painter.Antialiasing)
        rect = e.rect()
 
        gauge_rect = QtCore.QRect(rect)
        size = gauge_rect.size()
        pos = gauge_rect.center()
        gauge_rect.moveCenter( QtCore.QPoint(pos.x()-size.width(), pos.y()-size.height()) )
        gauge_rect.setSize(size*.9)
        gauge_rect.moveCenter(pos)
 
        refill_rect = QtCore.QRect(gauge_rect)
        size = refill_rect.size()
        pos = refill_rect.center()
        refill_rect.moveCenter( QtCore.QPoint(pos.x()-size.width(), pos.y()-size.height()) )
        # smaller than .9 == thicker gauge
        refill_rect.setSize(size*.9)
        refill_rect.moveCenter(pos)
 
        painter.setPen(QtCore.Qt.NoPen)
 
        painter.drawPixmap(rect, dial)
 
        painter.save()
        grad = QtGui.QConicalGradient(QtCore.QPointF(gauge_rect.center()), 270.0)
        grad.setColorAt(.75, QtCore.Qt.green)
        grad.setColorAt(.5, QtCore.Qt.yellow)
        grad.setColorAt(.1, QtCore.Qt.red)
        painter.setBrush(grad)
        #painter.drawPie(gauge_rect, 225.0*16, self._value*16)
        painter.drawPie(gauge_rect, 225.0*16, -270*self.value*16)
        painter.restore()
 
        painter.setBrush(QtGui.QBrush(dial.scaled(rect.size())))
        painter.drawEllipse(refill_rect)
 
        super(QtGauge,self).paintEvent(e)   
        painter.end()
 
       
def main():
    app = QtGui.QApplication(sys.argv)
    ex = QtGauge()
    ex.setValue(0.6)
    print ex.getValue()
    sys.exit(app.exec_())
 
 
if __name__ == '__main__':
    main()