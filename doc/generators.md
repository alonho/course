# Generators 

Generators can yield values, accept values via send and process exception via throw.

	!python
	def generator():
		yield 1
		a = yield
		print a
		try:
			yield
		except Exception as e:
			print "caught {}".format(e)
		
	>>> gen.next()
	1
	>>> gen.next()
	>>> gen.send(2)
	2
	>>> gen.throw(ValueError(3))
	caught 3
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    StopIteration


---

## Exercise 1 - flatten

	!python
	>>> for i in flatten(range(3), range(3, 5)):
	...     print i,
	0 1 2 3 4

---

## Execrise 1 - solution

	!python
	def flatten(*iterables):
		for iterable in iterables:
			for i in iterable:
				yield i

---

## Exercise 2 - find dependencies

Print every imported module and how many times it is imported for all python modules in a directory (recursive!):

	!python
	>>> print_deps("/tmp")
	os      1
	sys     2
    csv     1
	
Note: import can be done using `import os` and `from os import environ`.

---

## Map and filter

Map and filter provide an alternative for list comprehensions and for loops.

The following examples show cases where they are preferred over regular for loops and list comprehensions:

	!python
	>>> ints = [5, 6, 7]
	>>> filter(is_prime, ints) # [i for i in ints if is_prime(i)]
	[5, 7]
	>>> map(str, ints) # [str(i) for i in ints]
	['1', '2', '3']

The itertools module provides `ifilter` and `imap` for generator versions:

	!python
	>>> ints = [5, 6, 7]
	>>> from itertools import ifilter
	>>> first_prime = ifilter(is_prime, ints).next() # no need to process the whole list!
	>>> first_prime
	5
	
TIP: map and filter are implemented in C. they can be up to twice as fast.

---

## Reducers

Reducers take a sequence and return a single value.
	
	!python
	>>> sum(xrange(4))
	6
	>>> sum([[1], [2]], [])
	[1, 2]
	>>> all([True, False])
	False
	>>> any([True, False])
	True
	>>> max(xrange(4))
	3
	>>> people = [{'name': 'bar', 'age': 30}, {'name': 'foo', 'age': 20}]
	>>> min(people, key=lambda person: person['age'])
	{'name': 'foo', 'age': 20}

---

## Sorting

Sorting in python is always for the smallest to the biggest.

	!python
	>>> l = [3, 2, 1]
	>>> sorted(l) # generate a new sorted list
	[1, 2, 3]
	>>> l # original list untouched
	[3, 2, 1]

	>>> l.sort() # in-place
	>>> print l
	[1, 2, 3]

	>>> people = [{'name': 'foo', 'age': 20}, {'name': 'bar', 'age': 30}]
	>>> sorted(people, key=lambda person: person['age'], reverse=True)
	[{'name': 'bar', 'age': 30}, {'name': 'foo', 'age': 20)]
	
---

## Secondary sort

Sorting over more than one field can be done by generating a tuple containing them.
When comparing tuples, all the first items are compared, then all the second items, etc'.

	!python
	>>> messages = [{'msg': 'foo', 'year': 2012, 'month': 5}, 
	...             {'msg': 'bar', 'year': 2011, 'month': 6},
	...             {'msg': 'spam', 'year': 2012, 'month': 4}]  
	>>> sorted(messages, key=lambda msg: (msg['year'], msg['month']))
	[{'msg': 'bar', 'year': 2011, 'month': 6},
     {'msg': 'spam', 'year': 2012, 'month': 4},
	 {'msg': 'foo', 'year': 2012, 'month': 5}]

---

## Exercise 3 - primes

Print the first N primes. (a prime number is bigger then 1 and divides only by itself and 1).

	!python
	>>> print_first_primes(3)
	2
	3
	5

---

## Exercise 4 - primes continued

	!python
	>>> print primes(100, 110)
	547
	557
	563
	569
	571
	577
	587
	593
	599
	601
	
---

## Exercise 4 - solution

	!python
	from itertools import ifilter, count

	def take(n, gen):
		for i in xrange(n):
			yield gen.next()

	def is_prime(n):
		if n == 1: # 1 is special
			return False
		for i in xrange(2, (n / 2) + 1):
			if n % i == 0:
				return False
		return True

	def prime_generator():
		return ifilter(is_prime, count(1))

---

## Exercise 4 - solution

	!python
	def get_first_primes(n):
		return take(n, prime_generator())

	def print_first_primes(n):
		for prime in get_first_primes(n):
			print prime

	def get_primes(start, end):
		gen = prime_generator()
		for i in take(start, gen):
			pass
		return take(end - start, gen)

	def print_primes(start, end):
		for prime in get_primes(start, end):
			print prime
