# Unittests

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
