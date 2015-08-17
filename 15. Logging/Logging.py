import logging
# %(pathname)s Full pathname of the source file where the logging call was issued(if available).
# %(filename)s Filename portion of pathname.
# %(module)s Module (name portion of filename).
# %(funcName)s Name of function containing the logging call.
# %(lineno)d Source line number where the logging call was issued (if available).

logger = logging.getLogger('root')
#FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
#FORMAT = "[%(asctime)s %(name)s %(levelname) -15s ]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
FORMAT = "[%(asctime)s] [%(levelname)s]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

def log_func():
	logger.debug('my fist func message')



log_func()



import logging
logger = logging.getLogger('App Name')
def SetupLogging():
logger.setLevel(logging.DEBUG)
#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#create formatter
# was:%(asctime)s - %(name)s - %(levelname)s: %(message)s" 
formatter = logging.Formatter("%(levelname)s(%(name)s): %(message)s")
#add formatter to ch
ch.setFormatter(formatter)
#add ch to logger
logger.addHandler(ch)
logger.error("Whoops, an error!")
logger.debug ("Doing something boring") 
The formatter options are:

%(name)s            Name of the logger (logging channel)
%(levelno)s         Numeric logging level for the message (DEBUG, INFO,
WARNING, ERROR, CRITICAL)
%(levelname)s       Text logging level for the message ("DEBUG", "INFO",
"WARNING", "ERROR", "CRITICAL")
%(pathname)s        Full pathname of the source file where the logging
call was issued (if available)
%(filename)s        Filename portion of pathname
%(module)s          Module (name portion of filename)
%(lineno)d          Source line number where the logging call was issued
(if available)
%(created)f         Time when the LogRecord was created (time.time()
return value)
%(asctime)s         Textual time when the LogRecord was created
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
relative to the time the logging module was loaded
(typically at application startup time)
%(thread)d          Thread ID (if available)
%(process)d         Process ID (if available)
%(message)s         The result of record.getMessage(), computed just as
the record is emitted
 