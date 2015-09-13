#Refer to http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-2/l
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import sys
from PyQt4 import QtGui
import numpy as np
import numpy
from pylab import *
import logging	
import subprocess
import time
import logging
from os import system
import pandas as pd
import re


Ui_MainWindow, QMainWindow = loadUiType('window_v3.ui')

ADB 			= 'adb '

def Wait_for_Device():
	print("Waiting for device ready" )
	system(ADB + 'wait-for-devices')

def Device_Info(listWidget):
			
	Wait_for_Device()

	# Get /system/build.prop file for device infomation
	prop  = subprocess.check_output(ADB + 'shell cat /system/build.prop', shell=True) #  ro.product.board

	# Display build information
	listWidget.clear()
	listWidget.addItem('= DEVICE INFORMATION =')

	PDA = re.findall('ro.build.PDA=(.*)', prop)[0][:-1]	
	listWidget.addItem('Build version: %s' % PDA )

	date  = re.findall('ro.build.date=(.*)', prop)[0][:-1]
	listWidget.addItem('Build Date: %s' % date  )

	device = re.findall('ro.build.flavor=(.*)', prop)[0][:-1]
	listWidget.addItem('Project code: %s' % device )

	model = re.findall('ro.product.model=(.*)', prop)[0][:-1]
	listWidget.addItem('Model: %s' % model )

	platform = re.findall('ro.board.platform=(.*)', prop)[0][:-1]
	listWidget.addItem('Platform: %s' % platform)

	chipname = re.findall('ro.chipname=(.*)', prop)[0][:-1]
	listWidget.addItem('Chip name: %s' % chipname )

	board = re.findall('ro.product.board=(.*)', prop)[0][:-1]
	listWidget.addItem('Board: %s' %  board)

	path_cache = re.findall('ro.hwui.path_cache_size=(.*)', prop)[0][:-1]
	listWidget.addItem('Path Cache Size: %sMB' % path_cache )

	texture_cache = re.findall('ro.hwui.texture_cache_size=(.*)', prop)[0][:-1]
	listWidget.addItem('Texture Cache Size: %sMB' % texture_cache )

	layer_cache = re.findall('ro.hwui.layer_cache_size=(.*)', prop)[0][:-1]
	listWidget.addItem('Layer Cache Size: %sMB' % layer_cache)

	listWidget.setTextAlignment(Qt.AlignHCenter)

class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(Main, self).__init__()
		self.setupUi(self)
		self.pushButton_Start.clicked.connect(self.StartButton)
		self.pushButton_Stop.clicked.connect(self.StopButton)
		#self.pushButton_Start.setIcon(QtGui.QIcon('/home/insu13.yu/Works/PyQT/QtDesign/EmbedQtChart/start.png'))
		#self.pushButton_Stop.setIcon(QtGui.QIcon('/home/insu13.yu/Works/PyQT/QtDesign/EmbedQtChart/stop.png'))
		#self.pushButton_Start.setGeometry(200,20, 50,40)
	
	def StartButton(self):		
		Device_Info(self.listWidget)
	
	def StopButton(self):
		print ('StopButton')


	def setup_CPU0_plots(self):
		fig = Figure()
		canvas = FigureCanvas(fig)
		self.widget_CPU0.addWidget(canvas)

		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		ax  = [ fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]
		
		for i in xrange(0,4,1):
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			# show grid
			ax[i].grid(True)
			
			# set your xticks manually (10 ticks)
			ax[i].xaxis.set_ticks(numpy.arange(0,100,3)) # [i for i in range(0,100, 10)]

			# set your yticks manually (10 ticks)
			ax[i].yaxis.set_ticks(numpy.arange(0, 2.1, 0.2))
			
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
		self.ax1 = ax

	def setup_CPU1_plots(self):
		fig = Figure()
		canvas = FigureCanvas(fig)
		self.widget_CPU1.addWidget(canvas)

		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		ax  = [ fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]
		
		for i in xrange(0,4,1):
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			# show grid
			ax[i].grid(True)
			
			# set your xticks manually (10 ticks)
			ax[i].xaxis.set_ticks(numpy.arange(0,100,3)) # [i for i in range(0,100, 10)]

			# set your yticks manually (10 ticks)
			ax[i].yaxis.set_ticks(numpy.arange(0, 2.1, 0.2))
			
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
		self.ax2 = ax

	def setup_Clocks_plots(self):
		fig = Figure()
		canvas = FigureCanvas(fig)
		self.widget_Clocks.addWidget(canvas)

		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		ax  = [ fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]
		
		for i in xrange(0,4,1):
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
		self.ax3 = ax

	def setup_Temperature_plots(self):
		fig = Figure()
		canvas = FigureCanvas(fig)
		self.widget_Temperature.addWidget(canvas)

		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		ax  = [ fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]
		
		for i in xrange(0,4,1):
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
		
		ax[0].set_ylabel('AP')
		ax[1].set_ylabel('')

		fig.subplots_adjust(left=0.05, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)
		self.ax4 = ax

	def update_plots(self):
		ax1 = self.ax1
		x = np.arange(0,100.0)
		y1 = np.cos(2*np.pi*x/50.0)
		y2 = np.sin(2*np.pi*x/50.0)

		#draw graph, style, color, 
		#ax[0].fill_between(x, -1, y1, color='#00FF00')
		#ax[0].plot(x, y1, linestyle='-', color='#00FF00', linewidth=2)
		#ax[1].plot(x, y2, linestyle='-', color='#00FF00', linewidth=2)

		
		self.show()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	main.setup_CPU0_plots()
	main.setup_CPU1_plots()
	main.setup_Clocks_plots()
	main.setup_Temperature_plots()

	main.update_plots()
	sys.exit(app.exec_())