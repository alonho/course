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

---

## Inheritence, super and the MRO

Python supports multiple inheritence. Because all objects inherit from `object`, all inheritence trees look like diamonds.

There are two ways of calling parent methods. the explicit:

	!python
	class Person(object):
		def __init__(self, name):
			object.__init__(self)
			self._name = name

And using super:

	!python
	class Person(object):	
		def __init__(self, name):
			super(Person, self).__init__()
			self._name = name

`super` is recommended for several reasons: 

1. if `Person` no longer inherits from object but from `Mammal`, a single line changes.
2. `super` enables calling all constructors when used in the context of multiple inheritence. next slide will show how.

---

## How to user super

	!python
	class Person(object):
		def __init__(self):
			print "Person"
	class Student(Person):
		def __init__(self):
			super(Student, self).__init__()
			print "Student"
	class Teacher(Person):
		def __init__(self):
			super(Teacher, self).__init__()
			print "Teacher"
	class TeachingStudent(Student, Teacher):
		def __init__(self):
			super(TeachingStudent, self).__init__()
			print "TeachingStudent"
			
	>>> t = TeachingStudent()
	Person
	Teacher
	Student
	TeachingStudent
	>>> TeachingStudent.__mro__
	(__main__.TeachingStudent,
	 __main__.Student,
     __main__.Teacher,
	 __main__.Person,
	 object)

---

## How super works

### MRO - method resolution order

In a diamond inheritence model, where all constructors need to be called we need to find a way to order all constructors.
Python uses a common algorithm called `C3`.

A simplification of the algorithm:

1. children are initialized before parents.
2. siblings are initialized left to right.

NOTE: Any class along the chain can prevent a correct initialization sequence if it doesn't call `super`.

---

## super and constructor arguments

The best strategy is to assume you don't know what the method resolution is and pass keyword arguments.

Every constructor will consume the arguments it explicitly defined and pass the rest to the parent/sibling.

	!python
	class Person(object):
		def __init__(self, age):
			self.age = age

	class Student(Person):
		def __init__(self, semester, *args, **kwargs):
			super(Student, self).__init__(*args, **kwargs)
			self.semester = semester
	
	class Teacher(Person):
		def __init__(self, profession, *args, **kwargs):
			super(Teacher, self).__init__(*args, **kwargs)
			self.profession = profession

	class TeachingStudent(Student, Teacher):
		def __init__(self, *args, **kwargs):
			super(TeachingStudent, self).__init__(*args, **kwargs)

	>>> TeachingStudent(age=100, profession="math", semester=2)

---

## The import mechanism

The import statement:

	!python
	>>> import os

Same as:

	!python
	>>> __import__('os')
	
The import process searches for modules in directories found in the PYTHONPATH environment variable.

	!bash
	export PYTHONPATH=/projects/proj:/home/alon/utils

The list of search paths can be modified from python:

	!python
    >>> import sys
	>>> sys.path.append('path')
	
---

After looking at the PYTHONPATH, python looks in the package installation path:
	
	!python
	>>> import site
	>>> site.getsitepackages()
	['/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python',
     '/Library/Python/2.7/site-packages']
	 
Finally python looks at the stdlib directory, In my case its: /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7

After a module has been found and compiled it is stored in `sys.modules`. 

Actually, the first step of the import process is looking for the module name in `sys.modules`, making sure each module is compiled and invoked once.

---

## Import hooks

With import hooks the import process can be customized. Examples:

1. Import zipped files (already supported in python).
2. Import files located on the network.
3. Import encrypted files.

for more details, look at `sys.meta_path` and `sys.path_hooks`.

---

## eval and exec

`exec` - execute code:

	!python
	>>> exec("print 10")
	1
	>>> execfile("/tmp/bla.py")

`eval` - evaluate an expression:

	!python
	>>> eval("1 + 1")

NOTE: `eval` and `exec` can be a serious security risk, try to avoid them.

NOTE2: `eval`, `exec` and `execfile` all receive optional `locals` and `globals` arguments. by passing new dictionaries we can run the code in a partially isolated environment. BUT it still doesn't count as safe.

---


---

