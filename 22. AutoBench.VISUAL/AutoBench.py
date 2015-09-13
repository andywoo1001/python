# convert resource:  pyrcc4 -o resources_rc.py resources.qrc
import os
import sys
import time
import logging
import subprocess
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt4 import QtGui
from pylab import *
from os import system
from threading import Timer,Thread,Event
from pylab import *
from PyQt4.QtGui import *
from time import sleep		# time.sleep(1.0) to sleep(1.0)

SYSTRACE 			= '/home/insu13.yu/Android/android-sdk-linux/platform-tools/systrace/systrace.py'

# Check CPU & GPU clocks

Ui_MainWindow, QMainWindow = loadUiType('window_form.ui')

ADB 			= 'adb '
SKIAPR_APK 		= 'com.samsung.skiapr'

APK_LIST		= None
# Device variables
UNKNOWN, NOBLE, J2 = range(3)
DEVICE_MODEL	= ''		# (NOBLE,J2)
DEVICE_SERIAL 	= ''		# 05157df5dc24b01b
DEVICE_CHIP 	= ''		# universal7420 or universal3475
DEVICE_PRODUCT  = ''		# noblelteatt, j2lte etc

statusTextEdit 	= None
MainWindow 		= None

Status = [ {'Connection': False },
		   {'File Install' : False },
		   {'Config Setting' : False } ]


FLAGS = {
	'BENMK_Drawtime' 		: False,
	'BENMK_Launching' 		: False,
	'BENMK_Memory' 			: False,
	'DEBUG_Excel' 			: False,
	'DEBUG_Systrace' 		: False,
	'DEBUG_DrawtimeGraph' 	: False,
	'DEBUG_ColorDebug' 		: False,
	'DEBUG_ScreenCapture' 	: False,
	'DEBUG_SVG' 			: False,
	'DEBUG_PathGroupInfo' 	: False,
	'DEBUG_PathCacheInfo' 	: False
}

EXYNOS3 = {
	'GPU_MIN' 		 : '/sys/devices/11400000.mali/dvfs_min_lock',
	'GPU_MAX'		 : '/sys/devices/11400000.mali/dvfs_max_lock',
	'CPU_MIN' 		 : '/sys/devices/system/cpu/cpufreq/cpufreq_min_limit',
	'CPU_MAX' 		 : '/sys/devices/system/cpu/cpufreq/cpufreq_max_limit',
	'CPU_FREQ_TABLE' : '/sys/devices/system/cpu/cpufreq/cpufreq_table',
	'GPU_FREQ_TABLE' : '/sys/devices/11400000.mali/dvfs_table'	
}

EXYNOS7 = {
	'GPU_MIN' 			: '/sys/devices/14ac0000.mali/dvfs_min_lock',
	'GPU_MAX' 			: '/sys/devices/14ac0000.mali/dvfs_max_lock',
	'CPU0_MIN' 			: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq',
	'CPU0_MAX' 			: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq', 
	'CPU1_MIN' 			: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq',
	'CPU1_MAX' 			: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq',
	'CPU0_FREQ_TABLE'	: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_freq_table',
	'CPU1_FREQ_TABLE' 	: '/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_freq_table',
	'GPU_FREQ_TABLE' 	: '/sys/devices/14ac0000.mali/dvfs_table'
}

DIRS = {
	'INIT':None,			# Launching directory
	'ROOT':None,
	#'OUTPUT':None,
	'WORK':None,
}

FILENAMES = {
#	'FILE_LOG':None,
	'FILE_CONFIG_CFG':None,
	# Benchmark
	'FILE_DRAWTIME_CSV':None,
	'FILE_SURFACEFLINGER_CSV':None,
	'FILE_SKIAPR_CSV':None,
	'FILE_LAUCHING_CSV':None,
	'FILE_MEMORY_CSV':None,
	# Debug
	'FILE_SYSTRACE_HTML':None,
	'FILE_DRAWTIME_PNG':None,
	'FILE_COLORDEBUG_PNG':None,
	'FILE_SCREENCAPTURE_PNG':None,
	'FILE_SVG_SVG:None':None,
	'FILE_PATHGROUP_TXT':None,
	'FILE_PATHCACHE_TXT':None,
	'FILE_EXCEL_XLS':None
}

def Create_Root_Dir():
	PWD				= os.getcwd()
	DATE_TIME		= time.strftime("%Y%m%dT%H%M%S")
	ROOT_DIR 		= PWD + '/' + DATE_TIME + '_'  + DEVICE_PRODUCT
	
	DisplayMsg('Output directory is: %s' % ROOT_DIR)
	if not os.path.exists(ROOT_DIR):
		os.makedirs(ROOT_DIR)
	
	DIRS['INIT']			= PWD
	DIRS['ROOT']			= ROOT_DIR	
	os.chdir(ROOT_DIR)


def Update_Current_Dir(Package):
	#FILES['FILE_LOG']				= 'LOG_' + Package + '.log'
	FILES['FILE_SYSTRACE_HTML']		= 'Systrace_' 	+ Package + '.html'
	FILES['FILE_DRAWTIME_PNG']		= 'Drawtime_' 	+ Package + '.png'
	FILES['FILE_COLORDEBUG_PNG']	= 'ColorDebug_' + Package + '.png'
	FILES['FILE_SCREENCAPTURE_PNG']	= 'Capture_' 	+ Package + '.png'
	FILES['FILE_SVG_SVG']			= 'SVG_'		+ Package + '.svg'
	FILES['FILE_PATHGROUP_TXT']		= 'PathGroup_'	+ Package + '.txt'
	FILES['FILE_PATHCACHE_TXT']		= 'PathCache_'	+ Package + '.txt'
	FILES['FILE_EXCEL_XLS']			= 'Excel_'		+ Package + '.xls'

	pass



def LogTime():
	return time.strftime("%H:%M:%S") #%Y-%m-%d 

def Execute(commands):
	process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return process.stdout, process.stderr

def Bash(parameters):
	result = subprocess.check_output(parameters, shell=True)
	return result

def BashADB(parameters):
	result = subprocess.check_output(ADB + parameters, shell=True)
	return result

def BashADBshell(parameters):
	result = subprocess.check_output(ADB + 'shell ' + parameters, shell=True)
	return result

def BashADBcat(parameters):
	result = subprocess.check_output(ADB + 'shell cat ' + parameters, shell=True)
	return result


def DisplayMsg(msg):
	global statusTextEdit
	statusTextEdit.append(msg)

def Wait_for_Device():
	DisplayMsg("Please connect a device.\nWaiting for device ready...")
	QMessageBox.information( MainWindow, "Message Box", "Detecting Device\n\nPlease connect a device", QMessageBox.Ok);
	
	statusTextEdit.update()
	system(ADB + 'wait-for-devices')
	DisplayMsg("Done")	

def Detect_Device():
	global MainWindow,statusTextEdit	

	global	ADB, DEVICE_MODEL, DEVICE_SERIAL, DEVICE_CHIP, DEVICE_PRODUCT
	ADB = 'adb '
	Wait_for_Device()
	
	DisplayMsg("\nDetecting Devices")
	devices_str	= subprocess.check_output('adb devices', shell=True) 
	Device_List	= re.findall('([0-9].*)\sdevice', devices_str)
	nDevices 	= len(Device_List)

	# No device is detected
	if( nDevices == 0):
		QMessageBox.critical(MainWindow, 'Device', "No device found !", QMessageBox.Ok )
		return
		#sys.exit(1)
	
	DisplayMsg('%d device(s) detected' % nDevices)
	#logging.debug(Device_List)

	
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

		
		#logging.info('[%2d] Serial No.: %s, Device Model: %s (%s), Board chipset: %s' % (index, device_serial, device_model, device_product, device_chip))
		Devices.append([device_model, device_serial, device_chip, device_product])
		Device_Option += '[Option %2d] \n Serial No.: %s\n Device Model: %s (%s)\n Board chipset: %s\n\n' % (index, device_serial, device_model, device_product, device_chip)
		index+=1
	
	if(nDevices == 1):
		#logging.info('Only one device is found. The default device is chosen')
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

	#logging.info('Serial No.: %s, Device Model: %s (%s), Board chipset: %s is selected' % (DEVICE_SERIAL, DEVICE_MODEL, DEVICE_PRODUCT, DEVICE_CHIP))
	DisplayMsg('Serial No.: %s, Device Model: %s (%s), Board chipset: %s is selected' % (DEVICE_SERIAL, DEVICE_MODEL, DEVICE_PRODUCT, DEVICE_CHIP))

	# adb -s XXX setting
	ADB = 'adb -s %s ' % DEVICE_SERIAL
	#logging.debug('adb device command is: \'%s\'' % ADB)
	return True
	
def Device_Info(listWidget):
	#Wait_for_Device()

	# Display build information
	listWidget.clear()
	listWidget.addItem('== DEVICE INFORMATION ==')

	# Get /system/build.prop file for device infomation
	display  = subprocess.check_output(ADB + 'shell dumpsys window displays | grep init=', shell=True)
	Resolution = re.findall('init=(\d+x\d+ \d+dpi)', display)[0]
	listWidget.addItem('Resolution: %s' % Resolution )

	GLES  = subprocess.check_output(ADB + 'shell dumpsys SurfaceFlinger | grep GLES:', shell=True)
	version = re.findall('GLES: (.*)', GLES)[0][:-1]
	listWidget.addItem('GLES: %s' % version )


	# Get /system/build.prop file for device infomation
	prop  = subprocess.check_output(ADB + 'shell cat /system/build.prop', shell=True) #  ro.product.board

	
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

def Copy_Files_To_Device(progressBar):
	result = QMessageBox.question(MainWindow, 'Message', "Would you like to install SKIAPR.apk and event_record, event_reply and showfreq? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
	# to install spr and event files
	if result == QMessageBox.Yes:
		DisplayMsg('Copying tool(showfreq,event_record,apk) files...')
		system('find ./install/tools/* -exec %s push {} /sdcard/ \;' % ADB)
		system(ADB + 'install -r ./install/apk/SKIAPR')
		DisplayMsg('Done')
	else:
		DisplayMsg('Installation(showfreq,event_record,apk) is cancelled')
 
	
	result = QMessageBox.question(MainWindow, 'Message', "Would you like to remove /sdcard/spr and \n copy \'.spr\' and \'events\' files to android device ? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) 
	# to install spr and event files
	

	if result == QMessageBox.Yes:
		DisplayMsg('Copy spr, event to the device...')
		system(ADB + 'shell rm -rf /sdcard/spr')
		system(ADB + 'shell mkdir /sdcard/spr')
		system(ADB + 'shell mkdir /sdcard/spr/binary')
		system(ADB + 'shell mkdir /sdcard/spr/binary/spr')
		system(ADB + 'shell mkdir /sdcard/spr/binary/spr/NOBLE')
		system(ADB + 'shell mkdir /sdcard/spr/binary/spr/J2')


		# Make spr list
		NobleFileList = []
		J2FileList = []
		for filename in os.listdir('./install/spr/J2'):
			if filename.endswith(".spr"):
				J2FileList.append('./install/spr/J2/' + filename)

		for filename in os.listdir('./install/spr/NOBLE'):
			if filename.endswith(".spr"):
				NobleFileList.append('./install/spr/NOBLE/' + filename)
				
		DisplayMsg('Copying J2 and NOBLE(.spr, events) files...')
		
		total = len(J2FileList) + len(NobleFileList)
		count = 1
		progressBar.setValue(0)
		
		for file in J2FileList:
			DisplayMsg('copying ' + file + ' to /sdcard/spr/binary/spr/J2' )			
			result = Bash(ADB + 'push ' + file + ' /sdcard/spr/binary/spr/J2' )
			progressBar.setValue( int(float(count)/float(total)*100.0 ) )
			count += 1

		for file in NobleFileList:
			DisplayMsg('copying ' + file + ' to /sdcard/spr/binary/spr/NOBLE' )			
			result = Bash(ADB + 'push ' + file + ' /sdcard/spr/binary/spr/NOBLE' )
			progressBar.setValue( int(float(count)/float(total)*100.0 ) )
			count += 1

		DisplayMsg('Finished binary(spr and event) installation')
	else:
		DisplayMsg('Installation(spr and events) is cancelled')
		#system(ADB + 'install -r ./INSTALL/SKIAPR-debug.apk') """

def Load_Config(tableWidget, Filename):	
	global SKIAPR_APK
	DisplayMsg("\nLoading a config file (\'%s\') file" % (Filename) )

	try:
		f = open(Filename, 'r')		
		contents = f.readlines()
	except IOError:
		logging.error("[%s] Error: Cannot open \'%s\'" % (LogTime(), Filename))
		return
	else:		
		f.close()

	logging.info("\t%s lines are read from \'%s\'" % (len(contents), Filename))
	# remove comments
	contents = [re.sub(r" *#.*\n$",'',x) for x in contents]

	# remove empty lines
	contents = [x for x in contents if (x!= '' and x!='\n')]
	#contents = [x for x in contents if (not x== '' and not x=='\n')]

	# remove spaces (leave only one space:q)
	contents = [re.split(r"[ /]+", x) for x in contents]
		

	DisplayMsg("%s Applications or scenes test list" % len(contents))

	base  = 15
	index = 0
	for apk in contents:
		#logging.debug(apk)
		#logging.debug('APK info:' + apk)		
		parameters 	= len(apk)
		Package		= apk[0] 				# Package Name
		Activity  	= ''
		Task 		= ''
		File 		= ''
		if(Package == SKIAPR_APK): 		# SKIAPR case
			Activity = '.MainActivity'	# Activity Name
			Task = apk[1]				# Task name
			if Task == 'spr_file':
				if not parameters == 3:
					QMessageBox.critical(MainWindow, 'Loading Config File', "[%s] incorrect parameters(%d) @%s %s %s" % (Filename, parameters, apk[0], apk[1], apk[2]), QMessageBox.Ok )
					return
				File = apk[2]			# File name
			else:
				if not parameters ==2 :
					QMessageBox.critical(MainWindow, 'Loading Config File', "[%s] incorrect parameters(%d) @%s %s %s" % (Filename, parameters, apk[0], apk[1], apk[2]), QMessageBox.Ok )
					return
				File = 'NONE'
		else: # pre-installed apk case
	#		if not parameters ==3:
	#			logging.error("\tError: [%s] incorrect parameters(%d) @%s %s %s" % (Filename, parameters, apk[0], apk[1], apk[2]))
	#			sys.exit(1)
			Activity = apk[1]
			Task = 'NONE'
			File = apk[2]

		#logging.debug('[%2d] PACKAGE= %s, ACTIVITY= %s, TASK= %s, FILE= %s' % (index, Package, Activity, Task, File))
		#DisplayMsg('[%2d] PACKAGE= %s, ACTIVITY= %s, TASK= %s, FILE= %s' % (index, Package, Activity, Task, File))
		contents[index] = [Package, Activity, Task, File]

		index += 1
	# Write summary to XLSX file
	return contents

def Systrace(Duration, Filename):	
	DisplayMsg('Capturing Systrace sched gfx view for %d seconds' % Duration)
	commands = "%s --time=%d -o %s sched gfx view &" % ( SYSTRACE, int(Duration), Filename)
	subprocess.call(commands, shell=True)

def Enable_SPR_Mode(mode):
	if mode == True:
		BashADBshell('setprop debug.pr.path_pr all')
		#logging.info('SPR_MODE: ' + ADB + 'shell setprop debug.pr.path_pr all')
		return 'SPRALL_'
	else:
		BashADBshell('setprop debug.pr.path_pr none')
		#logging.info('SPR_MODE: ' + ADB + 'shell setprop debug.pr.path_pr none')
		return 'SPRNONE_'

def Run(tableWidget, progressBar):	
	global TASK_LIST
	# Create root direction for output
	Create_Root_Dir()


	index = 0
	size_of_list = len(TASK_LIST)
	for element in TASK_LIST:
		PACKAGE, ACTIVITY, TASK, FILE = element
		logging.info('[%d] APK is %s/%s  TASK= %s, FILE= %s' % (index, PACKAGE, ACTIVITY, TASK, FILE) )

		# Update Table
		#tableWidget.selectRow(index)
		#tableWidget.resizeColumnsToContents()
		
		
		# Update Progress bar
		progress_percentage = (float(index+1.0)/float(size_of_list))*100.00		
		progressBar.setValue(progress_percentage)
		index += 1
		sleep(1)

	# move back to launch directory
	os.chdir(DIRS['INIT'])

	"""apk_idx = 0
	for apk in APK_LIST:
		PACKAGE, ACTIVITY, TASK, FILE = apk
		
		# Task information
		logging.info('[%d] APK is %s/%s  TASK= %s, FILE= %s' % (task_idx, PACKAGE, ACTIVITY, TASK, FILE) )

		# Crate working directory and change to working directory for output
		WORK_DIR = Generate_Working_Directory(ROOT_DIR, PACKAGE, TASK, FILE)

		

		# PERFORMANCE TEST
		# Run N times for the same applications + 1 (systrace)
		for spr_on in range(2):
			SPR_MODE = Enable_SPR_Mode(spr_on)
			Init_LaunchTime_File(SPR_MODE+FILE_LAUNCHTIME)

			# Prepare SKIAPR TASK condition
			print ('PACKAGE = %s' % PACKAGE)
			if(PACKAGE == SKIAPR_APK):
				if(TASK == 'spr_file'):
					print('\t ' + ADB + 'shell setprop spr.test.case spr_file')
					logging.debug('\t ' + ADB + 'shell setprop spr.test.case spr_file')
					system(ADB + 'shell setprop spr.test.case spr_file')
					logging.debug('\t ' + ADB + 'shell cp /sdcard/spr/binary/%s /sdcard/spr/binary/test.spr' % FILE)
					system(ADB + 'shell cp /sdcard/spr/binary/%s /sdcard/spr/binary/test.spr' % FILE)
				else:
					logging.debug('\t ' + ADB + 'shell setprop %s' % TASK)
					system(ADB + 'shell setprop spr.test.case %s' % TASK)
			else: # Pre-install APK case
				logging.debug('\t '+ ADB + 'shell cp /sdcard/spr/binary/%s /sdcard/events' % FILE)
				system(ADB + 'shell cp /sdcard/spr/binary/%s /sdcard/events' % FILE)

			

			for iteration in range(RUN_ITERATION+1):

				# Iteration info
				logging.info('\tITERATION[%d]: %s' % (iteration, PACKAGE)  )

				FILE_DRAWTIME 	= SPR_MODE + FILE_NAMES[0] + '_I%d' % iteration + '.csv'
				FILE_SF_FPS 	= SPR_MODE + FILE_NAMES[1] + '_I%d' % iteration + '.csv'
				FILE_SKIAPR_FPS	= SPR_MODE + FILE_NAMES[2] + '_I%d' % iteration + '.csv'
				FILE_PNG 		= SPR_MODE + FILE_NAMES[3] + '_I%d' % iteration + '.png'
				FILE_SYSTRACE	= SPR_MODE + FILE_NAMES[4] + '_I%d_%s' % (iteration,PACKAGE) + '.html'
				FILE_LOG 		= SPR_MODE + FILE_NAMES[5] + '_I%d' % iteration + '.log'

				logging.debug('\t DrawTime:%s, SF:%s, SkiaPR:%s, PNG:%s, Systrace:%s' % (FILE_DRAWTIME, FILE_SF_FPS, FILE_SKIAPR_FPS, FILE_PNG, FILE_SYSTRACE))
							
				Wait_for_Device()
				Wait_for_Temperature(RUN_TEMPERATURE)
				APK_Start(PACKAGE, ACTIVITY, TASK, FILE, SPR_MODE+FILE_LAUNCHTIME)
				LOG_Clear()
				if iteration == RUN_ITERATION:
					Systrace(RUN_DURATION, FILE_SYSTRACE)
				else:
					if PACKAGE == SKIAPR_APK: # SKIAPR case
						logging.debug('Running SKIAPR (%s)', TASK)
						APK_Running(RUN_DURATION)
					else: # Pre-install APK case
						logging.debug('Running event_replay (%s) on %s', (FILE, PACKAGE) )
						system(ADB + 'shell /sdcard/spr/event_replay')
						# Launch events files


				LOG_Save(FILE_LOG)

				# For final iteration, Memory,PathCache,SurfaceFlinger,Screen capture
				if iteration == RUN_ITERATION:
					#FILE_MEMORY, FILE_PATHCACHE, FILE_SF
					FILE_CAPTURE	= PACKAGE + '_' + time.strftime("%Y%m%dT%H%M%S") + '.png'		# .png

					# Find PID of Package
					PID  = int(subprocess.check_output(ADB + "shell ps | grep %s | awk '{print $2}'" % (PACKAGE), shell=True))
					logging.debug('%s PID = %d' % (PACKAGE, int(PID)) )

					Memory_Info(PACKAGE, ACTIVITY, PID, SPR_MODE+FILE_MEMORY)
					PathCache_Info(PACKAGE, ACTIVITY, PID, SPR_MODE+FILE_PATHCACHE)
					SurfaceFlinger_Info(PACKAGE, ACTIVITY, PID, SPR_MODE+FILE_SF)
					Capture_Screen(PACKAGE, ACTIVITY, SPR_MODE+FILE_CAPTURE)
				
				APK_Stop(PACKAGE)

				# Process DrawTime
				Process_DrawTime(PACKAGE, FILE_LOG, FILE_DRAWTIME)
				Process_SurfaceFlingerFPS(FILE_LOG,FILE_SF_FPS)
				Process_SkiaPR(FILE_LOG, FILE_SKIAPR_FPS)
				Process_XLSX(FILE_DRAWTIME, FILE_SF_FPS, FILE_SKIAPR_FPS, PACKAGE, TASK, FILE, task_idx, iteration, spr_on)
				Graph(PACKAGE,FILE_DRAWTIME, FILE_PNG)
	task_idx +=1
	os.chdir(ROOT_DIR)
	"""


class Main(QMainWindow, Ui_MainWindow):
	def __init__(self, ):
		global statusTextEdit, MainWindow
		super(Main, self).__init__()
		self.setupUi(self)
		self.pushButton_Start.clicked.connect(self.StartButton)
		self.actionConnect.triggered.connect(self.ActionConnect)
		self.actionOpenConfig.triggered.connect(self.ActionOpenConfigFile)
		self.actionInstall2Device.triggered.connect(self.ActionInstall2Device)
		self.actionSystrace.triggered.connect(self.ActionSystrace)
		self.actionSystraceEvent.triggered.connect(self.ActionSystraceEvent)
		self.actionOpenSystraceFile.triggered.connect(self.ActionOpenSystraceFile)
		self.actionEventRecord.triggered.connect(self.ActionEventRecord)
		self.actionEventStop.triggered.connect(self.ActionEventStop)
		self.actionEventReplay.triggered.connect(self.ActionEventReplay)
		self.actionCaptureScreen.triggered.connect(self.ActionCaptureScreen)
		self.actionPerformanceMode.triggered.connect(self.ActionPerformanceMode)
		self.actionNormalMode.triggered.connect(self.ActionNormalMode)

			 
		statusTextEdit = self.statusTextEdit
		MainWindow = self
		self.progressBar.setValue(0)

		header = ['PACKAGE', 'ACTIVITY', 'TASK', 'FILE']
		self.tableWidget.setHorizontalHeaderLabels(header)

		self.tableWidget.setColumnCount(4)
		# set row count
		#self.tableWidget.setRowCount(10)
		self.tableWidget.setShowGrid(True)

		#self.tableWidget.setItem(1, 0, QtGui.QTableWidgetItem('ABCD'))
		# resize column 
		self.tableWidget.resizeColumnsToContents()
		# alignment
		#self.tableWidget.item(0,0).setTextAlignment(Qt.AlignRight)
		# 
		#self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft);

		#int row = self.tableWidget.rowCount();
		#self.tableWidget.insertRow(row);
		#self.tableWidget.setItem(row, 0, fileNameItem);
		#self.tableWidget.setItem(row, 1, sizeItem);
		self.UpdateCheckBoxStatus()

	def UpdateCheckBoxStatus(self):
		FLAGS['BENMK_Drawtime']			= self.chkboxBENMK_Drawtime.isChecked()
		FLAGS['BENMK_Launching'] 		= self.chkboxBENMK_Launching.isChecked()
		FLAGS['BENMK_Memory'] 			= self.chkboxBENMK_Memory.isChecked()
		FLAGS['DEBUG_Excel'] 			= self.chkboxDEBUG_Excel.isChecked()
		FLAGS['DEBUG_Systrace'] 		= self.chkboxDEBUG_Systrace.isChecked()
		FLAGS['DEBUG_DrawtimeGraph'] 	= self.chkboxDEBUG_DrawtimeGraph.isChecked()
		FLAGS['DEBUG_ColorDebug'] 		= self.chkboxDEBUG_ColorDebug.isChecked()
		FLAGS['DEBUG_ScreenCapture'] 	= self.chkboxDEBUG_ScreenCapture.isChecked()
		FLAGS['DEBUG_SVG'] 				= self.chkboxDEBUG_SVG.isChecked()
		FLAGS['DEBUG_PathGroupInfo'] 	= self.chkboxDEBUG_PathGroupInfo.isChecked()
		FLAGS['DEBUG_PathCacheInfo'] 	= self.chkboxDEBUG_PathCacheInfo.isChecked()

	def DVFS_Table(self):
		#print (DEVICE_MODEL, DEVICE_CHIP, DEVICE_PRODUCT)
		if(DEVICE_CHIP == 'universal7420'):		#N5
			CPU0tbl = BashADBcat(EXYNOS7['CPU0_FREQ_TABLE'])
			CPU1tbl = BashADBcat(EXYNOS7['CPU1_FREQ_TABLE'])
			GPUtbl  = BashADBcat(EXYNOS7['GPU_FREQ_TABLE'])

			# find only numbers
			CPU0tbl = re.findall('\d\d\d+', CPU0tbl)
			CPU1tbl = re.findall('\d\d\d+', CPU1tbl)
			GPUtbl  = re.findall('\d\d\d+', GPUtbl)

			self.CPU0_Min = BashADBcat(EXYNOS7['CPU0_MIN'])[:-2]
			self.CPU0_Max = BashADBcat(EXYNOS7['CPU0_MAX'])[:-2]
			self.CPU1_Min = BashADBcat(EXYNOS7['CPU1_MIN'])[:-2]
			self.CPU1_Max = BashADBcat(EXYNOS7['CPU1_MAX'])[:-2]
			self.GPU_Min  = BashADBcat(EXYNOS7['GPU_MIN'])[:-2]
			self.GPU_Max  = BashADBcat(EXYNOS7['GPU_MAX'])[:-2]

			# display DVFS table
			DisplayMsg('\n========= DVFS table =======')
			DisplayMsg('CPU0 DVFS table :\n%s\n' % CPU0tbl)
			DisplayMsg('CPU1 DVFS table :\n%s\n' % CPU1tbl)
			DisplayMsg('GPU DVFS table :\n%s\n' % GPUtbl)
			DisplayMsg('============================')
			DisplayMsg('CPU0 Min= %s, Max= %s' % (self.CPU0_Min, self.CPU0_Max) )
			DisplayMsg('CPU1 Min= %s, Max= %s' % (self.CPU1_Min, self.CPU1_Max) )
			DisplayMsg('GPU Min= %s, Max= %s' % (self.GPU_Min, self.GPU_Max) )
			DisplayMsg('============================')


		elif (DEVICE_CHIP == 'universal3475'):	#J2
			CPUtbl = BashADBcat(EXYNOS3['CPU_FREQ_TABLE'])
			GPUtbl = BashADBcat(EXYNOS3['GPU_FREQ_TABLE'])

			# find only numbers
			CPUtbl  = re.findall('\d\d\d+', CPUtbl)
			GPUtbl  = re.findall('\d\d\d+', GPUtbl)

			self.CPU_Min  = BashADBcat(EXYNOS3['CPU_MIN'])[:-2]
			self.CPU_Max  = BashADBcat(EXYNOS3['CPU_MAX'])[:-2]
			self.GPU_Min  = BashADBcat(EXYNOS3['GPU_MIN'])[:-2]
			self.GPU_Max  = BashADBcat(EXYNOS3['GPU_MAX'])[:-2]

			# display DVFS table
			DisplayMsg('\n========= DVFS table =======')
			DisplayMsg('CPU DVFS table : %s' % CPUtbl)
			DisplayMsg('GPU DVFS table : %s' % GPUtbl)
			DisplayMsg('============================')
			DisplayMsg('CPU Min= %s, Max= %s' % (self.CPU_Min, self.CPU_Max) )
			DisplayMsg('GPU Min= %s, Max= %s' % (self.GPU_Min, self.GPU_Max) )
			DisplayMsg('============================')
		else:
			QMessageBox.critical(MainWindow, 'Device', "Device is not supported", QMessageBox.Ok )

	# Detect attached devices and choose one
	# Find the device information for chosen one
	def ActionConnect(self):		
		ret = Detect_Device()
		if(ret == True):
			Device_Info(self.listWidget)
			self.DVFS_Table()
	
	# Copy Benchmark and Event files to the device
	def ActionInstall2Device(self):
		Copy_Files_To_Device(self.progressBar)

	def ActionOpenConfigFile(self):
		global TASK_LIST
		Filename = QFileDialog.getOpenFileName(self, 'Open File', './',  "Config (*.cfg)")
		DisplayMsg('Loading Config File\n%s' % Filename)
		TASK_LIST = Load_Config(self, Filename)
		# Add to tableWidget
		size_of_list = len(TASK_LIST)
		self.tableWidget.setRowCount(size_of_list)
		index = 0
		for element in TASK_LIST:
			PACKAGE, ACTIVITY, TASK, FILE = element
			self.tableWidget.setItem(index, 0, QtGui.QTableWidgetItem(PACKAGE) )
			self.tableWidget.setItem(index, 1, QtGui.QTableWidgetItem(ACTIVITY) )
			self.tableWidget.setItem(index, 2, QtGui.QTableWidgetItem(TASK) )
			self.tableWidget.setItem(index, 3, QtGui.QTableWidgetItem(FILE) )
			index += 1		
		# resize column 
		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.resizeRowsToContents()
		self.tableWidget.selectRow(0)
		FILENAMES['FILE_CONFIG_CFG'] = str(Filename)

	def ActionSystrace(self):
		select, ok = QtGui.QInputDialog.getText(MainWindow, 'Systrace', 'Enter duration of systrace in seconds') 
		Duration = int (select)
		filename = QFileDialog.getSaveFileName(self, 'Save File', './',  "html (*.html)")
		filename += '.html'
		Systrace(Duration, filename)

	def ActionSystraceEvent(self):
		filename = 'event.html'
		print(filename)

		Systrace(5, filename)
		system(ADB + 'shell /sdcard/event_replay')		
		subprocess.call('chromium-browser %s &', filename, shell=True)

	def ActionOpenSystraceFile(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File', './',  "html (*.html)")
		subprocess.call('chromium-browser %s &' % filename, shell=True)

	def ActionCaptureScreen(self):
		system(ADB + 'shell screencap -p /sdcard/screen.png')
		filename = QFileDialog.getSaveFileName(self, 'Save File', './',  "png (*.png)")
		system(ADB + 'pull /sdcard/screen.png ' + str(filename) + '.png')
		system(ADB + 'shell rm /sdcard/screen.png')
	
	def ActionPerformanceMode(self):
		system(ADB + 'remount > NULL')
		system(ADB + 'shell su -c setenforce 0')
		
		if(DEVICE_CHIP == 'universal7420'):		#N5
			# cpu
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq\"' % (int(self.Little_Max) * 1000) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq\"' % (int(self.Little_Max) * 1000) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq\"' % (int(self.Big_Max) * 1000) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq\"' % (int(self.Big_Max) * 1000) )

			# dvfs_min
			system(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_min_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_min_lock\"' % (int(self.GPU_Max)) )
			system(ADB + 'shell cat /sys/devices/14ac0000.mali/dvfs_min_lock' )

			# dvfs_max
			system(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )			
			system(ADB + 'shell cat /sys/devices/14ac0000.mali/dvfs_max_lock' )
			
			# Check CPU & GPU clocks
			gpu_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/14ac0000.mali/dvfs_max_lock", shell=True))
			gpu_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/14ac0000.mali/dvfs_min_lock", shell=True))
			cpu0_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq", shell=True))
			cpu0_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq", shell=True))			
			cpu1_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq", shell=True))
			cpu1_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq", shell=True))
			
			DisplayMsg('\n======= Performance Mode =====')
			DisplayMsg('Little Min: %s, Max: %s' % (cpu0_min, cpu0_max) )
			DisplayMsg('Big Min: %s, Max: %s' % (cpu1_min, cpu1_max) )
			DisplayMsg('GPU Min: %s, Max: %s' % (gpu_min, gpu_max) )
			DisplayMsg('============================')


		elif (DEVICE_CHIP == 'universal3475'):	#J2
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/cpufreq_min_limit\"' % (int(self.Little_Max) * 1000) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/cpufreq_max_limit\"' % (int(self.Little_Max) * 1000) )

			# dvfs_min
			system(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_min_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_min_lock\"' % (int(self.GPU_Max)) )
			system(ADB + 'shell cat /sys/devices/11400000.mali/dvfs_min_lock' )

			# dvfs_max
			system(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )			
			system(ADB + 'shell cat /sys/devices/11400000.mali/dvfs_max_lock' )
			
			# Check CPU & GPU clocks
			gpu_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/11400000.mali/dvfs_max_lock", shell=True))
			gpu_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/11400000.mali/dvfs_min_lock", shell=True))
			cpu0_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/cpufreq/cpufreq_min_limit", shell=True))
			cpu0_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/cpufreq/cpufreq_max_limit", shell=True))
			
			DisplayMsg('\n======= Performance Mode =====')
			DisplayMsg('CPU Mi: %s, Max: %s' % (cpu0_min, cpu0_max) )
			DisplayMsg('GPU Min: %s, Max: %s' % (gpu_min, gpu_max) )
			DisplayMsg('============================')

		else:
			QMessageBox.critical(MainWindow, 'Device', "Device is not supported", QMessageBox.Ok )
			return;			

	def ActionNormalMode(self):
		system(ADB + 'remount > NULL')
		system(ADB + 'shell su -c setenforce 0')


		if(DEVICE_CHIP == 'universal7420'):		#N5
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq\"' % (int(self.Little_Min) * 1000 ) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq\"' % (int(self.Little_Max) * 1000 ) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq\"' % (int(self.Big_Min) * 1000 ) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq\"' % (int(self.Big_Max) * 1000) )

			# dvfs_min
			system(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_min_lock\"' % (int(self.GPU_Min)) )
			print(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_min_lock\"' % (int(self.GPU_Min)) )
			system(ADB + 'shell cat /sys/devices/14ac0000.mali/dvfs_min_lock' )

			# dvfs_max
			system(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/14ac0000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )			
			system(ADB + 'shell cat /sys/devices/14ac0000.mali/dvfs_max_lock' )

			# Check CPU & GPU clocks
			gpu_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/14ac0000.mali/dvfs_max_lock", shell=True))
			gpu_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/14ac0000.mali/dvfs_min_lock", shell=True))
			cpu0_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_min_freq", shell=True))
			cpu0_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster0_max_freq", shell=True))			
			cpu1_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_min_freq", shell=True))
			cpu1_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/mp-cpufreq/cluster1_max_freq", shell=True))
			
			DisplayMsg('\n========== Normal Mode =======')
			DisplayMsg('Little Min: %s, Max: %s' % (cpu0_min, cpu0_max) )
			DisplayMsg('Big Min: %s, Max: %s' % (cpu1_min, cpu1_max) )
			DisplayMsg('GPU Min: %s, Max: %s' % (gpu_min, gpu_max) )
			DisplayMsg('============================')

		elif (DEVICE_CHIP == 'universal3475'):	#J2
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/cpufreq_min_limit\"' % (int(self.Little_Min) * 1000) )
			system(ADB + 'shell \"echo %d > /sys/devices/system/cpu/cpufreq/cpufreq_max_limit\"' % (int(self.Little_Max) * 1000) )
			

			# dvfs_min
			system(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_min_lock\"' % (int(self.GPU_Min)) )
			print(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_min_lock\"' % (int(self.GPU_Min)) )
			system(ADB + 'shell cat /sys/devices/11400000.mali/dvfs_min_lock' )

			# dvfs_max
			system(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )
			print(ADB + 'shell \"echo %d > /sys/devices/11400000.mali/dvfs_max_lock\"' % (int(self.GPU_Max)) )			
			system(ADB + 'shell cat /sys/devices/11400000.mali/dvfs_max_lock' )
			

			# Check CPU & GPU clocks
			gpu_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/11400000.mali/dvfs_max_lock", shell=True))
			gpu_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/11400000.mali/dvfs_min_lock", shell=True))
			cpu0_min = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/cpufreq/cpufreq_min_limit", shell=True))
			cpu0_max = int(subprocess.check_output(ADB + "shell cat " + "/sys/devices/system/cpu/cpufreq/cpufreq/cpufreq_max_limit", shell=True))
			
			DisplayMsg('\n========== Normal Mode =======')
			DisplayMsg('CPU Mi: %s, Max: %s' % (cpu0_min, cpu0_max) )
			DisplayMsg('GPU Min: %s, Max: %s' % (gpu_min, gpu_max) )
			DisplayMsg('============================')

		else:
			print("error")

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

	def StartButton(self):
		Run(self.tableWidget, self.progressBar)
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = Main()
	
	logging.basicConfig(level=logging.DEBUG)		# filename=('%s' % File_Log),
	logging.info("[%s] Start Logging " % LogTime() )

	main.show()
	sys.exit(app.exec_())