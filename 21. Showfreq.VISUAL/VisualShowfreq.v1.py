#Refer to http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-2/l
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import sys
from PyQt4 import QtGui
import numpy as np
import numpy
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Ui_MainWindow, QMainWindow = loadUiType('window_v1.ui')



class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(Main, self).__init__()
		self.setupUi(self)
		#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))

		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		self.widgetLayout.addWidget(self.canvas)	
		self.ax1  =  self.fig.add_subplot(311)
		self.ax2  =  self.fig.add_subplot(312)
		self.ax3  =  self.fig.add_subplot(313)
		
		line1, = self.ax1.plot([], [], 'r-')
		line2, = self.ax2.plot([], [], 'g-')
		line3, = self.ax3.plot([], [], 'b-')

		self.lines = [line1, line2, line3]

		for ax in [self.ax1, self.ax2, self.ax3]:			
			ax.set_xlim(0,10)
			ax.set_ylim(0,1)
			ax.grid()


		self.y1, self.y2, self.y3 = [], [], []
		x = range(10)
		self.lines[0].set_xdata(x)
		self.lines[1].set_xdata(x)
		self.lines[2].set_xdata(x)

		self.ani = animation.FuncAnimation(self.fig, self.update, blit=False, interval=10)
		
	def update(self, data):
		self.y1 = np.random.rand(10)
		self.y2 = np.random.rand(10)
		self.y3 = np.random.rand(10)

		self.lines[0].set_ydata(self.y1)
		self.lines[1].set_ydata(self.y2)
		self.lines[2].set_ydata(self.y3)
		#self.lines[2].set_data(self.x, self.y3)

		return self.lines


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	#main.update_plots()
	

	main.show()
	sys.exit(app.exec_())


		
		#self.toolbar = NavigationToolbar(canvas, self.widgetWin, coordinates=True)
		#self.widgetLayout.addWidget(self.toolbar)
 