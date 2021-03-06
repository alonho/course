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

	$ python -m unittest test

Or use nose, which is a smart test runner:

	$ nosetests test

---

## Mock

Mocking is a technique used when in unittests for replacing external dependencies with fake objects or functions. Here's an example of code which is hard to test:

	!python
	def log(data):
		try:
			with open("log", "a") as f:
				f.write(data)
		except IOError as e: # hard drive full
			if e.errno == errno.ENOSPC:
				return False
		return True

	class TestLog(unittest.TestCase):
		def test_no_space(self):
			with mock.patch('__builtin__.open') as open_func:
				error = IOError()
				error.errno = errno.ENOSPC
				open_func.side_effect = error
				self.assertEquals(False, log("foobar"))
		def test(self):
			with mock.patch('__builtin__.open') as open_func:
				self.assertEquals(True, log("foobar"))
				open_func.return_value.write.assert_called_with("foobar")

---

## Mocking objects

	!python
	class EmailServer(object):

		def __init___(self, ip, port):
			...

		def send_email(self, recipient, message):
			...

	def send_emails(email_server, recipients, message):
		for recipient in recipients:
			email_server.send_email(recipient, message)

	class TestSendMessages(TestCase):

		def test(self):
	        m = mock.create_autospec(EmailServer)
			send_emails(m, ["joe", "mike"], "help!")
			m.send_email.assert_called_with("joe", "help!")
			m.send_email.assert_called_with("mike", "help!")

---

## Mocking `self`

By mocking `self` we can test a method in complete isolation. No need to initialize an object. (great for sockets, files)

	!python
	class EmailServer(object):

		def __init___(self, ip, port):
			...

		def send_email(self, recipient, message):
			...

		def send_emails(self, recipients, message):
			for recipient in recipients:
				self.send_email(recipient, message)

	class TestSendMessages(TestCase):

		def test(self):
	        m = mock.create_autospec(EmailServer)
			EmailServer.send_emails(m, ["joe", "mike"], "help!")
			m.send_email.assert_called_with("joe", "help!")
			m.send_email.assert_called_with("mike", "help!")

---

## Exercise

Use `mock` to test the following code:

	!python
	import time
	def sleep_and_execute(func):
	    time.sleep(60)
		func()

	import socket
	def read(sock):
		data = sock.recv(4096)
		if data == '':
			raise socket.error('socket closed')
		return data

---
## Solution

    !python
    def test_sleep():
        with mock.patch('time.sleep') as s:
            f = mock.Mock()
            sleep_and_execute(f)
            f.assert_called_with()
            s.assert_called_with(60)

    class TestSocket(unittest.TestCase):

        def test_read_sock(self):
            sock = mock.Mock()
            sock.recv.return_value = 'foo'
            self.assertEquals(read(sock), 'foo')

        def test_read_error(self):
            bad_sock = mock.Mock()
            bad_sock.recv.side_effect = IOError

            with self.assertRaises(IOError):
                read(bad_sock)

---

## Coverage testing

By using the pycoverage module we can generate reports showing exactly which line of code has been tested.

After installing both `coverage` and `nose`, they can be invoked together:

	$ nosetests --with-coverage --cover-package=amodem --cover-html \
		tests/test_dsp.py
	......
	Name              Stmts   Miss  Cover   Missing
	-----------------------------------------------
	amodem                2      0   100%
	amodem.common        55      0   100%
	amodem.config        40      0   100%
	amodem.dsp           89      0   100%
	amodem.sampling      63      0   100%
	-----------------------------------------------
	TOTAL               249      0   100%
	----------------------------------------------------------------------
	Ran 6 tests in 0.457s


You should aim for maximal code coverage, so that each change in the code will be tested by your unittest suite.
This is especially true in Python, where there is no compiler to validate your type system.

---

## Continuous Integration

If you have a good unittest suite, it is recommended to have a CI server that
will run the tests automaticall on each commit, and present the build results
together with code coverage statistics.

For example, see:

* <https://travis-ci.org>, for build automation
* <https://coveralls.io/features>, for code coverage visualization

You should be notified automatically if a test fails or when you have code coverage degradation.
