# Logging

---

## Example

	!python
	>>> import sys, logging
	>>> logger = logging.getLogger(__name__)
	>>> logger.addHandler(logging.StreamHandler(sys.stdout))

	>>> logger.info("dividing")
	>>> try:
	>>>     1 / 0
	>>> except Exception as e:
	>>>     logger.exception("caught {}".format(e))
	caught integer division or modulo by zero
	Traceback (most recent call last):
	  File "<ipython-input-19-dd7b8f0dab6f>", line 2, in <module>
        1/0
	ZeroDivisionError: integer division or modulo by zero

Why isn't the info printed?

---

## Levels

The logger's default minimum level is `warning`.

	!python
	>>> logging._levelNames
	{0: 'NOTSET',
	10: 'DEBUG',
	20: 'INFO',
	30: 'WARNING',
	40: 'ERROR',
	50: 'CRITICAL',
	'NOTSET': 0,
	'DEBUG': 10,
	'INFO': 20,
	'WARN': 30,
	'WARNING': 30,
	'ERROR': 40,
	'CRITICAL': 50}

	>>> logger.info("bla")
	>>> logger.getEffectiveLevel()
	30
	>>> logger.setLevel(logging.DEBUG)
	>>> logger.info("bla")
	BLO

---

## Handlers

## Types

`logging.StreamHandler(sys.stdout)` - directs log messages to a stream.

`logging.FileHandler('log')` - directs log messages to a file.

`logging.handlers.RotatingFileHandler('log', maxBytes=1024, backupCount=10)` - a handler that once a file reaches 1024 bytes in size, moves it and creates a new file. `backupCount` states how many files to keep. files will be named: 'log', 'log.1', 'log.2', etc'. each file will be approx' 1024 bytes long.

`logging.handlers.TimedRotatingFileHandler('log', when='midnight')` - a handler that rotates every midnight. also support `backupCount`. files will be named: 'log', 'log.2012-06-19', 'log.2012-06-20'.

## Handler level

Handlers can also filter records by setting a minimum level:

	!python
	file_handler = FileHandler("log")
	stdout = StreamHandler(sys.stdout)
	file_handler.setLevel(logging.DEBUG) # debug and up to file
	stdout.setLevel(logging.INFO) # info and up to screen

---

## Formatters

The format of log messages can be modified using a `Formatter` object.

	!python
	>>> import logging
	>>> formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
		)
	>>> handler = logging.StreamHandler()  # logs to sys.stderr
	>>> handler.setFormatter(formatter)
	>>> logger = logging.getLogger("my_logger")
	>>> logger.addHandler(handler)
	>>> logger.error("Help")
	2012-07-08 17:33:12,126 - my_logger - ERROR - Help

An example of a verbose format: `%(asctime)s|%(process)d|%(name)s|%(threadName)s|%(levelname)s|%(module)s:%(lineno)s:%(funcName)s|%(message)s`.

---

## Logger inheritence

All loggers inherit from the `root` logger:

	!python
	>>> logging.root
	<logging.RootLogger at 0x10d50b1d0>

Child logger forward log records to parents:

	!python
	>>> logging.root.addHandler(StreamHandler())
	>>> logging.getLogger("foo").error("Help")
	Help
	>>> logging.getLogger("bar").error("Help")
	Help

We can define our own inheritence trees. In order to create a logger named `child` that inherits from a parent named `parent`, we'll name it `parent.child`:

	!python
	>>> parent = logging.getLogger("parent")
	>>> parent.addHandler(StreamHandler())
	>>> child = logging.getLogger("parent.child")
	>>> child.error("Help")
	Help

---

## Preventing inheritence

	!python
	>>> logger = logging.getLogger("parent")
	>>> logger.propagate = False

---

## Recommended logging usage

At each module, use:

	!python
	import logging
	log = logging.getLogger(__name__)

	def foo()
		''' Use module-specific logger. '''
		log.info('doing foo')

At `__main__` entry point, configure handlers and formatters and attach to relevant loggers.

Consider using logging configuration file:

	!python
	import logging.config
	logging.config.fileConfig('logging.config')


---

## LogBook

logging API feels like old-school Java :(

consider using LogBook package for modern Pythonic approach:

	!python
	>>> from logbook import Logger
	>>> log = Logger('Logbook')
	>>> log.info('Hello, World')
	[2010-07-23 16:34] INFO: Logbook: Hello, World

see <http://pythonhosted.org/Logbook/setups.html> for more examples.
