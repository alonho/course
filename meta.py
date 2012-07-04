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

from itertools import ifilter, count
def prime_generator():
	return ifilter(is_prime, count(1))

def get_first_primes(n):
	return take(n, prime_generator())

def get_primes(start, end):
	gen = prime_generator()
        for i in take(start, gen):
            pass
	return take(end - start, gen)

def print_first_primes(n):
	for prime in get_first_primes(n):
		print prime
		
def print_primes(start, end):
	for prime in get_primes(start, end):
		print prime