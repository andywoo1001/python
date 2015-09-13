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
from PyQt4.QtGui import *
import os


Ui_MainWindow, QMainWindow = loadUiType('window_v6.ui')


ADB 			= 'adb '
UNKNOWN, NOBLE, J2 = range(3)
DEVICE_MODEL	= ''		# (NOBLE,J2)
DEVICE_SERIAL 	= ''		# 05157df5dc24b01b
DEVICE_CHIP 	= ''		# universal7420 or universal3475
DEVICE_PRODUCT  = ''		# noblelteatt, j2lte etc
MainWindow 		= None

def LogTime():
	return time.strftime("%H:%M:%S") #%Y-%m-%d 

class ShowFreq():
	def __init__(self):
		pass

	def Enable(self,milliseconds):
		self.proc = subprocess.Popen(['adb', 'shell', '/sdcard/showfreq', '%s' % milliseconds ], stdout=subprocess.PIPE)

	def Disable(self):
		self.proc.kill()

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


def Wait_for_Device():
#	DisplayMsg("Please connect a device.\nWaiting for device ready...")
	QMessageBox.information( MainWindow, "Message Box", "Detecting Device\n\nPlease connect a device", QMessageBox.Ok);
	
#	statusTextEdit.update()
	system(ADB + 'wait-for-devices')
#	DisplayMsg("Done")	

def Detect_Device():
	global MainWindow,statusTextEdit	

	global	ADB, DEVICE_MODEL, DEVICE_SERIAL, DEVICE_CHIP, DEVICE_PRODUCT
	ADB = 'adb '
	Wait_for_Device()
	
#	DisplayMsg("\nDetecting Devices")
	devices_str	= subprocess.check_output('adb devices', shell=True) 
	Device_List	= re.findall('([0-9].*)\sdevice', devices_str)
	nDevices 	= len(Device_List)

	# No device is detected
	if( nDevices == 0):
		QMessageBox.critical(MainWindow, 'Device', "No device found !", QMessageBox.Ok )
		return
		#sys.exit(1)
	
#	DisplayMsg('%d device(s) detected' % nDevices)
	logging.debug(Device_List)

	
	index = 0
	Devices = []
	Device_Option = ''
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
			QMessageBox.critical(MainWindow, 'Device', "Unknown device !\n%s" % device_chip, QMessageBox.Ok )
			return False

		
		logging.info('[%2d] Serial No.: %s, Device Model: %s (%s), Board chipset: %s' % (index, device_serial, device_model, device_product, device_chip))
		Devices.append([device_model, device_serial, device_chip, device_product])
		Device_Option += '[Option %2d] \n Serial No.: %s\n Device Model: %s (%s)\n Board chipset: %s\n\n' % (index, device_serial, device_model, device_product, device_chip)
		index+=1
	
	if(nDevices == 1):
		logging.info('Only one device is found. The default device is chosen')
		DEVICE_MODEL 	= Devices[0][0]
		DEVICE_SERIAL 	= Devices[0][1]
		DEVICE_CHIP 	= Devices[0][2]
		DEVICE_PRODUCT 	= Devices[0][3].upper()
		#DisplayMsg("Serial No.: %s, Device Model: %s (%s), Board chipset: %s" % (index, device_serial, device_model, device_product, device_chip))
	else:
		select, ok = QtGui.QInputDialog.getText(MainWindow, 'Device option', Device_Option + '\nChoose one device: ')
		select = int(select)

		#select = int(input('Choose one device: '))
		#if( select >= nDevices) :
		#	logging.error('Wrong device selection %d', select)
		#	sys.exit(1)			
		DEVICE_MODEL 	= Devices[select][0]
		DEVICE_SERIAL 	= Devices[select][1]
		DEVICE_CHIP 	= Devices[select][2]
		DEVICE_PRODUCT  = Devices[select][3].upper()		

	logging.info('Serial No.: %s, Device Model: %s (%s), Board chipset: %s is selected' % (DEVICE_SERIAL, DEVICE_MODEL, DEVICE_PRODUCT, DEVICE_CHIP))
#	DisplayMsg('Serial No.: %s, Device Model: %s (%s), Board chipset: %s is selected' % (DEVICE_SERIAL, DEVICE_MODEL, DEVICE_PRODUCT, DEVICE_CHIP))

	# adb -s XXX setting
	ADB = 'adb -s %s ' % DEVICE_SERIAL
	logging.debug('adb device command is: \'%s\'' % ADB)
	return True
	
def Device_Info(listWidget):
	#Wait_for_Device()

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

def Copy_Files_To_Device():
	result = QMessageBox.question(MainWindow, 'Message', "Would you like to install 'show_freq' file ? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
	# to install spr and event files
	if result == QMessageBox.Yes:		
		system(ADB + 'push ./resources/showfreq /sdcard/')
		system(ADB + 'push ./resources/event_record /sdcard/')
		system(ADB + 'push ./resources/event_replay /sdcard/')		
		QMessageBox.information( MainWindow, "Message Box", "showfreq, event_record and event_replay are installed", QMessageBox.Ok);


	#else:
		#DisplayMsg('Installation(showfreq,event_record,apk) is cancelled')	


class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		super(Main, self).__init__()
		self.setupUi(self)
		self.pushButton_Start.clicked.connect(self.StartButton)
		#self.pushButton_Start.setIcon(QIcon(QPixmap('./res/Start.png')))
		self.pushButton_Stop.clicked.connect(self.StopButton)
		self.SlideBar.valueChanged.connect(self.UpdateShowFreq)
		self.actionConnect.triggered.connect(self.ActionConnect)		
		self.actionInstall2Device.triggered.connect(self.ActionInstall2Device)
		self.actionEventRecord.triggered.connect(self.ActionEventRecord)
		self.actionEventStop.triggered.connect(self.ActionEventStop)
		self.actionEventReplay.triggered.connect(self.ActionEventReplay)
		self.actionCaptureScreen.triggered.connect(self.ActionCaptureScreen)
		self.actionMP4_Recording.triggered.connect(self.ActionMP4_Recording)
		self.actionPerformanceMode.triggered.connect(self.ActionPerformanceMode)
		self.actionNormalMode.triggered.connect(self.ActionNormalMode)

		MainWindow = self

		self.showfreq = ShowFreq()
		self.showfreq_value = 1000
		
		#time index
		self.timeindex 	= 0
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

		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		self.Layout_System.addWidget(self.canvas)


		self.ax = [ self.fig.add_subplot(911), self.fig.add_subplot(912), self.fig.add_subplot(913), self.fig.add_subplot(914),
					self.fig.add_subplot(915), self.fig.add_subplot(916), self.fig.add_subplot(917), self.fig.add_subplot(918), self.fig.add_subplot(919)]
		
		#draw graph, style, color, 
		width = 2.0
		anti = True
		line0, = self.ax[0].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti) # CPU_Little
		line1, = self.ax[1].plot([], [], linestyle='-', color='#00FF00', linewidth=width, antialiased=anti) # CPU_Big
		line2, = self.ax[2].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Util	
		line3, = self.ax[3].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # GPU Freq

		line4, = self.ax[4].plot([], [], linestyle='-', color='#FF0000', linewidth=4, antialiased=anti) # DVFS Max
		line5, = self.ax[4].plot([], [], linestyle='-', color='#0000FF', linewidth=width, antialiased=anti) # DVFS Min
		line6, = self.ax[5].plot([], [], linestyle='-', color='#FFA000', linewidth=width, antialiased=anti) # APT
		line7, = self.ax[5].plot([], [], linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # PST		
		line8, = self.ax[6].plot([], [], linestyle='-', color='#FFA000', linewidth=width, antialiased=anti) # C0 Temperature
		line9, = self.ax[6].plot([], [], linestyle='-', color='#FF0000', linewidth=width, antialiased=anti) # C1 Temperature
		line10,= self.ax[6].plot([], [], linestyle='-', color='#FFFF00', linewidth=width, antialiased=anti) # G2 Temperature
				
		line11,= self.ax[7].plot([], [], linestyle='-', color='#C0C0C0', linewidth=width, antialiased=anti) # DDR
		line12,= self.ax[8].plot([], [], linestyle='-', color='#C0C0C0', linewidth=width, antialiased=anti) # BUS
		
		
		self.lines = [line0,line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12]
		
		# Y labels
		self.ax[0].set_ylabel('CPU Little')
		self.ax[1].set_ylabel('CPU Big')
		self.ax[2].set_ylabel('GPU Util (%)')
		self.ax[3].set_ylabel('GPU Freq (MHz)')
		self.ax[4].set_ylabel('DVFS (MHz)')
		self.ax[5].set_ylabel('APT/PST (C)')
		self.ax[6].set_ylabel('Temperature (C)')
		self.ax[7].set_ylabel('DDR (MHz)')		
		self.ax[8].set_ylabel('BUS (MHz)')

		# Y ticks		
		self.ax[0].yaxis.set_ticks(numpy.arange(0, 1601, 200)) # CPU0
		self.ax[1].yaxis.set_ticks(numpy.arange(0, 2201, 200)) # CPU1
		self.ax[2].yaxis.set_ticks(numpy.arange(0, 101, 20)) # GPU Util
		self.ax[3].yaxis.set_ticks(numpy.arange(0, 801, 100)) # GPU Freq
		self.ax[4].yaxis.set_ticks(numpy.arange(0, 1201, 200)) # DVFS
		self.ax[5].axis([0, 100, 30,70]) # APT,PST
		self.ax[6].axis([0, 100, 30,70]) #.yaxis.set_ticks(numpy.arange(0, 71, 10)) # Temperature		
		self.ax[7].yaxis.set_ticks(numpy.arange(0, 1601, 200)) # DDR
		self.ax[8].yaxis.set_ticks(numpy.arange(0, 801, 100)) # BUS
		
		# ============================================
		# Setup chart properties, tick and grid etcs
		# ============================================		
		for i in range(0,9):
			ticklines = self.ax[i].get_xticklines()
			ticklines.extend( self.ax[i].get_yticklines() )
			gridlines = self.ax[i].get_xgridlines()
			gridlines.extend( self.ax[i].get_ygridlines() )
			ticklabels = self.ax[i].get_xticklabels()
			ticklabels.extend( self.ax[i].get_yticklabels() )

			for line in ticklines:
				line.set_color('#00C040')
				line.set_linewidth(1)

			for line in gridlines:
				line.set_color('#00C040')
				line.set_linestyle('-')			

			for label in ticklabels:
				label.set_color('#404040') # drak grey
				label.set_fontsize('8') # or 'small'
						# show grid
			
			# disable auto scale
			self.ax[i].set_autoscale_on(False)

			self.ax[i].grid(True)

			#background color
			self.ax[i].set_axis_bgcolor((0, 0, 0))
			
			# set your xticks manually 
			self.ax[i].xaxis.set_ticks(numpy.arange(0,100,2.5)) # [i for i in range(0,100, 10)]
	
			# remove label
			self.ax[i].set_xticklabels([])

		self.fig.subplots_adjust(left=0.10, bottom=0.01, right=0.98, top=0.99, wspace=0.2, hspace=0.1)

		# set x data
		x = range(100)
		for line in self.lines:
			line.set_xdata(x)

		self.enable_display = False

		
	def update_lines(self, data):
		if (self.enable_display == False): 
			for line in self.lines:
				line.set_ydata([None]*100)
			return self.lines


		values = self.showfreq.GetValues()
		#print ('value=', values)
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
			self.LCD_GPU_FREQ.setStyleSheet( "color: #999900" )

		# GPU Util
		if (values[14] <= 0):
			self.LCD_GPU_UTIL.setStyleSheet( "color: #C0C0C0;" )		
		#elif (values[14] >= 80): # default
		#	self.LCD_GPU_UTIL.setStyleSheet( "color: #FF0000;" )
		else:
			self.LCD_GPU_UTIL.setStyleSheet( "color: #999900;" )

		# APT
		if (values[22] >= Max_Temperature):
			self.LCD_APT.setStyleSheet( "color: #FFA000;" )
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
		#elif (values[14] >= 60): 
		#	self.LCD_GPU.setStyleSheet( "color: #FF0000;" )		
		else:
			self.LCD_GPU.setStyleSheet( "color: #999900;" )

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

		padd = [None]*(100-self.timeindex)

		if (self.enable_display == True): 
			self.lines[0].set_ydata(self.mCPU0[-100:] 	  + padd)
			self.lines[1].set_ydata(self.mCPU4[-100:] 	  + padd)
			self.lines[2].set_ydata(self.mGPUUtil[-100:]  + padd)
			self.lines[3].set_ydata(self.mGPUFreq[-100:] + padd)			
			self.lines[4].set_ydata(self.mDVFS_Max[-100:] + padd)
			self.lines[5].set_ydata(self.mDVFS_Min[-100:] + padd)
			self.lines[6].set_ydata(self.mAPT[-100:]      + padd)
			self.lines[7].set_ydata(self.mPST[-100:]      + padd)
			self.lines[8].set_ydata(self.mCPUG0[-100:]    + padd)
			self.lines[9].set_ydata(self.mCPUG1[-100:]    + padd)
			self.lines[10].set_ydata(self.mGPU[-100:]     + padd)			
			self.lines[11].set_ydata(self.mDDR[-100:]     + padd)
			self.lines[12].set_ydata(self.mBUS[-100:]     + padd)			
		else:
			for line in self.lines:
				line.set_ydata([None]*100)

		return self.lines


	def StartButton(self):		
		self.showfreq.Enable(self.showfreq_value)
		self.enable_display = True
		print ('StartButton')

		
	def StopButton(self):
		self.enable_display = False
		print ('StopButton')

	def UpdateShowFreq(self, value):		
		self.showfreq_value = int(10**(value/10.0))
		print(self.showfreq_value)
		self.showfreq.Disable()
		self.showfreq.Enable(self.showfreq_value)		

	# Detect attached devices and choose one
	# Find the device information for chosen one
	def ActionConnect(self):		
		ret = Detect_Device()
		if(ret == True):
			Device_Info(self.listWidget)
	
	# Copy Benchmark and Event files to the device
	def ActionInstall2Device(self):
		Copy_Files_To_Device()

	def ActionCaptureScreen(self):
		system(ADB + 'shell screencap -p /sdcard/screen.png')
		filename = QFileDialog.getSaveFileName(self, 'Save File', './',  "png (*.png)")
		system(ADB + 'pull /sdcard/screen.png ' + str(filename) + '.png')
		system(ADB + 'shell rm /sdcard/screen.png')
	
	def ActionPerformanceMode(self):
		system(ADB + 'remount')
		system(ADB + 'shell su -c setenforce 0')
		system(ADB + 'shell \"echo 1500000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq\"')
		system(ADB + 'shell \"echo 1500000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq\"')
		system(ADB + 'shell \"echo 2100000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq\"')
		system(ADB + 'shell \"echo 2100000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq\"')
		#system(ADB + 'shell echo 700 > /sys/devices/14ac0000.mali/dvfs_min_lock')
		#system(ADB + 'shell echo 700 > /sys/devices/14ac0000.mali/dvfs_max_lock')

	def ActionNormalMode(self):
		system(ADB + 'remount')
		system(ADB + 'shell su -c setenforce 0')
		system(ADB + 'shell \"echo  400000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq\"')
		system(ADB + 'shell \"echo 1500000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq\"')
		system(ADB + 'shell \"echo  800000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq\"')
		system(ADB + 'shell \"echo 2100000 > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq\"')

	def ActionEventRecord(self):
		system(ADB+'shell /sdcard/event_record &')		
		proc = subprocess.check_output(ADB + "shell ps | grep event_record | awk {'print $2'}", shell=True)
		self.PID = re.findall('\d+', proc)
		print (self.PID)
		
	def ActionEventStop(self):
		for pid in self.PID:
			system(ADB+'shell kill %d' % int(pid))
			print('kill %d' % int(pid))
		

	def ActionEventReplay(self):
		system(ADB+'shell /sdcard/event_replay &')
		#self.PID  = int(subprocess.check_output(ADB + "shell /sdcard/event_record", shell=True))

	def ActionMP4_Recording(self):
		pass
#		system(ADB+'shell screenrecord /sdcard/recording.mp4 &')		
#		proc = subprocess.check_output(ADB + "shell ps | grep screen_record | awk {'print $2'}", shell=True)
#		self.PID = re.findall('\d+', proc)
#		
#		filename = QFileDialog.getSaveFileName(self, 'Save File', './',  "mp4 (*.mp4)")
#		system(ADB + 'pull /sdcard/recording.mp4 ' + str(filename) + '.mp4')
					

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)		# filename=('%s' % File_Log),
	logging.info("[%s] Start Logging " % LogTime() )

	app = QtGui.QApplication(sys.argv)
	main = Main()
	#main.update_lines()
	ani = animation.FuncAnimation(main.fig, main.update_lines, blit=True, interval=10)
	
	main.show()
	sys.exit(app.exec_())