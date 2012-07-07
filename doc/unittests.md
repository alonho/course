# Unittests

---

## Projects with no unittest

You start by writing small functions and modules. Test everything manually and fast. You don't need automatic tests. 

A month passes. You have tons of code. What happens if you change this? how does it affect other parts? how long does it take to test the code manually? is it even possible to test it manually?

---

## Why unittest

1. test the impossible - test code that interacts with a server that is not yet implemented.
2. get feedback, fast! - if you broke something, you can know about it in a manner of seconds.
3. tests improve the code and design - tests are easier to write when APIs are simple and components are decoupled. by writing tests you are forced to improve the code!
4. regression - the fear factor is eliminated because the tests immediately verify the code works and bugs didn't re-appear.
5. maintainabillity - when another developer gets ownership on code with tests, the tests protect him in cases he didn't completely understand the code. code without tests has higher chances of being thrown away relatively to code with tests.

---

## Integration tests

Why you should also have integration tests:

1. A lot of bugs appear where multiple modules interact.
2. The ratio between the test code and tested code is usually better than unittest. Example: uploading a movie to youtube is a relatively simple process. a lot of code is running to make it happen in youtube, but a test can be fairly short.
3. Performance problems often appear only when a number of components interact.
4. The integrity in the systems quality improves as more components of the system are tested automatically.

Integration tests also have downsides:

1. Integration tests are harder to maintain - they require more components to stay unchanged.
2. Integration tests take longer to run.

**Try to unittest everything. Write integration tests to the common paths of the system.**

---

## Example

	!python
	from unittest import TestCase

	def div(x, y):
		return x / y

	class TestDiv(TestCase):
		
		def test_sanity(self):
			self.assertEquals(div(10, 2), 5)
		
		def test_0(self):
			with self.assertRaises(ZeroDivisionError):
				div(3, 0)
				
The builtin unittest module can run tests:

	!bash
	python -m unittest test.py
	
Or use nose, which is a smart test runner:
	
	!bash
	nosetests test

---

## Mock

Mocking is a technique used when in unittests for replacing external dependencies with fake objects or functions. Here's an example of code which is hard to test:
	
	!python
	import os, errno
	
	def log(data):
		try:
			with open("log", "a") as f:
				f.write(data)
		except IOError as e: # hard drive full
			if e.errno == errno.ENOSPC:
				return False
		return True
	
	import mock, unittest

	class TestLog(unittest.TestCase):
		def test(self):
			with mock.patch('__builtin__.open') as open_func:
				error = IOError()
				error.errno = errno.ENOSPC
				open_func.side_effect = error			
				self.assertEquals(False, log("some data"))

---

		
