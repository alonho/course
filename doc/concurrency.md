# Concurrency

---

## Exercise - CPU-bound example

Find all the prime numbers until 'end' in a given amount of 'threads'.

    !python
    >>> calc_primes(end=50, threads=5)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

Try to use `multiprocessing` module, to get performance gain (from multi-core CPU).

---

## Exercise - solution

    !python
    from multiprocessing import Pool

    def is_prime(n):
        if n == 1: # 1 is special
            return False

        divisors = xrange(2, (n / 2) + 1)
        return all(n % d != 0 for d in divisors)

    def calc_primes_pool(end, threads):
        p = Pool(threads)

        results = []
        for i in xrange(end):
            result = p.apply_async(is_prime, (i,))
            results.append((i, result))

        for i, result in results:
            if result.get():
                yield i

---

## I/O-bound concurrency

Let's say we want to write a TCP server that counts the number of connection
attempts, and writes it back to the client.

    $ netcat localhost 5000
    <1, took 24.6 ms>

    $ netcat localhost 5000
    <2, took 14.8 ms>

    $ netcat localhost 5000
    <3, took 15.5 ms>

    $ netcat localhost 5000
    <4, took 15.9 ms>

    $ netcat localhost 5000
    <5, took 19.0 ms>

---

### Naive implementation

    !python
    class Server(object):
        def __init__(self):
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.s.bind(('localhost', 5000))
            self.s.listen(10)
            self.n = 0

        def run(self):
            while True:
                conn, peer = self.s.accept()
                self.handle(conn, peer)

        def handle(self, conn, peer):
            tmp = self.n
            t = time.time()
            for i in xrange(1000000):
                pass  # simulate request processing
            dt = time.time() - t
            self.n = tmp + 1
            conn.sendall('<{0}, took {1:.1f} ms>\n'.format(self.n, dt*1e3))

---

### Naive threaded implementation

    !python
    class Server(object):
        def __init__(self):
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.s.bind(('localhost', 5000))
            self.s.listen(10)
            self.n = 0

        def run(self):
            while True:
                conn, peer = self.s.accept()
                t = threading.Thread(target=self.handle, args=(conn, peer))
                t.start()

        def handle(self, conn, peer):
            tmp = self.n
            t = time.time()
            for i in xrange(1000000):
                pass  # simulate request processing
            dt = time.time() - t
            self.n = tmp + 1
            conn.sendall('<{0}, took {1:.1f} ms>\n'.format(self.n, dt*1e3))

---

## Let's test it!

    !bash
    $ nc localhost 5000
    <1, took 17.8 ms>

    $ nc localhost 5000
    <2, took 17.5 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &);
    <3, took 62.8 ms>
    <3, took 61.3 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &);
    <4, took 66.1 ms>
    <4, took 64.4 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &); (nc localhost 5000 &);
    <5, took 105.6 ms>
    <5, took 111.5 ms>
    <5, took 110.3 ms>

    $ nc localhost 5000
    <6, took 17.4 ms>

---

## Discussion

We forgot to make sure that `self.n` is updated **atomically**,
and got a race condition.

We have to **synchronize** all accesses to shared memory between threads,
because we cannot tell when the threads will be scheduled to run.

Can we have something better?

We would like our code to run atomically, but to be able to yield control to
other tasks, when we allow it to.

This is called "cooperative multitasking", and the tasks (that use cooperation
to achieve concurrency) are also called "green threads".

Since Python currently does not support CPU-bound concurrency, we would like
our tasks to cooperate around I/O events.

Can we have **atomicity** on CPU access, but **cooperation** around I/O events?

---

## Yes, we can!

This is exactly what `gevent` library provides us.

    !python
    >>> from gevent import socket
    >>> def request(addr):
    ...     s = socket.create_connection(('localhost', 5000))
    ...     return s.recv(1024)

    >>> addr = ('localhost', 5000)
    >>> request(addr)
    '<10, took 20.1 ms>'

    >>> request(addr)
    '<11, took 18.3 ms>'

    >>> request(addr)
    '<12, took 20.3 ms>'

---

## Concurrent requests

    !python
    >>> f1 = gevent.spawn(request, addr)
    >>> f2 = gevent.spawn(request, addr)
    >>> f3 = gevent.spawn(request, addr)
    >>> f1.get()
    '<13, took 78.6 ms>'
    >>> f2.get()
    '<13, took 80.2 ms>'
    >>> f3.get()
    '<13, took 81.5 ms>'

This is concurrent execution, reproducing our race condition :)

---

## Exceptions

`.get()` method raises an error if its greenlet failed with exception:

    >>> f = gevent.spawn(request, ('1.2.3.4', 5678))
    >>> f.get()
    Traceback (most recent call last):
      File "/usr/local/lib/python2.7/dist-packages/gevent/greenlet.py", line 327, in run
        result = self._run(*self.args, **self.kwargs)
      File "<stdin>", line 2, in request
      File "/usr/local/lib/python2.7/dist-packages/gevent/socket.py", line 591, in create_connection
        raise err
    error: [Errno 111] Connection refused
    <Greenlet at 0x7f2c3344bc30: request(1)> failed with error

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/lib/python2.7/dist-packages/gevent/greenlet.py", line 274, in get
        raise self._exception
    socket.error: [Errno 111] Connection refused


It's much better than the default thread behaviour.

---

## gevent-based server

    !python
    class Server(object):

        def __init__(self):
            addr = ('localhost', 5001)
            self.s = gevent.server.StreamServer(addr, self.handle)
            self.n = 0

        def run(self):
            self.s.serve_forever()

        def handle(self, conn, peer):
            tmp = self.n
            t = time.time()
            for i in xrange(1000000):
                pass
            dt = time.time() - t
            self.n = tmp + 1

            conn.sendall('<{0}, took {1:.1f} ms>\n'.format(self.n, dt*1e3))
            conn.close()
