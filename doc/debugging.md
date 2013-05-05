# Debugging 

---

## Ipython 

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

### ipython utility functions

* `pdb` - commands ipython to drop into pdb on exception.
* `?` - writing `open?` or `file?` will show the object's signature and documentation.
* `??` - writing `func??` will show it's code (only if it's python and not C).
* `!` -  execute shell commands
* `!!` - execute shell commands and returns results
* `timeit` - `timeit [1] * 1000` will print the run time of the statement.

---

## Utilties

* `python -m pdb` - enter pdb on exception
* ipdb or pudb - better pdb!
* gdb - attach
* pstuck and pytrace

---

## IDE

Make sure you use an IDE (eclipse, emacs with with pyflakes etc') that supports static analysis. If it does, It can show you some trivial bugs like syntax errors and typos.

### PEP 8

PEP 8 is a standard coding convention for python. If you'll follow it, you'll have an easier time understanding other people's code. 

Some IDEs can be configured to verify it for you.

How to enable it in eclipse: pep8 is included with PyDev 2.3.0 and up. enable it in PyDev > Editor > Code Analysis > pep8.py
