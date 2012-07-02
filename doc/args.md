
# Advanced Python Topics

---

## args (*)

Allows printf style variadic functions.

**variadic function - a function that gets a variable number of arguments.**


Usage example:

	!python
	logger.info("%s, I am your %s", jedi, relationship)

Implementation example:

	!python
	def f(*args): # you can call it in a different name if you want, the * is a must
		print type(args), args
	    print 

	>>> f(1, 2, 3)
	tuple (1, 2, 3)
	
---

The reverse operation - pass a sequence as the arguments:

	!python
	>>> f(*(1,2,3))
	tuple (1, 2, 3)

    >>> f(*[1,2,3]) # we can put any iterable here
	tuple (1, 2, 3)

    >>> f(*'abc') # and I mean, any iterable
	tuple ('a', 'b', 'c')

When unpacking in a non variadic function call, make sure the number of args match:

	!python
	def add(x, y):
		return x + y
		
	>>> add(*[1, 2, 3])
	Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: add() takes exactly 2 arguments (3 given)
	
---
	
## kwargs (\*\*)

* Keyword arguments allow passing values by argument name: `foo(a=10)`
* Enables default values.
* Improves readability and maintainability.
* **TIP**: When calling a function that receives many arguments, name them.

Examples:

	!python
	def foo(**kwargs):
		print kwargs
		
	>>> foo(a=1, b=2)
	{'a': 1, 'b': 2}
	
	>>> foo(**{'a': 1, 'b': 2})
    {'a': 1, 'b': 2}
	
	def foo(a, b=None):
		print a, b
		
    >> foo(**{'a': 1, 'b': 2})
	1 2
