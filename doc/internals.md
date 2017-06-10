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

Static variables and methods are also stored in a dict:

	!python
	>>> class Foo(object):
	...     def bar(self):
	...         pass
	>>> print Foo.bar
	<unbound method Foo.bar>
	>>> print Foo.__dict__['bar']
	<unbound method Foo.bar>

---

Every instance has a dict:

	!python
	>>> foo = Foo()
	>>> foo.__dict__
	{} # the methods are kept at the class's __dict__
	>>> foo.__dict__['a'] = 100
	>>> foo.a
	100

Even module attribute are stored in a dict:

	!python
	>>> import sys
	>>> sys.__dict__.keys()
	['setrecursionlimit', 'dont_write_bytecode', 'getrefcount', ...]

And the module cache (makes sure modules are loaded once) is also a dict:

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

## Dynamic access to attributes

Use builtin `getattr` and `setattr`:

    !python
    class Foo(object):
        pass

    >>> f = Foo()
    >>> setattr(f, 'member', 1.23)
    >>> getattr(f, 'member')
    1.23
    >>> f.member
    1.23

---

## Hooking attribute access

The `__getattr__` method is called for non-existent members.

    !python
    class Foo(object):
        def __getattr__(self, name):
            print 'getting {}'.format(name)
            return len(name)

    >>> f = Foo()
    >>> f.x
    getting x
    1
    >>> f.helloworld
    getting helloworld
    10
    >>> f.blah = 0.1
    >>> f.blah
    0.1

---

## Hooking attribute access

The `__getattribute__` method is called for any members.

    !python
    class Foo(object):
        def __getattribute__(self, name):
            print 'getting {}'.format(name)
            return len(name)

    >>> f = Foo()
    >>> f.x
    getting x
    1
    >>> f.helloworld
    getting helloworld
    10
    >>> f.blah = 0.1
    >>> f.blah
    getting blah
    4

---

## Hooking attribute access

The `__setattr__` method is called when setting all members.

    !python
    class Foo(object):
        def __setattr__(self, name, value):
            print 'setting {} = {}'.format(name, value)

    >>> f = Foo()
    >>> f.x = 1
    setting x = 1
    >>> f.bar = 1.23
    setting bar = 1.23
    >>> f.x = 1
    setting x = 1

---

## Exercise 1 - case insensitive object

	!python
	>>> obj = CaseInsensitive()
    >>> a.x = 1
    >>> a.x
    1
    >>> a.X
    1
    >>> a.XYZ = 2
    >>> a.xyz
    2
    >>> a.__dict__
    {'x': 1, 'xyz': 2}

---

## Exercise 1 - solution

	!python
    class CaseInsensitive(object):
        def __setattr__(self, name, value):
            return object.__setattr__(self, name.lower(), value)
        def __getattribute__(self, name):
            return object.__getattribute__(self, name.lower())

Note that we are using `object` because looking at `self.__dict__`
will trigger an infinite recursion of `__getattr__/__setattr__`.

---

The `__getattr__` method can be overriden in a similar manner, except that it's called only if the attribute doesn't exist in the object's `__dict__`.

The attribute lookup order is as follows:

1. `__getattribute__`
2. `__dict__`
3. `__getattr__`

---

## Descriptors

Descriptors allow customizing attribute getting, setting and deletion.

Example of dynamic attribute lookup:

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
it's useful for calculated values and readonly attributes.

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
	>>> A.a  # class attr translates to:
             # A.__dict__['a'].__get__(None, A)
	None <class '__main__.const'>
	100
	>>> A().a # instance attr translates to:
              # type(obj).__dict__['a'].__get__(obj, type(obj))
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
                fmt = "Expected {}, got {} ({})"
				raise TypeError(fmt.format(self._cls, type(value), value))
			self._value = value

---

## Inheritence, super and the MRO

Python supports multiple inheritence. Because all objects inherit from `object`,
all inheritence trees look like diamonds.
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

---

## Why to use `super`?

`super` is recommended for several reasons:

1. if `Person` no longer inherits from object but from `Mammal`, a single line changes.
2. `super` enables calling all constructors when used in the context of multiple inheritence. next slide shows how.

---

## How to use `super`?

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

---

## How to use `super`?

    !python
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

## How `super` works?

**MRO** - method resolution order

In a diamond inheritence model, where all constructors need to be called we need to find a way to order them.
Python uses an algorithm called `C3`.

The essence of the algorithm:

1. children are initialized before parents.
2. siblings are initialized left to right.

NOTE: Any class along the chain can prevent a correct initialization sequence if it doesn't call `super` or calls it with the wrong argument.

---

## super and constructor arguments

The best strategy is to assume you don't know what the method resolution order is and pass keyword arguments.

Every constructor will consume the arguments it explicitly defined and pass the rest to the parent/sibling using `*args` and `**kwargs`.

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

The list of search paths can be modified from within python:

	!python
    >>> import sys
	>>> sys.path.append('path')

---

After looking at the PYTHONPATH, python looks in the package installation path:

	!python
	>>> import site
	>>> site.getsitepackages()
	['/usr/local/lib/python2.7/dist-packages',
     '/usr/lib/python2.7/dist-packages']

Finally python looks at the stdlib directory, On Linux, it's
`/usr/lib/python2.7/`

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

## Mutability

An immutable object cannot be modified after it is created.
This is in contrast to a mutable object, which can be modified after it is created.

Examples of immutable objects: ints, floats, strings, tuples etc'.

Examples of mutable objects: lists, dicts, objects etc'.

	!python
	>>> string = "foo"
	>>> copy = string
	>>> copy is string
	True
	>>> string += "bar" # creates a new string
	>>> copy is string
	False
	>>> string
	foobar
	>>> copy
	foo
	>>> l = [1, 2, 3]
	>>> l2 = l # creates a reference to the same list
	>>> l.append(4)
	>>> l2
	[1, 2, 3, 4]

---

## Dictionaries and `__hash__`

Dictionaries, or more generally hash maps, identify keys using a hash function.
The hash function maps a value (lets say, a string) to a number. The same string will always be mapped to the same number, Hence, consistent hashing.

A dictionary calculates the hash of objects by calling `__hash__`.

Dictionary keys must be immutable. Mutable objects can't generate a consistent hash, therefore, their `__hash__` attribute is set to `None`.

If a custom object has immutable qualities (a user id that will never change), It can implement `__hash__`:

	!python
	class User(object):

	    def __init__(self, id, name):
			self.id = id
			self.name = name
		def __eq__(self, other):
		    return self.id == other.id
		def __hash__(self):
			return self.id

That way we can build dictionaries with users as keys, or sets of users.

---

## Immutable data structures

`frozenset` is an immutable `set`.

The brownie library has an `ImmutableDict` implementation.

`tuples` can be used as immutable `lists`.

---

## The stack

The python stack is composed of frames.

Each thread has it's own stack.

The stack frames points to the code object, local variables, the previous stack frame and various python internal information.

	!python
	>>> def print_stack():
	...     frame = sys._getframe(0) # first frame
	...     print frame
	...     print frame.f_code # the code object
	...     print frame.f_locals # locals()
	...     print frame.f_back  # previous frame
	>>> print_stack()
	<frame object at 0x100379df0>
	<code object print_stack at 0x100437830, file "<stdin>", line 1>
	{'frame': <frame object at 0x100379df0>} # locals()
	<frame object at 0x100379c40> # previous frame

---

## Printing the stack

	!python
	import traceback
	>>> def foo():
	...     traceback.print_stack()
	>>> foo()
	  File "<stdin>", line 1, in <module>
   	  File "<stdin>", line 2, in foo

Useful for exception analysis:

	!python
	>>> def foo():
	...     1 / 0
	>>> try:
	...     foo()
	... except:
	...     traceback.print_exc()
	Traceback (most recent call last):
	  File "<stdin>", line 2, in <module>
      File "<stdin>", line 2, in foo
	ZeroDivisionError: integer division or modulo by zero

NOTE: if you're using `logging`, use `logger.exception` to log a message with a traceback.

---

## Functions and methods

Python functions are simple function objects.

	!python
	def func():
		pass

	>>> print func
	<function __main__.func>

Python methods are a bit different.

	!python
	class A(object):
		def foo(self):
			pass

	>>> print A().foo
	<bound method A.foo of <__main__.A object at 0x101e4aed0>>

---

There's a reason for that:

	!python
	>>> a = A()
	>>> foo = a.foo
	>>> foo() # where is 'self'?
	>>> print foo.im_func
	<function __main__.foo>
	>>> print foo.im_self
	<__main__.A at 0x101e4afd0>

So calling bound methods:

	!python
	>>> a.foo()

Is implemented roughly like this:

	!python
	>>> a.foo.im_func(a.foo.im_self)

---

Unbound methods are methods of the class:

	!python
	>>> A.foo
	<unbound method A.foo>
	>>> print A.foo.im_self # no instance
	None
	>>> print A.foo.im_class
	<class __main__.A>

One of the reasons the `im_class` attribute exists is this:

	!python
	>>> a = A()
	>>> A.foo(a)
	>>> A.foo(10) # type of self is compared against im_class
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    TypeError: unbound method foo() must be called with A instance
	as first argument (got int instance instead)

---

## `__slots__`

`__slots__` let us avoid a dictionary allocation per instance.
by defining a list of member names, a small and fixed amount of memory per object is allocated.

Without `__slots__`:

	!python
	>>> import sys
	>>> class A(object):
	...     pass
	>>> sys.getsizeof(A())
    64
	>>> sys.getsizeof(A.__dict__)
	280

---

## `__slots__`

With `__slots__`:

	!python
	>>> class A(object):
	...     __slots__ = ()
	>>> sys.getsizeof(A())
	16
	>>> A().__dict__
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    AttributeError: 'A' object has no attribute '__dict__'

---

No attributes can be added to classes with `__slots__`:

	!python
	>>> class A(object):
	...     __slots__ = ('a', 'b')
	>>> a = A()
	>>> a.a = 10
	>>> a.c = 100
	Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'A' object has no attribute 'c'

Note1: `__slots__` and inheritence - `__dict__` allocation will be prevented only if all classes in the inheritence tree define `__slots__`.

Note2: `__slots__` is implemented using descriptors!

---

## Function default arguments

Avoid this:

	!python
	def f(x=[]):
	    x.append(1)
		print x
	>>> f()
	[1]
	>>> f()
	[1, 1]
	>>> f.func_defaults # these objects are saved in the function object!
	([1, 1],)

---

## Function default arguments

Do this:

	!python
	def f(x=None):
		if x is None:
			x = []
		x.append(1)
		print x
	>>> f()
	[1]
	>>> f()
	[1]

---

## casting to bool

Avoid this:

	!python
	def foo(string=None):
	   if string: # what if an empty string is valid?
	       ...

Do this:

	!python
	if x is None:
		...
	if x == '':
		...

---

## nested scopes - closures

Nested scopes allow functions to access variables defined in enclosing scopes.

	!python
	>>> def addx(x):
	...	    def add(y):
	...         return x + y
	... 	return add
	>>> add5 = addx(5)
	>>> print add5(3)
	8

How does it work?

	!python
	>>> add5.func_closure
	(<cell at 0x10ccc1360: int object at 0x7fea11413110>,)
	>>> cell = _[0] # cell is a reference to a variable in an upper scope
	>>> cell.cell_contents
	5

---

## When in doubt...

    >>> import this
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
