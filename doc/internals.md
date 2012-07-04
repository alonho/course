# Python Internals

---

## Everything is a dict

Variables, which are names pointing to values are stored in a dict:

	!python
	>>> a = 10
	>>> print a
	10
	>>> print locals()['a']
	10

As well as methods:

	!python
	>>> class Foo(object):
	...     def bar(self):
	...         pass
	>>> print Foo.bar
	<unbound method Foo.bar>
	>>> print Foo.__dict__['bar']
	<unbound method Foo.bar>

---

As well as members:

	!python
	>>> foo = Foo()
	>>> foo.__dict__
	{} # the methods are kept at the class's __dict__
	>>> foo.__dict__['a'] = 100
	>>> foo.a
	100

And even modules:
	
	!python
	>>> import sys
	>>> sys.__dict__.keys()
	['setrecursionlimit', 'dont_write_bytecode', 'getrefcount', ...]
	
And even the module cache (makes sure modules are loaded once):
	
	!python
	>>> sys.modules['sys']
	<module 'sys' (built-in)>

---

## locals and globals

There are two types of dictionaries designated for variable lookup: locals() returns local variables, 
globals() returns global variables.

	!python
	glob = 100
	def global_test():
		return glob # locals() won't contain 'glob' but globals() will
	
	def local_test():
		loc = 100
		return loc

	>>> dis.dis(global_test)
	2           0 LOAD_GLOBAL              0 (glob)
                3 RETURN_VALUE        
			
	>>> dis.dis(local_test)
    2           0 LOAD_CONST               1 (100)
                3 STORE_FAST               0 (loc)

    3           6 LOAD_FAST                0 (loc)
                9 RETURN_VALUE      

---

`dis.dis` is a python disassembler. it prints the bytecode of the functions.

For loading global variables the `LOAD_GLOBAL` bytecode is used.
			
For loading local variables the `LOAD_FAST` bytecode is used.
			
The reason `LOAD_FAST` is called `LOAD_FAST` and not `LOAD_LOCAL` is because local variable access is optimized, 
and therefore, local variable access is faster. 
			
---
			
## The mighty '.'

`__getattribute__` allows customization of the attribute lookup process.

	!python
	class Foo(object):

	    def __getattribute__(self, attr):
			print 'getting {}'.format(attr)
			return 10

	>>> print Foo().a
	getting a
	10

---

## Exercise 1 - case insensitive object

	!python
	>>> obj = CaseInsensitive()
	>>> obj.a = 100
	>>> obj.A
	100

---

## Exercise 1 - solution

	!python
	class A(object):
		def __getattribute__(self, attr):
			try:
				return super(A, self).__getattribute__(attr)
			except AttributeError:
				return super(A, self).__getattribute__(attr.lower())

---

`__getattr__` can be overriden in a similar manner, except that it's called only if the attribute doesn't exist in the object's `__dict__`.

The attribute lookup order is as follows:

1. `__getattribute__`
2. `__dict__`
3. `__getattr__`

---

## Descriptors

Descriptors provide a way to dynamically process attribute getting, setting and deletion.

Example of dynamic getting of an attribute:

	!python
	import math

	class Angle(object):
	
		def __init__(self, degrees):
			self.degrees = degrees
		
		@property
		def radians(self):
			return self.degrees * (math.pi / 180)
		
	>>> a = Angle(180)
	>>> a.radians
	3.141592653589793
	>>> a.radians = 100 # read only attribute!
	Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute

property is a built-in utility decorator that generates descriptor objects.

---

## The descriptor protocol

	!python
	class const(object):
	
		def __init__(self, value):
			self._value = value
	
		def __get__(self, obj, type):
			print obj, type
			return self._value
			
		def __set__(self, obj, value):
			raise AttributeError() # indicates a read only
				
		def __delete__(self, obj):
			# no allocation, nothing to do.
			pass
			
	>>> class A(object):
	...     a = const(100)
	>>> A.a # class attr translates to: A.__dict__['a'].__get__(None, A)
	None <class '__main__.const'>
	100
	>>> A().a # instance attr translates to: type(obj).__dict__['a'].__get__(obj, type(obj))
	<__main__.A object at 0x103449e90> <class '__main__.const'>
	100

---

## Exercise 2 - typesafe

	!python
	class Person(object):
		name = typesafe(str)
		age = typesafe(int)
	
	>>> p = Person()
	>>> p.name = "Alon"
	>>> p.age = "Horev"
	Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: Expected <type 'int'>, got <type 'str'> (Horev)

---

## Exercise 2 - solution

	!python
	class typesafe(object):

	    def __init__(self, cls):
			self._cls = cls
			self._value = None
        
		def __get__(self, obj, type):
			return self._value
				
		def __set__(self, obj, value):
			if not isinstance(value, self._cls):
				raise TypeError("Expected {}, got {} ({})".format(self._cls, type(value), value))
			self._value = value
