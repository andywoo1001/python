import logging

BLACK     ='\033[30m'
RED       ='\033[31m'
GREEN     ='\033[32m'
ORANGE    ='\033[33m'
BLUE      ='\033[34m'
PURPLE    ='\033[35m'
CYAN      ='\033[36m'
LIGHTGREY ='\033[37m'
DARKGRAY  ='\033[90m'
LIGHTRED  ='\033[91m' # FAIL
LIGHTGREEN='\033[92m' # OK GREEN
YELLOW    ='\033[93m' # WARNING
LIGHTBLUE ='\033[94m' #OK BLUE
PINK      ='\033[95m' #HEADER
LIGHTCYAN ='\033[96m'
RED_BKGND= '\033[1;41m'
ENDC     = '\033[0m'
BOLD     = '\033[1m'a
UNDERLINE= '\033[4m'


LOG_FILE_FORMAT		= '[%(asctime)s] %(levelname)-8s %(filename)s(%(lineno)s)-%(funcName)s() : %(message)s'
LOG_FILE_DATEFMT	= '%Y-%m-%d %H:%M:%S'
LOG_FILE_LEVEL		= logging.DEBUG
LOG_FILE_NAME		= 'temp.log'
LOG_CONSOLE_FORMAT	= DARKGRAY + '%(asctime)s ' + ENDC + \
					  '%(message)s'
LOG_CONSOLE_DATEFMT = '%m-%d %H:%M'
LOG_CONSOLE_LEVEL	= logging.DEBUG



class ColoredFormatter(logging.Formatter):
	def format(self, record):
		color 	= None
		if record.levelno == logging.DEBUG:
			color = LIGHTGREY
		elif record.levelno == logging.INFO:
			color = BOLD+GREEN			
		elif record.levelno == logging.WARN:
			color = YELLOW
		elif record.levelno == logging.ERROR:
			color = RED_BKGND
		elif record.levelno == logging.CRITICAL:
			color = RED_BKGND
	
		record.msg = color + '%-08s' % record.levelname + ENDC + ' ' + \
					'[ ' + LIGHTGREY + record.filename + ':' + ENDC + \
					LIGHTCYAN + str(record.lineno) + LIGHTGREY + ENDC + ' ' +\
					PINK + record.funcName+ '()' + ENDC  + ' ] ' + \
					color + record.msg + ENDC
		return logging.Formatter.format(self, record)


# set up logging to file
logging.basicConfig(level=LOG_FILE_LEVEL, format=LOG_FILE_FORMAT, datefmt=LOG_FILE_DATEFMT, filename=LOG_FILE_NAME, filemode='w')

# define a Handler which writes INFO messages
console = logging.StreamHandler()
console.setLevel(LOG_CONSOLE_LEVEL)
console.setFormatter(ColoredFormatter(LOG_CONSOLE_FORMAT, datefmt=LOG_CONSOLE_DATEFMT))
log = logging.getLogger('LOG')
log.addHandler(console)


def log_test():
	log.debug("debug message")
	log.info("info message")
	log.warn("warn message")
	log.error("error message")
	log.critical("critical message")

if __name__ == '__main__':
	log_test()
	