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
		self.mCPU0 = []
		self.mCPU1 = []
		self.mCPU2 = []
		self.mCPU3 = []
		self.mCPU4 = []
		self.mCPU5 = []
		self.mCPU6 = []
		self.mCPU7 = []

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
		#time index
		self.timeindex 	= 0

		#init CPU information panel
		self.fig1 = Figure()
		self.canvas1 = FigureCanvas(self.fig1)
		self.Layout_CPU.addWidget(self.canvas1)

		self.ax1 = [ self.fig1.add_subplot(811), self.fig1.add_subplot(812), self.fig1.add_subplot(813), self.fig1.add_subplot(814),
					 self.fig1.add_subplot(815), self.fig1.add_subplot(816), self.fig1.add_subplot(817), self.fig1.add_subplot(818)	]
		
		#init System information panel
		self.fig2 = Figure()
		self.canvas2 = FigureCanvas(self.fig2)
		self.Layout_System.addWidget(self.canvas2)

		# make plots
		self.ax2  = [ self.fig2.add_subplot(811), self.fig2.add_subplot(812), self.fig2.add_subplot(813), self.fig2.add_subplot(814),
					  self.fig2.add_subplot(815), self.fig2.add_subplot(816), self.fig2.add_subplot(817), self.fig2.add_subplot(818) ]

		# draw horizontal line
		#ax[0].axhline(y=0.5, xmin=0, xmax=1, color='#FF0000', linewidth=4)
			
		# draw vertical line
		#ax[0].axvline(x=50, ymin=0, ymax=1, color='#006000', linewidth=4)

			

	def setup_CPU_chart(self):
		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)
 
		# make plots
		for i in xrange(0,8):
			self.ax1[i].clear()
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			ticklines = self.ax1[i].get_xticklines()
			ticklines.extend( self.ax1[i].get_yticklines() )
			gridlines = self.ax1[i].get_xgridlines()
			gridlines.extend( self.ax1[i].get_ygridlines() )
			ticklabels = self.ax1[i].get_xticklabels()
			ticklabels.extend( self.ax1[i].get_yticklabels() )

			for line in ticklines:
				line.set_color('#00C040')
				line.set_linewidth(1)

			for line in gridlines:
				line.set_color('#00C040')
				line.set_linestyle('-')			

			for label in ticklabels:
				label.set_color('#404040') # drak grey
				label.set_fontsize('8') # or 'small'

			#self.ax1[0].axis([0,100,0,2100])
			self.ax1[i].set_autoscale_on(False)

			# show grid
			self.ax1[i].grid(True)

			# set your xticks manually (10 ticks)
			self.ax1[i].xaxis.set_ticks(numpy.arange(0,100,2.5)) # [i for i in range(0,100, 10)]

			# set your yticks manually (10 ticks)
			self.ax1[i].yaxis.set_ticks(numpy.arange(0, 1401 if i < 4 else 2201, 200))
			
			# remove label
			self.ax1[i].set_xticklabels([])

			self.ax1[i].set_axis_bgcolor((0, 0, 0))

		# Y labels
		self.ax1[0].set_ylabel('CPU0')
		self.ax1[1].set_ylabel('CPU1')
		self.ax1[2].set_ylabel('CPU2')
		self.ax1[3].set_ylabel('CPU3')
		self.ax1[4].set_ylabel('CPU4')
		self.ax1[5].set_ylabel('CPU5')
		self.ax1[6].set_ylabel('CPU6')
		self.ax1[7].set_ylabel('CPU7')

		self.fig1.subplots_adjust(left=0.10, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)
		

	def setup_System_chart(self):
		## add navigation toolbar		
		#self.toolbar = NavigationToolbar(canvas, self.mplwindow, coordinates=True)
		#self.mplvl.addWidget(self.toolbar)

		for i in xrange(0,8):
			# ============================================
			# Setup chart properties, tick and grid etcs
			# ============================================
			ticklines = self.ax2[i].get_xticklines()
			ticklines.extend( self.ax2[i].get_yticklines() )
			gridlines = self.ax2[i].get_xgridlines()
			gridlines.extend( self.ax2[i].get_ygridlines() )
			ticklabels = self.ax2[i].get_xticklabels()
			ticklabels.extend( self.ax2[i].get_yticklabels() )

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
			self.ax2[i].grid(True)
			
			# set your xticks manually (10 ticks)
			self.ax2[i].xaxis.set_ticks(numpy.arange(0,100,3)) # [i for i in range(0,100, 10)]
		
			# remove label
			self.ax2[i].set_xticklabels([])

			self.ax2[i].set_axis_bgcolor((0, 0, 0))
			
			self.ax2[i].set_autoscale_on(False)
			

		# Y ticks
		self.ax2[0].yaxis.set_ticks(numpy.arange(0, 1201, 200)) # DVFS
		self.ax2[1].yaxis.set_ticks(numpy.arange(0, 1301, 200)) # DDR
		self.ax2[2].yaxis.set_ticks(numpy.arange(0, 1001, 100)) # BUS
		self.ax2[3].yaxis.set_ticks(numpy.arange(0, 1001, 100)) # GPU Freq
		self.ax2[4].yaxis.set_ticks(numpy.arange(0, 101, 10)) # GPU Util
		#self.ax2[5].yaxis.set_ticks(numpy.arange(30, 71, 5)) # APT
		#self.ax2[6].yaxis.set_ticks(numpy.arange(30, 71, 5)) # PST
		self.ax2[7].yaxis.set_ticks(numpy.arange(0, 71, 10)) # Temperature

		self.ax2[5].axis([0, 100, 30,70])
		self.ax2[6].axis([0, 100, 30,70])

		# Y labels
		self.ax2[0].set_ylabel('DVFS (MHz)')
		self.ax2[1].set_ylabel('DDR (MHz)')
		self.ax2[2].set_ylabel('BUS (MHz)')
		self.ax2[3].set_ylabel('GPU Freq (MHz)')
		self.ax2[4].set_ylabel('GPU Util (%)')
		self.ax2[5].set_ylabel('APT (C)')
		self.ax2[6].set_ylabel('PST (C)')
		self.ax2[7].set_ylabel('Temperature (C)')

		self.fig2.subplots_adjust(left=0.10, bottom=0.03, right=0.98, top=0.99, wspace=0.2, hspace=0.1)

	
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

		loc = self.timeindex	

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
		x = arange(100)
		padd = [None]*(100-loc)
		
		#draw graph, style, color, 
		width = 1.0
		anti = False


		self.ax1[0].plot(x, self.mCPU0[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[1].plot(x, self.mCPU1[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[2].plot(x, self.mCPU2[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[3].plot(x, self.mCPU3[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[4].plot(x, self.mCPU4[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[5].plot(x, self.mCPU5[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[6].plot(x, self.mCPU6[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		self.ax1[7].plot(x, self.mCPU7[-100:] + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti)
		
		#self.ax1[0].axvline(x=loc, ymin=0, ymax=1, color='#006000', linewidth=3)

		self.ax2[0].plot(x, self.mDVFS_Max[-100:] + padd, linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # DVFS
		self.ax2[0].plot(x, self.mDVFS_Min[-100:] + padd, linestyle='-', color='#0000FF', linewidth=width, antialiased=anti) # DVFS
		self.ax2[1].plot(x, self.mDDR[-100:]      + padd, linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # DDR
		self.ax2[2].plot(x, self.mBUS[-100:]      + padd, linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # BUS
		self.ax2[3].plot(x, self.mGPUFreq[-100:]  + padd, linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Freq
		self.ax2[4].plot(x, self.mGPUUtil[-100:]  + padd, linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Util	
		self.ax2[5].plot(x, self.mAPT[-100:]      + padd, linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # APT
		self.ax2[6].plot(x, self.mPST[-100:]      + padd, linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # PST		
		self.ax2[7].plot(x, self.mCPUG0[-100:]    + padd, linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # C0 Temperature
		self.ax2[7].plot(x, self.mCPUG1[-100:]    + padd, linestyle='-', color='#00FF00', linewidth=width, antialiased=anti) # C1 Temperature
		self.ax2[7].plot(x, self.mGPU[-100:]      + padd, linestyle='-', color='#0000FF', linewidth=width, antialiased=anti) # C2 Temperature

		self.canvas1.draw()
		self.canvas2.draw()

		self.canvas1.flush_events()
		self.canvas2.flush_events()
		#self.show()

		self.thread = Timer(self.duration/1000.0, self.update)
		self.thread.start()


		"""ax1 = self.ax1
		x = np.arange(0,100.0)
		y1 = (np.cos(2*np.pi*x/50.0)+1.0) * 1000
		
		#ax1[0].clear()
		ax1[0].plot(x, y1, linestyle='-', color='#00FF00', linewidth=2)
		self.canvas1.draw()
		self.canvas1.flush_events()
		self.show()"""
		
		print ('Update is done')

	def StartButton(self):		
		print ('StartButton')
		Device_Info(self.listWidget)		
		self.duration = 1000
		self.showfreq = ShowFreq(self.duration)
		self.update() 
		self.thread = Timer(0.5, self.update)
		self.thread.start()
		#ani animation.FuncAnimation(fig, animate, interval = 10)

	
	def StopButton(self):
		print ('StopButton')
		#self.thread.cancel()
		#self.showfreq.Terminate()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	main.setup_CPU_chart()
	main.setup_System_chart()
	#main.update()
	main.show()
	#main.update()
	
	sys.exit(app.exec_())