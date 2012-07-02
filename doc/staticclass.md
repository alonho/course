# Static And Class Methods

---

## Static Methods

Static methods are basically functions enclosed in a class. 

They can be called directly from the class or from an instance.

They have no access to the instance or class attributes because they don't get `self`.

Somewhat similar to a namespace in C++.
	
	!python
	class NameSpace(object):

	    @staticmethod
		def foo(): # no self!
			print "bar"

	>>> NameSpace.foo()
	bar

I admit I haven't found many use cases for static methods.

---

## Class methods

Class methods can also be called directly from the class or from an instance, but unlike staticmethod that get no arguments or regular methods that get `self` they get the class object as the first argument.

It's common practice to call the argument `cls`. (`class` is a reserved keyword)

A common use case is implementing several constructors for the same class.

Example:

	!python
	class XMLElement(object):

	    def __init__(self, string):
			...
			
		@classmethod
		def from_file(cls, path):
			with open(path) as f:
				return cls(f.read())
			
	>>> element = XMLElement.from_file("bla.xml")

When a class method is called from a child class, the child class is passed as the `cls` argument.
