
# The Standard Library

## Threading

---

### Exercise 1 - primes

Find all the prime numbers until 'end' in a given amount of 'threads'.

	!python
	>>> calc_primes(end=50, threads=5)
	[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

Note: remember there is no performance gain here because of the GIL (global interpreter lock).

---

Bonus 1: how does the threaded version compare to a non-threaded one?

Bonus 2: convert the implementation to use multiprocessing.

---

### Exercise 1 - multiprocessing

	!python
	from multiprocessing import Pool

	def is_prime(n):
		if n == 1: # 1 is special
			return False
		for i in xrange(2, (n / 2) + 1):
			if n % i == 0:
				return False
		return True

	def calc_primes_pool(end, threads):
		p = Pool(threads)
		results = [(p.apply_async(is_prime, (i,)), i) for i in xrange(end)]
		for result, value in results:
			if result.get():
				yield value

---

### Exercise 1 - threaded solution

	!python
	from Queue import Queue, Empty
	import threading

	def worker(in_queue, out_queue):
		while True:
			value = in_queue.get()
			if value is None:
				break
			if is_prime(value):
				out_queue.put(value)
        
	def calc_primes_queues(end, threads):
		in_queue, out_queue = Queue(), Queue()
		threads = [threading.Thread(target=worker, args=(in_queue, out_queue))
                   for i in xrange(threads)]
        [thread.start() for thread in threads]	
		map(in_queue.put, xrange(end))
		[in_queue.put(None) for i in xrange(len(threads))]
		[thread.join() for thread in threads]
		result = []
		while True:
			try:
				result.append(out_queue.get_nowait())
			except Empty:
				break
		return result

---

## Collections

### `Counter`

	!python
	>>> cnt = Counter()
	>>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
	...     cnt[word] += 1
	>>> cnt
	Counter({'blue': 3, 'red': 2, 'green': 1})
	
	>>> cnt2 = Counter(['red', 'green']) # init with a list
	>>> cnt - cnt2
	Counter({'blue': 3, 'red': 1})

---

### `deque`

A double ended queue. provides O(1) complexity for addition/deletion on both sides.

using `maxlen` the deque can be used as a cyclic buffer:

	!python
	from collections import deque
	def tail(filename, n=10):
		"""Return the last n lines of a file"""
		return deque(open(filename), n)

---

### `defaultdict`

`defaultdict` is dictionary with default values for non-existing keys.

	!python
	>>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
	>>> d = defaultdict(list)
	>>> for k, v in s:
	...     d[k].append(v)
	...
	>>> d.items()
	[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

`defaultdict` is faster than the `dict`'s alternative `setdefault` method:

	!python
	>>> d = {}
	>>> for k, v in s:
	...     d.setdefault(k, []).append(v)
	...
	>>> d.items()
	[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
	
---

### `namedtuple`

a `namedtuple` can be used anywhere a `tuple` is used (it inherits from `tuple`).

	!python
	>>> from collections import namedtuple
	>>> Point = namedtuple("Point", "x y") # generates a class
	>>> p = Point(10, 20) 
	>>> print p # automatic __repr__
	Point(x=10, y=20)
	>>> x, y = p
	>>> p.x = 100 # immutable
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute

TIP: The `namedtuple` takes less memory than regular objects because it doesn't have a `__dict__`. Event though it has a `__dict__` attr, it generates a dictionary only when accessed.

---

### Exercise 2 - find cap words

	!python
	print_cap_words("Do not Take life Too seriously. You will never get out of it alive.")
	Y : You
	D : Do
	T : Take, Too

---

### Exercise 2 - solution

	!python
	from collections import defaultdict
	import re
	
	def find_cap_words(s):
		char_to_words = defaultdict(set)
		for word in re.findall('[A-Z][a-z]*', s):
			char_to_words[word[0]].add(word)
		return char_to_words
		
	def print_cap_words(s):
		for char, words in find_cap_words(s).iteritems():
			print char, ':', ', '.join(words)

---

### Exercise 3 - char counter

	!python
	>>> char_count("abbcccdddd")
	{'a': 1, 'b': 2, 'c': 3, 'd': 4}

	>>> word_count("How much wood can a woodchuck chuck if a woodchuck would chuck wood")
	{'How': 1,
	 'a': 2,
     'can': 1,
     'chuck': 2,
     'if': 1,
     'much': 1,
     'wood': 2,
     'woodchuck': 2,
     'would': 1}

Bonus: add an `int` argument called `most_common` for returning only the most common char/word.

---

### Exercise 3 - solution

	!python
	from collections import Counter
	def char_count(s):
		return Counter(s)
	
	def word_count(s):
		return Counter(s.split())
	
And the bonus:

	!python
	def char_count_common(s, most_common):
		return dict(char_count(s).most_common(most_common))
	
	def word_count_common(s, most_common):
		return dict(word_count(s).most_common(most_common))
		
---

## Exercise 4 - subprocess 

Implement a grep function using `subprocess.Popen` and the unix `grep`:

	!python
	foo.txt:
	foo
	bar
	foobar
	spam
	eggs

	>>> l = grep("foo", "foo.txt")
	>>> l
	["foo", "foobar"]

Bonus: implement the grep process as a python script.

---

## Exercise 4 - solution

grep.py:

	!python
	def grep(string, input_file):
		line = input_file.readline()
		while line != '':
			if string in line:
				yield
			line = input_file.readline()

	if __name__ == '__main__':
		with open(sys.argv[2]) as input_file:
			for line in grep(string=sys.argv[1], input_file=input_file):
				sys.stdout.writeline(line)

main.py:
	
	!python
	def grep(string, path):
		proc = subprocess.Popen("python grep.py {} {}".format(string, path),
		                        stdout=subprocess.PIPE,
							    shell=True)
		return map(str.strip, proc.stdout.readlines())

---

## Exercise 5 - sets

	!python
	>>> compare_strings("spam", "eggs")
	chars in spam and not in eggs: apm
	chars in eggs and not in spam: eg
	chars in one and not the other: aegmp
	chars in both strings:  s
	all chars:  apsegm
	spam contained in eggs: False
	eggs contained in spam: False

---

## Exercise 5 - solution

	!python
	def compare_strings(a, b):
		a_set = set(a)
		b_set = set(b)
		join_set = ''.join
		print "chars in {} and not in {}: {}".format(a, b, join_set(a_set - b_set))
		print "chars in {} and not in {}: {}".format(b, a, join_set(b_set - a_set))
		print "chars in one and not the other:", join_set(a_set ^ b_set)
		print "chars in both strings: ", join_set(a_set & b_set)
		print "all chars: ", join_set(a_set | b_set)
		print "{} contained in {}: {}".format(a, b, a_set <= b_set)
		print "{} contained in {}: {}".format(b, a, b_set <= a_set)
	
---

## StringIO

The `StringIO` module has two use cases:
	
### Mimic a `file` object

The `StringIO.StringIO` object implements the file object interface and behaves as an in-memory file.

	!python
	def ungzip(string):
		return GzipFile(fileobj=StringIO(string)).read()


This is also great for unittest:

	!python
	def test_grep():
		assert ["foo", "foobar"] == grep("foo", StringIO("foo\nbar\nfoobar"))
	

Note: the `cStringIO` module is a (faster) C implementation of StringIO.

---

### Growing strings

A very delicate performance issue in python is collection of data from a stream:

	!python
	>>> s = read()
	>>> s += read() # allocates a new string, bigger than the last!
	>>> s += read() # this will become slower and slower as the string grows.
	>>> return s

A faster implementation:

	!python
	>>> l = []
	>>> l.append(read())
	>>> l.append(read())
	>>> return ''.join(l)

A faster and more elegent implementation:

	!python
    >>> from StringIO import StringIO
	>>> s = StringIO()
	>>> s.write(read())
	>>> s.write(read())
	>>> return s.getvalue()


---

## pickle

`pickle` or it's C implementation `cPickle` provides serialization functions for python objects:

	!python
	>>> cPickle.dumps([1, 2])
	'(lp1\nI1\naI2\na.'
	>>> cPickle.loads(_)
	[1, 2]

It is used throughout the standard library (e.g. `multiprocessing`).

Not all objects are pickleable: sockets, methods (not functions, methods), etc'.

If your object is not pickleable, or you want to pickle it in a custom way you can define methods for `pickle` to use: `__getstate__` and `__setstate__`.

---

## Exercise 6 - implement a db

	!python
	>>> with DB(path='db') as db:
	>>>     db['a'] = 10
	>>>     db['b'] = [1, 2, 3]
	>>>
	>>> db = DB(path='db')
	>>> db['a']
	10
	>>> db['b']
	[1, 2, 3]
	>>> db.close()
	
Hint: `obj[key]` translates to `obj.__getitem__(key)`, `obj[key] = value` translates to `obj.__setitem__(key, value)`.
	
---

## Exercise 6 - solution

Ha! you implemented the `shelve` module!

---

* `itertools` - generators versions to existing functions and more: izip, islice, imap, ifilter, cycle, repeat, chain, groupby.
* `array` - lists to/from C arrays. good for interacting with the OS.
* `struct` - build and unpack C types and structs.
* `argparse` - from 2.7. if not available can be installed as package.
* `brownie` - not in the stdlib. contains many nice utilities like `ImmutableDict`.

---

## External Libraries

### lxml - building

	!python
	>>> from lxml.builder import E	
	>>> page = (
	...   E.html(       # create an Element called "html"
	...     E.head(
	...       E.title("This is a sample document")
	...     ),
	...     E.body(
	...       E.h1("Hello!"),
	...       E.p("This is a paragraph with ", E.b("bold"), " text in it!"),
	...     )
	...   )
	... )

	>>> print(etree.tostring(page, pretty_print=True))
	<html>
		<head>
			<title>This is a sample document</title>
		</head>
		<body>
			<h1>Hello!</h1>
			<p>This is a paragraph with <b>bold</b> text in it!</p>
		</body>
	</html>

---

## lxml - iterative parsing

	!python
	>>> xml_file = StringIO('''\
	... <root>
	...   <a><b>ABC</b><c>abc</c></a>
	...   <a><b>MORE DATA</b><c>more data</c></a>
	...   <a><b>XYZ</b><c>xyz</c></a>
	... </root>''')

	>>> for _, element in etree.iterparse(xml_file, tag='a'):
	...     print('%s -- %s' % (element.findtext('b'), element[1].text))
	...     element.clear()
	ABC -- abc
	MORE DATA -- more data
	XYZ -- xyz	
	
---

## Exercise 7 - xor a buffer

What would be the fastest way to xor a buffer with 0x7b?

	!python
	>>> xor_buf('\x01\x02\x03', 0x7b)
	'zyx'
	
---	

## `numpy`

`numpy` has similar qualities to the `array` module except that it supports multi-dimensional arrays, array and matrix algebra and is widely used for scientific means.

	!python
	>>> arr = numpy.array([1, 2, 3], dtype=int8)
	>>> arr
	array([1, 2, 3], dtype=int8)
	>>> arr + 1
	array([2, 3, 4], dtype=int8)
	>>> arr ^ 0x7b
    array([122, 121, 120], dtype=int8)
	>>> xored = _
	>>> xored.tostring()
	'zyx'

---

### Exercise 2 - echo server

Implement an echo server, which upper cases every input. It should support multiple clients concurrently. Remember the limitation on number of threads. consider using select/poll.

Some client code for example.

	!python
	>>> import socket
	>>> sock = socket.socket()
	>>> sock.connect(('127.0.0.1', 12345))
	>>> sock.send('foo')
	>>> sock.recv(3)
	'FOO'
	>>> sock.send('bar')
	>>> sock.recv(3)
	'BAR'

Simple server code:
	
	!python
	>>> import socket
	>>> server = socket.socket()
	>>> server.bind(("127.0.0.1", 12345))
	>>> server.listen(1)
	>>> (sock, addr) = server.accept()
	>>> sock.send(sock.recv(1024).upper())
