import logging
import sys

logger = logging.getLogger('root')
#FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
#FORMAT = "[%(asctime)s %(name)s %(levelname) -15s ]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
FORMAT = "[%(asctime)s] [%(levelname)s]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)



import logging
import os.path

def initialize_logger(output_dir):
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# create console handler and set level to info
	ConsoleHandler = logging.StreamHandler(sys.stdout)
	ConsoleHandler.setLevel(logging.ERROR)
	FORMAT = "[%(levelname)s]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
	ConsoleHandler.setFormatter(logging.Formatter(FORMAT))
	logger.addHandler(ConsoleHandler)

	# create debug file handler and set level to debug
	FileHandler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
	FileHandler.setLevel(logging.DEBUG)
	FORMAT = "[%(asctime)s] [%(levelname)s]-[%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s "
	FileHandler.setFormatter(logging.Formatter(FORMAT))
	logger.addHandler(FileHandler)

	# create error file handler and set level to error
	# handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
	# handler.setLevel(logging.ERROR)
	# formatter = logging.Formatter("%(levelname)s - %(message)s")
	# handler.setFormatter(formatter)
	# logger.addHandler(handler)


# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='all.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)



logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")