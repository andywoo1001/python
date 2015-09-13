#Refer to http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-2/l
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import sys
from PyQt4 import QtGui
import numpy as np
import numpy
from pylab import *
	
Ui_MainWindow, QMainWindow = loadUiType('window_v2.ui')


class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(Main, self).__init__()
		self.setupUi(self)

	def setup_plots(self):
		fig = Figure()
		canvas = FigureCanvas(fig)
		self.mplvl.addWidget(canvas)		
		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		ax  = [ fig.add_subplot(811), fig.add_subplot(812), fig.add_subplot(813), fig.add_subplot(814), 
				fig.add_subplot(815), fig.add_subplot(816), fig.add_subplot(817), fig.add_subplot(818), ]
		
		for i in xrange(0,8,1):
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			# show grid
			ax[i].grid(True)
			
			# set your xticks manually (10 ticks)
			ax[i].xaxis.set_ticks(numpy.arange(0,100,3)) # [i for i in range(0,100, 10)]

			# set your yticks manually (10 ticks)
			ax[i].yaxis.set_ticks(numpy.arange(-1,1,0.2))
			
			# remove label
			ax[i].set_xticklabels([])

			ax[i].set_axis_bgcolor((0, 0, 0))

			ticklines = ax[i].get_xticklines()
			ticklines.extend( ax[i].get_yticklines() )
			gridlines = ax[i].get_xgridlines()
			gridlines.extend( ax[i].get_ygridlines() )
			ticklabels = ax[i].get_xticklabels()
			ticklabels.extend( ax[i].get_yticklabels() )

			for line in ticklines:
				line.set_color('#00C040')
				line.set_linewidth(1)

			for line in gridlines:
				line.set_color('#00C040')
				line.set_linestyle('-')			

			for label in ticklabels:
				label.set_color('#404040') # drak grey
				label.set_fontsize('small')
			# draw horizontal line
			#ax[0].axhline(y=0.5, xmin=0, xmax=1, color='#FF0000', linewidth=4)
			# draw vertical line
			ax[0].axvline(x=50, ymin=0, ymax=1, color='#006000', linewidth=4)


		fig.subplots_adjust(left=0.05, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)
		self.ax = ax

	def update_plots(self):
		ax = self.ax
		x = np.arange(0,100.0)
		y1 = np.cos(2*np.pi*x/50.0)
		y2 = np.sin(2*np.pi*x/50.0)

		#draw graph, style, color, 
		ax[0].fill_between(x, -1, y1, color='#00FF00')
		ax[0].plot(x, y1, linestyle='-', color='#00FF00', linewidth=2)
		ax[1].plot(x, y2, linestyle='-', color='#00FF00', linewidth=2)

		
		self.show()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	main.setup_plots()
	main.update_plots()
	sys.exit(app.exec_())