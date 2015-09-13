import time
import subprocess
import re


class ShowFreq():
	def __init__(self, milliseconds):
		self.proc = subprocess.Popen(['adb', 'shell', '/sdcard/showfreq', '%s' % milliseconds ], stdout=subprocess.PIPE)

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




if __name__ == '__main__':
	#display out put line by line
	showfreq = ShowFreq(1000)
		
	while True:
		values = showfreq.GetValues()
		if values != None:
			print values						
		#	showfreq.Terminate()
		