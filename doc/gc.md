# Garbage Collection

## Reference Counting

Each object can be referenced by several other objects. Each object has a member indicating what the current ref count is. once the ref count reaches zero, the garbage collector destroys it.

When the garbage collector destroys an object it calls it's `__del__` method.

	!python
	class A(object):
		def __del__(self):
			print "BYE"

	def f():
		a = A() # ref count = 1
		d = {'a': a} # ref count = 2
	    del a # ref count = 1, nothing printed!
        print "ready?"
        del d['a'] # ref count = 0
	>>> f()
	ready?
	BYE

---

## Analyzing references

In the following example we can see two references:

1. A local variable creates a reference from the stack frame.
2. A dictionary references it's values.

	    !python
		>>> import gc
		>>> def f():
		...     l = [1, 2]
		...     d = {'list': l}
		...     print gc.get_referrers(l)
		>>> f()
		[<frame object at 0x7fc4bbc764f0>, {'list': [1, 2]}]


---

## `__del__` is bad - swallows exception

`__del__` swallows exceptions. The reason is that the garbage collector checks reference counts in certain intervals, and when it decides to destroy an object then it can't raise exceptions because any random line of our code may be runnning.

	!python
	>>> class A(object):
	...     def __del__(self):
	...         1 / 0
	... 
	>>> print A()
	Exception ZeroDivisionError: 'integer division or modulo by zero' in 
	<bound method A.__del__ of <__main__.A object at 0x10e9167d0>> ignored
	<__main__.A object at 0x10e9167d0>
	>>> 

---
 
## `__del__` is bad - cyclic references

If the gc identifies cyclic references and the objects implement `__del__` it will never release them. NEVER!

	!python
	class A(object):	
		def __del__(self):
			self.x.release() # who goes first? a or b?
 
	>>> a = A()
    >>> b = A()
	>>> a.x = b
	>>>	b.x = a
	>>>	del a
	>>>	del b
	>>> import gc
	>>> gc.collect()
	>>> gc.garbage # the gc marks object it can't free
	[<__main__.A at 0x101e27510>, <__main__.A at 0x101e27f50>]
	
	
