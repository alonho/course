# Metaclasses

**Inspired and partially copied from:
<http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python>**

---

## But first - classes

Classes are objects, and can be treated as such:

	!python
	class Foo(object):

		bar = 100 # static attribute - shared by all instances

		def do(self):
			pass

	>>> print Foo
    <class '__main__.Foo'>
	>>> print Foo.bar
	100
	>>> Foo.bar = 200

---

## Creating classes dynamically

Since classes are objects, you can create them on the fly, like any object.

	!python
	def choose_class(name):
		if name == 'foo':
			class Foo(object):
				pass
			return Foo
		else:
			class Bar(object):
				pass
			return Bar

	>>> MyClass = choose_class('foo')
	>>> print MyClass # the function returns a class, not an instance
	<class '__main__.Foo'>
	>>> print MyClass() # you can create an object from this class
	<__main__.Foo object at 0x89c6d4c>

---

## How Python creates a class object?

	!python
	class Foo(object):

		bar = 100

		def do(self):
			pass

Translates to:

	!python
	Foo = type(
		'Foo', # the name of the class (it's __name__ attribute)
        (object,), # it's bases
		{ # the class dictionary, contains functions and static attributes
			'__module__': '__main__',
			'bar': 100,
			'do': <function do at 0x10a9a6a28>
		}
	)


`type` is a metaclass - it creates classes.
Using metaclasses we can alter the class creation process. we can add, remove, change or verify methods and attributes, parent objects and the class name.

---

## Create a metaclass

When writing a class we can add the `__metaclass__` attribute in order to replace the default metaclass (`type`).

	!python
	def implements_str(name, bases, dct):
		assert '__str__' in dct
		print "found __str__"
		return type(name, bases, dct)

	>>> class Foo(object):
	...     __metaclass__ = implements_str
	...     def __str__(self):
    ...         return ''
	found __str__

If the `__metaclass__` attribute is not defined, python will look for it in the parent classes or the module.

---

## Metaclass as a class

A metaclass can be implemented both as a class and as a function. as long as it gets the 3 arguments.

	!python
	class ImplementsStr(type):

		def __new__(cls, name, bases, dct):
			assert '__str__' in dct
			print "found __str__"
			return super(ImplementsStr, cls).__new__(cls, name, bases, dct)
---

## Example - django

Using metaclasses, the django web framework provides a clean object-oriented API to database rows.

	!python
	class Person(models.Model):
		name = models.CharField(max_length=30)
		age = models.IntegerField()

	guy = Person(name='bob', age='35')
	print guy.age

---

## Exercise 1 - Interfaces

	!python
	class Stream(object):

	    def read(self, count):
			pass
		def write(self, data):
			pass

	>>> class SocketStream(object):
	>>>	    __metaclass__ = Interface(Stream)
	>>>     def read(self, count):
	>>>			pass

	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
        raise NotImplementedError(msg)
	NotImplementedError: write is not implemented for SocketStream

---

## Exercise 1 - Interfaces

Bonus: verify argument count and names (hint: `import inspect`)

	!python
	>>> class SocketStream(object):
	>>>	    __metaclass__ = interface(Stream)
	>>>     def read(self, cont):
	>>>			pass # typo!

	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
        raise NotImplementedError(msg)
	NotImplementedError: argument diff in read: \
		['self', 'count'] vs. ['self', 'cont']

---

## Exercise 1 - Solution

	!python
	import inspect

	def interface(interface_class):
		class Interface(type):
			def __new__(cls, name, bases, dct):
				for attr, value in interface_class.__dict__.iteritems():
					if not inspect.isfunction(value):
						continue
					if attr not in dct: # missing method!
						fmt = '{} is not implemented for {}'
						msg = fmt.format(attr, name)
						raise NotImplementedError(msg)
					check_signatures(value, dct[attr])
		return Interface

---

## Exercise 1 - Solution

	!python
	def check_signatures(orig, new):
		if not inspect.isfunction(new):
			fmt = '{} should be a function but is a {}'
			raise NotImplementedError(fmt.format(new, type(new)))

		orig_args = inspect.getargspec(orig).args
		new_args = inspect.getargspec(new).args
		if orig_args != new_args:
			fmt = 'argument diff in {}: {} vs. {}'
			msg = fmt.format(new, orig_args, new_args)
			raise NotImplementedError(msg)

---

## Exercise 2 - Singleton

## Exercise 3 - decorate all methods
