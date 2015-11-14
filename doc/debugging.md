# Debugging

---

## Logging is your friend

No, really!

Make sure you can understand your code's execution flow
from the finest level log messages.

Colorizing your log may help :)

Use defensive assertions - to catch your errors as soon as possible.
They can be disabled in production (using Python's `"-O"` command line option).

    !bash
    $ python -c "assert 0; print('Done.')"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    AssertionError
    $ python -O -c "assert 0; print('Done.')"
    Done.

Very useful when developing an algorithm - e.g. make sure an array is sorted
(after you sort it).

---

## Exceptions

NEVER swallow exceptions!!!

    !python
    # NEVER do this!
    try:
        func()
    except:
        # will swallow EVERYTHING, including syntax errors and SystemExit!
        # And you will never know what happened...
        pass

If you really (REALLY) need to, do the following:

    try:
        func()
    except Exception:
        log.exception('make sure this error is viewed and acted upon')

Or, use `traceback.print_exc()` to print the exception to stderr.
---

## IPython

### Embedding

A recipe to launch ipython by calling a function:

	!python
	def ishell():
		try:
			from IPython import embed
			embed(user_ns=sys._getframe(1).f_locals)
		except ImportError:
			# IPython < 0.11
			# Explicitly pass an empty list as arguments, because otherwise
			# IPython would use sys.argv from this script.
			try:
				from IPython.Shell import IPShellEmbed
				ipshell = IPShellEmbed(argv=[], user_ns=sys._getframe(1).f_locals)
				ipshell()
			except ImportError:
				# IPython not found at all, raise ImportError
				raise

---

### Example

	!python
	def foo():
		a = 10
		ishell()
		print 20

	if __name__ == '__main__':
		foo()

Run the script:

	!bash
	# python script.py
	In [1]: print a
	10
	In [2]:
	Do you really want to exit ([y]/n)? y
    20

---

### IPython utility functions

* `run` - run the named file inside IPython as a program.
* `history -l 1000` - show latest 1000 commands.
* `pdb` - commands ipython to drop into pdb on exception.
* `?` - writing `open?` or `file?` will show the object's signature and documentation.
* `??` - writing `func??` will show it's code (only if it's python and not C).
* `!` -  execute shell commands
* `!!` - execute shell commands and returns results
* `timeit` - `timeit [1] * 1000` will print the run time of the statement.
* `!ps` - run "ps" as a shell command.

---

## more utilities

* `python -m pdb script.py` - enter pdb on exception
* ipdb or pudb - better pdb!
* gdb - attach to Python interpreter (to debug C extensions)
* pystuck and pytrace

pdb commands:

    (Pdb) help

    Documented commands (type help <topic>):
    ========================================
    EOF    bt         cont      enable  jump  pp       run      unt
    a      c          continue  exit    l     q        s        until
    alias  cl         d         h       list  quit     step     up
    args   clear      debug     help    n     r        tbreak   w
    b      commands   disable   ignore  next  restart  u        whatis
    break  condition  down      j       p     return   unalias  where


---

## Example

Consider the following program:

    !python
    ''' PDB example '''

    def inv(x):
        return 1.0 / x

    def avg(items):
        res = 0.0
        for i in items:
            res = res + inv(i)
        return inv(res)

    if __name__ == '__main__':
        import sys
        args = map(float, sys.argv[1:])
        res = avg(args)
        print(res)

---

The following exception is thrown:

    $ python main.py 2 2 3 0 1
    Traceback (most recent call last):
      File "main.py", line 15, in <module>
        res = avg(args)
      File "main.py", line 9, in avg
        res = res + inv(i)
      File "main.py", line 4, in inv
        return 1.0 / x
    ZeroDivisionError: float division by zero

Let's debug it!

    $ python -m pdb main.py 2 2 3 0 1
    > /tmp/test/main.py(1)<module>()
    -> ''' PDB example '''
    (Pdb)

The program is loaded and waiting to be started.

---

Let's run the program, by issuing the "continue" command (`c`):

    (Pdb) c
    Traceback (most recent call last):
      File "/usr/lib/python2.7/pdb.py", line 1314, in main
        pdb._runscript(mainpyfile)
      File "/usr/lib/python2.7/pdb.py", line 1233, in _runscript
        self.run(statement)
      File "/usr/lib/python2.7/bdb.py", line 400, in run
        exec cmd in globals, locals
      File "<string>", line 1, in <module>
      File "main.py", line 1, in <module>
        ''' PDB example '''
      File "main.py", line 9, in avg
        res = res + inv(i)
      File "main.py", line 4, in inv
        return 1.0 / x
    ZeroDivisionError: float division by zero
    Uncaught exception. Entering post mortem debugging
    Running 'cont' or 'step' will restart the program
    > /tmp/test/main.py(4)inv()
    -> return 1.0 / x
    (Pdb)

---

We can get more context by issuing the "list" command (`l`):

    (Pdb) l
      1     ''' PDB example '''
      2
      3     def inv(x):
      4  ->     return 1.0 / x
      5
      6     def avg(items):
      7         res = 0.0
      8         for i in items:
      9             res = res + inv(i)
     10         return inv(res)
     11
    (Pdb)

---

We can "travel" up and down the stack, and pring local variables:

    (Pdb) u
    > /tmp/test/main.py(9)avg()
    -> res = res + inv(i)
    (Pdb) l
      4         return 1.0 / x
      5
      6     def avg(items):
      7         res = 0.0
      8         for i in items:
      9  ->         res = res + inv(i)
     10         return inv(res)
     11
     12     if __name__ == '__main__':
     13         import sys
     14         args = map(float, sys.argv[1:])

    (Pdb) p res
    1.3333333333333333
    (Pdb) p items
    [2.0, 2.0, 3.0, 0.0, 1.0]
    (Pdb) p i
    0.0

    (Pdb) d
    > /tmp/test/main.py(4)inv()
    -> return 1.0 / x
    (Pdb) d
    *** Newest frame


---

## IDE

Beware of IDEs that implicitly manipulate your Python environment, as this
may result in different behaviour than in production.

### Static analysis

Make sure you use an IDE (eclipse, emacs with with pyflakes, etc.) that supports static analysis.
If it does, it can show you some trivial bugs like syntax errors and typos.

It will save you a lot of debugging time.

### PEP 8

PEP 8 is a standard coding convention for python. If you'll follow it, you'll have an easier time understanding other people's code.

Some IDEs can be configured to verify it for you.

How to enable it in eclipse: pep8 is included with PyDev 2.3.0 and up. enable it in PyDev > Editor > Code Analysis > pep8.py
