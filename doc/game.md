# Game of life

---

## The rules

1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

---

## First session 

Implement it!

1. What is the type of the matrix?
2. Can the size of the matrix be passed as an argument?
3. Did you start from the top (printing to screen) or bottom (game rules)?
4. If you have a bug in the rules of the game, can you write a unittest to show it? are the rules independent code?

---

## Second session

Test first!

1. Do you trust your code more?
2. Did it take a lot longer?

---
	
## Third session

3 dimensional.
More object oriented.
3 lines per method.

---

## Fourth session

No if statements! (can be done using inheritence).

---

## Roman Numerals

	Symbol	Value
	I	    1
	V	    5
	X	    10
	L	    50
	C	    100
	D	    500
	M	    1,000

Counting to 10: I, II, III, IV, V, VI, VII, VIII, IX, and X

These Roman numbers are formed by combining symbols together and adding the values. 

For example, MMVI is 1000 + 1000 + 5 + 1 = 2006. 

Generally, symbols are placed in order of value, starting with the largest values. 

When smaller values precede larger values, the smaller values are subtracted from the larger values, and the result is added to the total. 

For example MCMXLIV = 1000 + (1000 − 100) + (50 − 10) + (5 − 1) = 1944.

Implement `toroman` that gets a number and returns a string.
