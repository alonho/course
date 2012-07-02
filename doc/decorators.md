
# Decorators

* apply a specific policy or behavior to several functions
* aids in preventing code duplication
* sometimes misused

## Examples

	!python
	# raises an exception if the user is not logged in
	@login_required
	def change_password():
		pass
		
	# displays a warning when used for the first time
	@deprecated
	def func():
	    pass
		
	# python can be type safe!
	@typecheck(int, int)
	def add(x, y):
	    pass

---

## Syntax

	!python
	@decorator
	def func():
		pass
	
Equivalent to:
	
	!python
	def func():
	    pass
	func = decorator(func)

Definition: 

**A decorator is a callable the receives a function and returns a callable**

Truth is, a decorator may return anything, but returning something other than a callable usually doesn't make sense.

---

## The debug decorator

A decorator that prints each time the function is called.

	!python
	
	def debug(func):
		def decorated(*a, **k):
			print "calling", func.__name__
			return func(*a, **k)
		return decorated
		
	@debug
	def foo():
	    pass
		
	>>> foo()
	calling foo

---

## Exercise 1 - a better debug decorator

This debug decorator also prints arguments, exceptions and return values.

Can you implement it using the information you see here?

	!python
	@debug
	def div0(n):
		return n / 0

	@debug
	def div2(n):
		return n / 2

    >>> div2(10)
    div2 got  (10,) {}
    returned: 5
	
    >>> div0(10)
    div0 got (10,) {}
	raised: integer division or modulo by zero
	Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero

---

---

## Execise 1 - solution

	!python
	def debug(func):
		def new_func(*a, **k):
			print "{} got ".format(func.__name__), a, k
			try:
				ret = func(*a, **k)
			except Exception as e:
				print "raised: {}".format(e)
				raise
			else:
				print "returned: {}".format(ret)
				return ret
		return new_func

---

## Decorators as classes

Useful when a function needs to save state

	!python
	class InvocationCounter(object):
		
		def __init__(self, func):
		    self._func = func
			self.count = 0
			
		def __call__(self, *a, **k):
		    self.count += 1
			return self._func(*a, **k)

	@InvocationCounter
	def foo():
		pass

	>>> foo()
	>>> foo()
	>>> foo.count
	2
	
---

## Decorator factories

A function that generates a decorator

	!python
	def ignore_exceptions(exception_types, default):
		def decorator(func):
			def decorated(*args, **kwargs):
				try:
					return func(*args, **kwargs)
				except Exception as e:
					if type(e) not in exception_types:
						raise
					return default
			return decorated
		return decorator
		
	@ignore_exceptions([ZeroDivisionError], 0)
	def safediv(x, y):
		return x / y
		
    >>> safediv(3, 0)
	0

---

## Exercise 2 - type checker

Adding some type safety 

	!python
	@typesafe(int, int)
	def add(x, y):
		return x + y
	
	>>> add(5, "bla")
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    TypeError: invalid type for argument y. expected int, got str

---

## Class decorator

	!python

	@decorate_methods(debug)
	class Calculator(object):
		def add(self, x, y):
			return x + y
		def sub(self, x, y):
			return x - y

Note: methods in child classes won't be decorated (metaclasses can solve that).

---

## gotcha #1

Decorators usually replace a function with two nested ones and should be avoided where cpu is the bottleneck.

---

## gotcha #2

Don't decorate a function with a function that gets a different number of arguments.

	!python
	
    # The retry decorator returns a function that gets a 'retries' argument indicating
    # how many times to invoke the decorated function in case an exception occured.
	
	@retry
	def foo():
	    pass
		
    >>> foo(retries=3) # how can a fresh coder know this argument exists?

---

## gotcha #3

Always use `functools.wraps` in order to preserve the function's name and documentation.

Without `functools.wraps`:
  
	!python
	
	def debug(func):
		def decorated(*a, **k):
			print "calling", func.__name__
			return func(*a, **k)
		return decorated

	@debug
	def foo():
		"""
		foo does this and that.
		"""
	    pass

	>>> foo.__name__
	decorated
	>>> foo.__doc__
	None

---

With `functools.wraps`:

	!python
	from functools import wraps
	
	def debug(func):
		@wraps(func)
		def decorated(*a, **k):
			print "calling", func.__name__
			return func(*a, **k)
		return decorated

	@debug
	def foo():
		"""
		foo does this and that.
		"""
	    pass

	>>> foo.__name__
	foo
	>>> foo.__doc__
	foo does this and that.
