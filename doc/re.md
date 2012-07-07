# Regular Expressions

Inspired by 'learn regex the hard way' by Zed Shaw

---

## Finding specific strings

	!python
	>>> s = "Do not take life Too seriously."
	>>> from re import search
	>>> print search(r"Don't", s)
	None
	>>> print search(r"Do not", s)
	<_sre.SRE_Match at 0x10cbc73d8>
	>>> m = _
	>>> m.start()
	0
	>>> m.end()
	6

Note: adding 'r' before a strings marks it as a raw string and is highly recommended. without it python may try to interpret escape sequences in the string ('\w' and such which are also regex symbols).

---

## Matching any character

The dot ('.') matches any character except new line.

	!python
	>>> s = "Do not take life Too seriously."
	>>> from re import search
	>>> print search(r"l.f.", s)
	<_sre.SRE_Match at 0x10cbc73d8>
	>>> print search(r". . .", s) # no adjacent three single letter words
	None
	
In order for '.' to match '\n' (new line) we need to pass a flag:

	!python
	>>> re.search(r"l...e", "li\nfe", re.DOTALL) 
	<_sre.SRE_Match at 0x10cbc7578>
	
Note: in order to  match the '.' character, prefix it with a backslash ('\.'). This also applies to other symbols of the regex language.
	
---

## Matching a set of characters

	!python
	>>> from re import search
	>>> search(r"[tm]ake", "make")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"[tm]ake", "take")
	<_sre.SRE_Match at 0x10cbc7578>
	
Range of characters

	!python
	>>> search(r"[a-z]ake", "bake")
	<_sre.SRE_Match at 0x10cbc7578>
	
Example ranges: `0-9`, `a-z`, `A-Z`, `a-f`.

Multiple ranges in the same set: `[a-zA-Z]`.

Predefined sets: `\d`: numbers, `\D`: not numbers, `\w`: alphanumeric, `\W`: not alphanumeric, `\s`: whitespace. `\S`: not whitespace. there are many more, look them up!

---

## The inverse of a set of characters

The caret (^) at the start of a set creates an inverse set.

	!python
	>>> from re import search
	>>> search(r"[^t]ake", "make")
	<_sre.SRE_Match at 0x10cbc7578>

---

## Matching at start and end

The caret (^) marks the start of the string. The dollar ($) marks the end.

	!python
	>>> from re import search
	>>> search(r"^bar", "foobar")
	None
	>>> search(r"^foo", "foobar")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"bar$", "foobar")
	<_sre.SRE_Match at 0x10cbc7578>

---

## Optional elements

A symbol followed by a question mark (?) indicates it is optional.

	!python
	>>> from re import search
	>>> search(r"b?oo", "foo")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"b?oo", "boo")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"a[0-9]?", "a2")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"a[0-9]?", "a")
	<_sre.SRE_Match at 0x10cbc7578>
	
---

## Repetition

A symbol followed by a plus sign (+) indicates it can be repeated 1 or more times:

	!python
	>>> from re import search
	>>> search(r"fo+bar", "fooooobar")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"fo+bar", "fbar")
	None

A symbol followed by an asterisk (*) indicates it can be repeated 0 or more times:

	!python
	>>> from re import search
	>>> search(r"fo*bar", "fooooobar")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"fo*bar", "fbar")
	<_sre.SRE_Match at 0x10cbc7578>

---

A specific number of repititions is written as `{n}` where `n` is the number of repetitions:

	!python
	>>> from re import search
	>>> search(r"fo{2}bar", "foobar")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"fo{2}bar", "fooobar")
	None

A minimum and maximum can be specified by seperating them with a comma (`{min,max}`). not specifying minimum means 0, not specfiying maximum means infinite:
	
	!python
	>>> from re import search
	>>> search(r"fo{2,4}bar", "fooobar")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"fo{2,}bar", "foooooobar") # two or more
	<_sre.SRE_Match at 0x10cbc7578>

---

## Logical 'or'

A logical or is a binary operator marked by a pipe ('|'):

	!python
	>>> from re import search
	>>> search(r"^foo$|^bar$", "foobar")
	None
	>>> search(r"^foo$|^bar$", "foo")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"^foo$|^bar$", "bar")
	<_sre.SRE_Match at 0x10cbc7578>

Parenthesis can be used as in regular boolean algebra:
	
	!python
	>>> from re import search
	>>> search(r"(f|b)oo", "foo")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> search(r"(f|b)oo", "boo")
	<_sre.SRE_Match at 0x10cbc7578>

---

## Grouping - capturing parts

A common usage of regex is capturing specific parts of the text. 

Each part is called a subgroup.

The parenthesis are used to mark subgroups:

	!python
	>>> from re import search
	>>> search(r"chapter (\d+)", "chapter 10")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> match = _
	>>> match.groups()
	('10',)
	>>> print match.group(0) # the first group is the whole string
	chapter 10
	>>> print match.group(1)
	10

Note: parenthesis are used both for logical 'or' and for capturing. Luckily there's a non capturing version of parenthesis. an example usage for using `or` without capturing: `(?:a|b)`.

---

## Grouping - naming subgroups

When a single regex has many subgroups it becomes unreadable and uncomfortable to work with (you need to remember the index of the subgroup to get it).

An alternative approach is to name the subgroups:

	!python
	>>> from re import search
	>>> search(r"chapter (?P<chapter>\d+) line (?P<line>\d+)", "chapter 7 line 22")
	<_sre.SRE_Match at 0x10cbc7578>
	>>> match = _
	>>> match.groupdict()
	{'chapter': '7', 'line': '22'}

Note: this is a python extension to the regex standard.

---

## Finding all matches

`findall` returns the list of subgroups captured by each match. if no subgroups we're defined, the list of matched strings are returned.

	!python
	>>> from re import findall
	>>> findall(r"\d+", "123 456 789")
	['123', '456', '789']
	
    >>> findall(r"chapter (\d+) line (\d+)", "chapter 7 line 22\nchapter 8 line 3")
	[('7', '22'), ('8', '3')]
	
There's also a generator version that yields match objects:

	!python
	>>> from re import finditer
	>>> for match in finditer("\d+", "123 456 789"):
	...     print match.group(0)
	123
	456
	789

---

## Substitutions

A common use of regex is to perform rich substitutions.

The `sub` function gets a `repl` (replace) argument that can be a string that replaces the matches:

	!python
	>>> from re import sub
	>>> print sub(pattern='foo', repl='bar', string='foobar')
	barbar

The string can refer to subgroups using `\g<n>` where `n` is the subgroup:

	!python
	>>> print sub(pattern='[0-9a-fA-F]', repl=r'0x\g<0>', string='8a')
	0x8a

`repl` can also be a function that gets a match and returns a string:

	!python
	>>> def inc(match):
	...     return str(int(match.group(0)) + 1)
	>>> print sub(pattern='\d+', repl=inc, string='123 456')
	124 457
	
--- 

## Compilation

Each time a pattern is passed as an argument to `search` or `findall` it is compiled into a `pattern` object. If the same pattern is used over and over again, performance can be improved by compiling the pattern before hand:

	!python
	>>> number_pattern = re.compile("\d+")
	>>> number_pattern.findall("123 456 789")
	["123", "456", "789"]

---

## Exercise 1

`get_domain` verifies an email address and returns the domain part of it.

	!python
	>>> print get_domain("bill")
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    ValueError: Invalid regex
	
	>>> print get_domain("bill@domain") # must have a '.'!
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
    ValueError: Invalid regex
	
	>>> print get_domain("bill@domain.com")
	domain.com

---
	
## Exercise 2 

`replace_with_bob` replaces all words that start with a 'k' with 'bob'.

	!python
	>>> print replace_with_bob("A knight with a knife")
	A bob with a bob

## Exercise 3

`capitalize` replaces all sentences 

	!python
	>>> print capitalize("""sentences are seperated by dots.
	                        don't forget the first sentence.
							the last sentence might not end with a dot.")
	Sentences are seperated by dots. 
	Don't forget the first sentence.
	The last sentence might not end with a dot.
