# Context Managers

* Great for resource management
* An alternative for destructors (`__del__` is bad!)

Examples:

    !python
    # do this
	with self.lock:
		1 / 0 # even though an exception is raised the lock is released
	
    # don't do this - you might forget to call release
	lock.acquire()
	try:
		...
	finally:
		lock.release()
	
    with file('/tmp/bla', 'w') as f:
		f.write('data')
	    1 / 0 # even though an exception is raised the file is closed
	
	# nesting
	with lock1, lock2:
		...

---

## The context manager protocol

A context manager provides methods for the entrance and exit of a context.

	!python
	>>> with LockContext() as lock:
	... 	print lock.is_locked()
	... print lock.is_locked()
	init
	locking..
	True
	unlocking..
	False

	class LockContext(object):
	    def __init__(self):
			print "init"
			self._lock = Lock()
		def is_locked(self):
			return self._lock.locked()
		def __enter__(self):
			print "locking.."
			self._lock.acquire()
			return self
		def __exit__(self, exc_type, exc_val, exc_tb):
			print "unlocking.."
			self._lock.release()

---

## The context manager protocol

A Context manager can swallow exceptions (prevent propagation) by returning `True` in its `__exit__` method. 

	!python
	>>> with NoExceptions():
	...     1 / 0
	Ha Ha
	>>>

	class NoExceptions(object):
	
		def __enter__(self):
			pass
	
		def __exit__(self, exc_type, exc_val, exc_tb):
			print "Ha Ha"
			return True # indicates exception has been handled and shouldn't propagate

---

## contextlib

Context manager utilities can be found in the stdlib's `contextlib` module.

The `contextmanager` decorator turns a generator function into an object.

The generator should yield once, that way the first iteration is the `__enter__`, and the second is the `__exit__`.

The exception information is passed by simply throwing the exception into the generator.

	!python
	@contextmanager
	def locked(lock):
		lock.acquire()
		try:
			yield
		finally:
			lock.release()
		
	>>> lock = Lock()
	>>> with locked(lock):
	...     pass

---

## Exercise 1 - NoExceptions

	!python
	>>> with NoExceptions([ZeroDivisionError]):
	...	    1 / 0
	ignoring exception: integer division or modulo by zero
	>>>
	
---

## Exercise 1 - solution

	!python
	@contextmanager
	def no_exceptions(exception_types):
		try:
			yield
		except Exception as e:
			if type(e) not in exception_types:
				raise
			else:
				print "ignoring exception :{}".format(e)

---

## Exercise 2 - timed

	!python
	def benchmark():
		with Timed("list comprehension"):
			[str(i) for i in xrange(100000)]
		with Timed("map"):
	        map(str, xrange(100000))
	
	>>> benchmark()
	list comprehension took 0.0324079990387
    map took 0.0171928405762

---

## Exercise 2 - solution

	!python
	import time
	from contextlib import contextmanager
	
	@contextmanager
	def Timed(obj):
		stime = time.time()
		yield
		print "{} took {}".format(obj, time.time() - stime)

