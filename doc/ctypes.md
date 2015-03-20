# ctypes

---

## Introduction

This talk is heavily based on the `ctypes` module's excellent documentation: <https://docs.python.org/library/ctypes.html>

## What is `ctypes`?

`ctypes` is a foreign function library for Python. 

It provides C compatible data types, and allows calling functions in DLLs or shared libraries. 

It can be used to wrap these libraries in pure Python.

It's part of CPython from 2.5 version.

---

## An example

### Linux

    !python
    >>> import ctypes as c
    >>> d = c.CDLL("libc.so.6")  # /lib/x86_64-linux-gnu/libc.so.6
    >>> print d.printf("Hello Linux World\n")
    Hello Linux World
    18


### Windows

    !python
    >>> import ctypes as c
    >>> d = c.CDLL('msvcrt')
    >>> print d.printf("Hello Windows World\n")
    Hello Windows World
    20

---

## Calling functions

You can access the exported functions via library object's attributes:

    !python
    >>> printf1 = d.printf
    >>> printf2 = getattr(d, 'printf')
    >>> assert printf1 is printf2

IMPORTANT: make sure you pass the right arguments to the library's functions!

What happens if you are wrong?

---

## Exercise 1:

What should happen when this code runs?

    !python
    >>> x = 123
    >>> d.printf("x = %d\n", x)

And now?

    !python
    >>> x = 123
    >>> y = 45
    >>> d.printf("x = %d\n", x, y)

And now?

    !python
    >>> x = 123
    >>> d.printf("x = %s\n", x)

---

## Conclusion

With great power, comes great responsibility :)

`ctypes` is **very** easy to use, but it also makes it **very** to easy to "shoot yourself in the foot".

Protect yourself with a good unittest suite, to make sure you are accessing your libraries correctly.

---

## How `ctypes` really works?

In order to call a C function, you should follow some kind of "calling convention".

It usually involves:

- how the arguments should be stored (registers/stack)
- how the return value should be retrieved.

To do this correctly, you actually need to "build" the correct stack structure for the function you want to call,
call it, and parse the returning stack structure to obtain the results. 

This is all done automatically by the compiler each time you call a function.

`ctypes` knows how to "reproduce" this "magic" from Python, so you can call **any** C function.

---

## Data types

Note that we called `printf` with Python's string object, and somehow it worked.

Under the hood, `ctypes` converted `str` into its underlying `char *` type and passed it to `printf`.

It also automatically converts Python's `int` into `signed long int` C type.

In order to be explicit about your arguments' types use `c_*` type system:

---

## Data types

    ctypes type     |   C type              | Python type
    --------------------------------------------------------------------
    c_bool          |   _Bool               | bool (1)
    c_char          |   char                | 1-character string
    c_wchar         |   wchar_t             | 1-character unicode string
    c_byte          |   char                | int/long
    c_ubyte         |   unsigned char       | int/long
    c_short         |   short               | int/long
    c_ushort        |   unsigned short      | int/long
    c_int           |   int                 | int/long
    c_uint          |   unsigned int        | int/long
    c_long          |   long                | int/long
    c_ulong         |   unsigned long       | int/long
    c_longlong      |   long long           | int/long
    c_ulonglong     |   unsigned long long  | int/long
    c_float         |   float               | float
    c_double        |   double              | float
    c_longdouble    |   long double         | float
    c_char_p        |   char *              | string or None
    c_wchar_p       |   wchar_t *           | unicode or None
    c_void_p        |   void *              | int/long or None

---

## Data types

An example:

    !python
    >>> printf = libc.printf
    >>> printf("Hello, %s\n", "World")
    Hello, World
    13
    >>> printf("Hello, %S\n", u"World")
    Hello, World
    13
    >>> printf("%d bottles of beer\n", 42)
    42 bottles of beer
    19
    >>> printf("%f bottles of beer\n", 42.5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ArgumentError: argument 2: exceptions.TypeError: \
                Don't know how to convert parameter 2
    
    >>> printf("An int %d, a double %f\n", 1234, c_double(3.14))
    An int 1234, a double 3.140000
    31

---

## Return value

    !python
    >>> strchr = libc.strchr
    >>> strchr("abcdef", ord("d")) 
    8059983
    >>> strchr.restype = c_char_p # c_char_p is a pointer to a string
    >>> strchr("abcdef", ord("d"))
    'def'
    >>> print strchr("abcdef", ord("x"))
    None
    >>>

---

## Passing by reference

    !python
    >>> i = c_int()
    >>> f = c_float()
    >>> s = create_string_buffer('\x00' * 32)
    >>> print i.value, f.value, repr(s.value)
    0 0.0 ''
    >>> libc.sscanf("1 3.14 Hello", "%d %f %s",
    ...             byref(i), byref(f), s)
    3
    >>> print i.value, f.value, repr(s.value)
    1 3.1400001049 'Hello'
    >>>

---

## Setting types for functions

    !python
    >>> strchr = libc.strchr
    >>> strchr.restype = c_char_p
    >>> strchr.argtypes = [c_char_p, c_char]
    >>> strchr("abcdef", "d")
    'def'
    >>> strchr("abcdef", "def")
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    ArgumentError: argument 2: exceptions.TypeError: \
            one character string expected
    >>> print strchr("abcdef", "x")
    None
    >>> strchr("abcdef", "d")
    'def'
    >>>

---

## More goodies

* pointers
* structures
* unions
* byte-alignment
* byte order
* typed arrays
* callback functions (so you can use stdlib's `qsort` from Python)

---

## Exercise

Use ctypes to generate pseudo-random numbers using a `random()` function from your C library:


    Macro: int RAND_MAX

        The value of this macro is an integer constant representing the 
        largest value the rand function can return. 

        In the GNU C Library, it is 2147483647, which is the largest signed
        integer representable in 32 bits. 

        In other libraries, it may be as low as 32767. 

    Function: int rand (void)

        The rand function returns the next pseudo-random number in the series. 
        The value ranges from 0 to RAND_MAX. 

---

## Solution

    !python
    >>> import ctypes as c
    >>> d = c.CDLL("libc.so.6") 
    >>> RAND_MAX = 2.0 ** 31
    >>> [d.random()/RAND_MAX for _ in xrange(10)]
    [0.6288709244690835,
     0.36478447262197733,
     0.5134009099565446,
     0.9522297247312963,
     0.916195067577064,
     0.6357117276638746,
     0.7172969290986657,
     0.14160255528986454,
     0.6069688759744167,
     0.016300571616739035]

