#Refer to http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-2/
# http://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib
# qt examples http://www.elektrosoft.it/tutorials/hbqt/hbqt.asp
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
from threading import Timer,Thread,Event
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation


Ui_MainWindow, QMainWindow = loadUiType('window_v4.ui')

ADB 			= 'adb '

class ShowFreq():
	def __init__(self, milliseconds):
		self.proc = subprocess.Popen(['adb', 'shell', '/sdcard/spr/showfreq', '%s' % milliseconds ], stdout=subprocess.PIPE)

	def GetValues(self):
		line = self.proc.stdout.readline()
		string = line.rstrip()
		str1 = re.sub('[^0-9\.\s-]','',string)
		str2 = re.sub('-\s','',str1)
		values = re.split('\s+',str2)
		if len(values) != 27:
			return None;
		# remove incorrectly parsed two values (CPU0, CPU1)
		del values[19]
		del values[20]
		values = [float(x) for x in values]
		return values

	def Terminate(self):
		self.proc.kill()

def Wait_for_Device():
	print("Waiting for device ready" )
	system(ADB + 'wait-for-devices')
	print("Done")

def Detect_Device():
	global	ADB, DEVICE_MODEL, DEVICE_SERIAL, DEVICE_CHIP, DEVICE_PRODUCT
	ADB = 'adb '
	Wait_for_Device()
	
	logging.info("Detecting Devices")
	devices_str	= subprocess.check_output('adb devices', shell=True) 
	Device_List	= re.findall('([0-9].*)\sdevice', devices_str)
	nDevices 	= len(Device_List)

	# No device is detected
	if( nDevices == 0):
		logging.error('NO devices are connected !')
		sys.exit(1)
	
	logging.debug(' %d device(s) detected', nDevices)
	logging.debug(Device_List)

	
	index = 0
	Devices = []
	for device_serial in Device_List:
		device_chip = subprocess.check_output(('adb -s %s shell getprop ro.product.board' % device_serial), shell=True)
		device_chip = re.sub('\s','',device_chip)

		device_product = subprocess.check_output(('adb -s %s shell getprop ro.product.device' % device_serial), shell=True)
		device_product = re.sub('\s','',device_product)

		if device_chip.find('universal7420') != -1: 	# NOBLE
			device_model = 'NOBLE'
			DEVICE = NOBLE
		elif device_chip.find('universal3475') != -1: # J2
			device_model = 'J2'
			DEVICE = J2		
		else:
			DEVICE = UNKNOWN
			sys.exit(1)
		
		logging.info('[%2d] Serial No.: %s, Device Model: %s (%s), Board chipset: %s' % (index, device_serial, device_model, device_product, device_chip))
		Devices.append([device_model, device_serial, device_chip, device_product])
		index+=1
	
	if(nDevices == 1):
		logging.info('Only one device is found. The default device is chosen')
		DEVICE_MODEL 	= Devices[0][0]
		DEVICE_SERIAL 	= Devices[0][1]
		DEVICE_CHIP 	= Devices[0][2]
		DEVICE_PRODUCT 	= Devices[0][3].upper()		
	else:
		select = int(input('Choose one device: '))
		if( select >= nDevices) :
			logging.error('Wrong device selection %d', select)
			sys.exit(1)			
		DEVICE_MODEL 	= Devices[select][0]
		DEVICE_SERIAL 	= Devices[select][1]
		DEVICE_CHIP 	= Devices[select][2]
		DEVICE_PRODUCT  = Devices[select][3].upper()		

	logging.info('Serial No.: %s, Device Model: %s (%s), Board chipset: %s is selected' % (DEVICE_SERIAL, DEVICE_MODEL, DEVICE_PRODUCT, DEVICE_CHIP))

	# adb -s XXX setting
	ADB = 'adb -s %s ' % DEVICE_SERIAL
	logging.debug('adb device option is: \'%s\'' % ADB)
	
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

	#listWidget.setTextAlignment(Qt.AlignHCenter)

class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(Main, self).__init__()
		self.setupUi(self)
		self.pushButton_Start.clicked.connect(self.StartButton)
		self.pushButton_Stop.clicked.connect(self.StopButton)
		#self.pushButton_Start.setIcon(QtGui.QIcon('/home/insu13.yu/Works/PyQT/QtDesign/EmbedQtChart/start.png'))
		#self.pushButton_Stop.setIcon(QtGui.QIcon('/home/insu13.yu/Works/PyQT/QtDesign/EmbedQtChart/stop.png'))
		#self.pushButton_Start.setGeometry(200,20, 50,40)
		# draw horizontal line
		#ax[0].axhline(y=0.5, xmin=0, xmax=1, color='#FF0000', linewidth=4)
			
		# draw vertical line
		#ax[0].axvline(x=50, ymin=0, ymax=1, color='#006000', linewidth=4)

		#time index
		self.timeindex 	= 0
		self.mCPU0 		= []
		self.mCPU1 		= []
		self.mCPU2 		= []
		self.mCPU3 		= []
		self.mCPU4 		= []
		self.mCPU5 		= []
		self.mCPU6 		= []
		self.mCPU7 		= []
		self.mDVFS_Max 	= []	
		self.mDVFS_Min 	= []
		self.mDDR 		= []
		self.mBUS 		= []
		self.mGPUFreq 	= []
		self.mGPUUtil 	= []
		self.mAPT 		= []
		self.mPST 		= []
		self.mCPUG0 	= []
		self.mCPUG1 	= []
		self.mGPU 		= []
		

		#draw graph, style, color, 
		width = 1.0
		anti = False


		#init CPU information panel
		self.figA = Figure()
		self.canvasA = FigureCanvas(self.figA)
		self.Layout_CPU.addWidget(self.canvasA)
		self.axA = [ self.figA.add_subplot(811), self.figA.add_subplot(812), self.figA.add_subplot(813), self.figA.add_subplot(814),
					 self.figA.add_subplot(815), self.figA.add_subplot(816), self.figA.add_subplot(817), self.figA.add_subplot(818)	]
		
		lineA0, = self.axA[0].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA1, = self.axA[1].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA2, = self.axA[2].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA3, = self.axA[3].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA4, = self.axA[4].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA5, = self.axA[5].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA6, = self.axA[6].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		lineA7, = self.axA[7].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti )
		self.linesA = [lineA0,lineA1,lineA2,lineA3,lineA4,lineA5,lineA6,lineA7]
		

		#init System information panel
		self.figB = Figure()
		self.canvasB = FigureCanvas(self.figB)
		self.Layout_System.addWidget(self.canvasB)
		self.axB  = [ self.figB.add_subplot(811), self.figB.add_subplot(812), self.figB.add_subplot(813), self.figB.add_subplot(814),
					  self.figB.add_subplot(815), self.figB.add_subplot(816), self.figB.add_subplot(817), self.figB.add_subplot(818) ]

		lineB0a, = self.axB[0].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # DVFS
		lineB0b, = self.axB[0].plot([], [], linestyle='-', color='#0000FF', linewidth=width, antialiased=anti) # DVFS
		lineB1, = self.axB[1].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # DDR
		lineB2, = self.axB[2].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # BUS
		lineB3, = self.axB[3].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Freq
		lineB4, = self.axB[4].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Util	
		lineB5, = self.axB[5].plot([], [], linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # APT
		lineB6, = self.axB[6].plot([], [], linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # PST		
		lineB7a, = self.axB[7].plot([], [], linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # C0 Temperature
		lineB7b, = self.axB[7].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti) # C1 Temperature
		lineB7c, = self.axB[7].plot([], [], linestyle='-', color='#0000FF', linewidth=width, antialiased=anti) # C2 Temperature
		self.linesB = [lineB0a,lineB0b,lineB1,lineB2,lineB3,lineB4,lineB5,lineB6,lineB7a,lineB7b,lineB7c]
		
		x = arange(100)
		for line in self.linesA:
			line.set_xdata(x)

		for line in self.linesB:
			line.set_xdata(x)

		self.setup_CPU_chart()
		self.setup_System_chart()
			

	def setup_CPU_chart(self):
		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		for i in xrange(0,8):
			#self.axA[i].clear()
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			ticklines = self.axA[i].get_xticklines()
			ticklines.extend( self.axA[i].get_yticklines() )
			gridlines = self.axA[i].get_xgridlines()
			gridlines.extend( self.axA[i].get_ygridlines() )
			ticklabels = self.axA[i].get_xticklabels()
			ticklabels.extend( self.axA[i].get_yticklabels() )

			for line in ticklines:
				line.set_color('#00C040')
				line.set_linewidth(1)

			for line in gridlines:
				line.set_color('#00C040')
				line.set_linestyle('-')			

			for label in ticklabels:
				label.set_color('#404040') # drak grey
				label.set_fontsize('8') # or 'small'

			#self.axA[0].axis([0,100,0,2100])
			self.axA[i].set_autoscale_on(False)

			# show grid
			self.axA[i].grid(True)

			# set your xticks manually (10 ticks)
			self.axA[i].xaxis.set_ticks(numpy.arange(0,100,2.5)) # [i for i in range(0,100, 10)]

			# set your yticks manually (10 ticks)
			self.axA[i].yaxis.set_ticks(numpy.arange(0, 1401 if i < 4 else 2201, 200))
			
			# remove label
			self.axA[i].set_xticklabels([])

			self.axA[i].set_axis_bgcolor((0, 0, 0))

		# Y labels
		self.axA[0].set_ylabel('CPU0')
		self.axA[1].set_ylabel('CPU1')
		self.axA[2].set_ylabel('CPU2')
		self.axA[3].set_ylabel('CPU3')
		self.axA[4].set_ylabel('CPU4')
		self.axA[5].set_ylabel('CPU5')
		self.axA[6].set_ylabel('CPU6')
		self.axA[7].set_ylabel('CPU7')

		self.figA.subplots_adjust(left=0.10, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)
		

	def setup_System_chart(self):
		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)

		for i in xrange(0,8):
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			ticklines = self.axB[i].get_xticklines()
			ticklines.extend( self.axB[i].get_yticklines() )
			gridlines = self.axB[i].get_xgridlines()
			gridlines.extend( self.axB[i].get_ygridlines() )
			ticklabels = self.axB[i].get_xticklabels()
			ticklabels.extend( self.axB[i].get_yticklabels() )

			for line in ticklines:
				line.set_color('#00C040')
				line.set_linewidth(1)

			for line in gridlines:
				line.set_color('#00C040')
				line.set_linestyle('-')			

			for label in ticklabels:
				label.set_color('#404040') # drak grey
				if(i == 0 or i == 1):
					label.set_fontsize('8') # or 'small'
				else:
					label.set_fontsize('9') # or 'small'

			# show grid
			self.axB[i].grid(True)
			
			# set your xticks manually (10 ticks)
			self.axB[i].xaxis.set_ticks(numpy.arange(0,100,3)) # [i for i in range(0,100, 10)]
		
			# remove label
			self.axB[i].set_xticklabels([])

			self.axB[i].set_axis_bgcolor((0, 0, 0))
			
			self.axB[i].set_autoscale_on(False)
			

		# Y ticks
		self.axB[0].yaxis.set_ticks(numpy.arange(0, 1201, 200)) # DVFS
		self.axB[1].yaxis.set_ticks(numpy.arange(0, 1301, 200)) # DDR
		self.axB[2].yaxis.set_ticks(numpy.arange(0, 1001, 100)) # BUS
		self.axB[3].yaxis.set_ticks(numpy.arange(0, 1001, 100)) # GPU Freq
		self.axB[4].yaxis.set_ticks(numpy.arange(0, 101, 10)) # GPU Util
		#self.axB[5].yaxis.set_ticks(numpy.arange(30, 71, 5)) # APT
		#self.axB[6].yaxis.set_ticks(numpy.arange(30, 71, 5)) # PST
		self.axB[7].yaxis.set_ticks(numpy.arange(0, 71, 10)) # Temperature

		self.axB[5].axis([0, 100, 30,70])
		self.axB[6].axis([0, 100, 30,70])

		# Y labels
		self.axB[0].set_ylabel('DVFS (MHz)')
		self.axB[1].set_ylabel('DDR (MHz)')
		self.axB[2].set_ylabel('BUS (MHz)')
		self.axB[3].set_ylabel('GPU Freq (MHz)')
		self.axB[4].set_ylabel('GPU Util (%)')
		self.axB[5].set_ylabel('APT (C)')
		self.axB[6].set_ylabel('PST (C)')
		self.axB[7].set_ylabel('Temperature (C)')

		self.figB.subplots_adjust(left=0.10, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)

	
	def update(self):

		values = self.showfreq.GetValues()
		print ('value=', values)
		if values == None:
			values = self.showfreq.GetValues()
			print ('value=', values)

		self.mCPU0.append(values[1])
		self.mCPU1.append(values[2])
		self.mCPU2.append(values[3])
		self.mCPU3.append(values[4])
		self.mCPU4.append(values[5])
		self.mCPU5.append(values[6])
		self.mCPU6.append(values[7])
		self.mCPU7.append(values[8])

		self.mDVFS_Max.append(values[15])
		self.mDVFS_Min.append(values[16])
		self.mDDR.append(values[17])
		self.mBUS.append(values[18])
		self.mGPUFreq.append(values[13])
		self.mGPUUtil.append(values[14])
		self.mAPT.append(values[22])
		self.mPST.append(values[23])
		self.mCPUG0.append(values[19])
		self.mCPUG1.append(values[20])
		self.mGPU.append(values[21])
		self.timeindex += 1

		Max_Temperature = 40.0
		# DVFX Max
		if (values[15] == -1):
			self.LCD_DVFS_MAX.setStyleSheet( "color: #C0C0C0;" )
		else:
			self.LCD_DVFS_MAX.setStyleSheet( "color: #FF0000;" )

		# DVFX Min
		if (values[16] == -1):
			self.LCD_DVFS_MIN.setStyleSheet( "color: #C0C0C0;" )
		else:
			self.LCD_DVFS_MIN.setStyleSheet( "color: #FF0000;" )

		# GPU Freq 
		if (values[13] == 0):
			self.LCD_GPU_FREQ.setStyleSheet( "color: #C0C0C0;" )
		else:
			self.LCD_GPU_FREQ.setStyleSheet( "color: #0000FF;" )

		# GPU Util
		if (values[14] <= 0):
			self.LCD_GPU_UTIL.setStyleSheet( "color: #C0C0C0;" )		
		elif (values[14] >= 80): # default
			self.LCD_GPU_UTIL.setStyleSheet( "color: #FF0000;" )
		else:
			self.LCD_GPU_UTIL.setStyleSheet( "color: #0000FF;" )

		# APT
		if (values[22] >= Max_Temperature):
			self.LCD_APT.setStyleSheet( "color: #FF0000;" )
		else:
			self.LCD_APT.setStyleSheet( "color: #000000;" )

		# PST
		if (values[23] >= Max_Temperature):
			self.LCD_PST.setStyleSheet( "color: #FF0000;" )
		else:
			self.LCD_PST.setStyleSheet( "color: #000000;" )

		# GPU
		if (values[21] <= 0):
			self.LCD_GPU.setStyleSheet( "color: #C0C0C0;" )
		elif (values[14] >= 60): 
			self.LCD_GPU.setStyleSheet( "color: #FF0000;" )		
		else:
			self.LCD_GPU.setStyleSheet( "color: #000000;" )

		self.LCD_DVFS_MAX.display('%.f' % values[15])
		self.LCD_DVFS_MIN.display('%.f' % values[16])
		self.LCD_GPU_FREQ.display('%.f' % values[13])
		self.LCD_GPU_UTIL.display('%.f' % values[14])
		self.LCD_DDR.display('%.f' % values[17])
		self.LCD_BUS.display('%.f' % values[18])

		self.LCD_APT.display('%.1f\'' % values[22])
		self.LCD_PST.display('%.1f\'' % values[23])	
		self.LCD_CPU_G0.display('%.1f\'' % values[19])
		self.LCD_CPU_G1.display('%.1f\'' % values[20])
		self.LCD_GPU.display('%.1f\'' % values[21])

		self.LCD_CPU0.display('%.f' % values[1])
		self.LCD_CPU1.display('%.f' % values[2])
		self.LCD_CPU2.display('%.f' % values[3])
		self.LCD_CPU3.display('%.f' % values[4])
		self.LCD_CPU4.display('%.f' % values[5])
		self.LCD_CPU5.display('%.f' % values[6])
		self.LCD_CPU6.display('%.f' % values[7])
		self.LCD_CPU7.display('%.f' % values[8])

		# graph
		padd = [None]*(100-self.timeindex)

		self.lineA[0].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[1].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[2].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[3].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[4].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[5].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[6].set_ydata(self.mCPU0[-100:] + padd)
		self.lineA[7].set_ydata(self.mCPU0[-100:] + padd)

		self.lineB[0].set_ydata(self.mDVFS_Max[-100:] + padd)
		self.lineB[0].set_ydata(self.mDVFS_Min[-100:] + padd)
		self.lineB[1].set_ydata(self.mDDR[-100:]      + padd)
		self.lineB[2].set_ydata(self.mBUS[-100:]      + padd)
		self.lineB[3].set_ydata(self.mGPUFreq[-100:]  + padd)
		self.lineB[4].set_ydata(self.mGPUUtil[-100:]  + padd)
		self.lineB[5].set_ydata(self.mAPT[-100:]      + padd)
		self.lineB[6].set_ydata(self.mPST[-100:]      + padd)
		self.lineB[7].set_ydata(self.mCPUG0[-100:]    + padd)
		self.lineB[7].set_ydata(self.mCPUG1[-100:]    + padd)
		self.lineB[7].set_ydata(self.mGPU[-100:]      + padd)

		print ('Update is done')

	def StartButton(self):		
		print ('StartButton')
		Device_Info(self.listWidget)		
		self.duration = 1000
		self.showfreq = ShowFreq(self.duration)
		self.ani = animation.FuncAnimation(self.figB, self.update, blit=False, interval=10e0)

	
	def StopButton(self):
		print ('StopButton')
		#self.thread.cancel()
		#self.showfreq.Terminate()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	
	main.show()
	
	sys.exit(app.exec_())