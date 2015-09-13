import time
import subprocess
import re


class ShowFreq():
	def __init__(self, milliseconds):
		self.proc = subprocess.Popen(['adb', 'shell', '/sdcard/showfreq', '%s' % milliseconds ], stdout=subprocess.PIPE)

	def GetValues(self):
		line = self.proc.stdout.readline()
		return line

	def Terminate(self):
		self.proc.kill()

if __name__ == '__main__':
	#display out put line by line
	showfreq = ShowFreq(1000)
	line = showfreq.GetValues()
	line = showfreq.GetValues()
	string = line.rstrip()
	str1 = re.sub('[^0-9\.\s-]','',string)
	str2 = re.sub('-\s','',str1)
	values = re.split('\s+',str2)
	del values[19]
	del values[21]
	values = [float(x) for x in values]

	#line = '1.00 [ 900  900  900  900 | 1800 1800 1800 1800] [MAX: 1500 MIN:  400 | MAX: 1800 MIN:  800] [GPU-Freq: 266 ( 22)] 
	#[DVFS MAX: 420 (node) MIN:  -1 (   )] [DDR: 1264 BUS:  200] [CPU0:  66 CPU1:  65 GPU:  62] [APT: 52.3 PST: 48.2] [FPS:  0]'
	print line
	#str1 = 1.00  900  900  900  900  1800 1800 1800 1800  1500   400   1800   800 - 266  22   420    -1      1264   200 0  66 1  65   62  52.3  48.2   0
	print str1
	#str2 = 1.00  900  900  900  900  1800 1800 1800 1800  1500   400   1800   800 266  22   420    -1      1264   200 0  66 1  65   62  52.3  48.2   0
	print str2
	#values [1.0, 900.0, 900.0, 900.0, 900.0, 1800.0, 1800.0, 1800.0, 1800.0, 1500.0, 400.0, 1800.0, 800.0, 266.0, 22.0, 420.0, -1.0, 1264.0, 200.0, 0.0, 66.0, 1.0, 65.0, 62.0, 52.3, 48.2, 0.0]
	print values

	print ('TIME = %.2f' % values[0])
	print ('CPU0 = %.f' % values[1])
	print ('CPU1 = %.f' % values[2])
	print ('CPU2 = %.f' % values[3])
	print ('CPU3 = %.f' % values[4])
	print ('CPU4 = %.f' % values[5])
	print ('CPU5 = %.f' % values[6])
	print ('CPU6 = %.f' % values[7])
	print ('CPU7 = %.f' % values[8])
	print ('BIG_MAX_CLOCK = %.f' % values[9])
	print ('BIG_MIN_CLOCK = %.f' % values[10])
	print ('LITTLE_MAX_CLOCK = %.f' % values[11])
	print ('LITTLE_MIN_CLOCK = %.f' % values[12])
	
	print ('GPU_FREQ = %.f' % values[13])
	print ('GPU_UTIL = %.f' % values[14])
	print ('DVFS_MAX = %.f' % values[15])
	print ('DVFS_MIN = %.f' % values[16])
	print ('DDR_CLOCK = %.f' % values[17])
	print ('BUS_CLOCK = %.f' % values[18])

	print ('CPU0_TEMP = %.f' % values[19])
	print ('CPU1_TEMP = %.f' % values[20])
	print ('GPU_TEMP = %.f' % values[21])
	print ('APT_TEMP = %.1f' % values[22])
	print ('PST_TEMP = %.1f' % values[23])
	print ('FPS = %.1f' % values[24])
	showfreq.Terminate()	
	
