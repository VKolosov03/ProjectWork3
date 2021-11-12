import os
import timeit

test1 = """
with open('number.txt', 'r') as open_file:
	text_file=open_file.readlines()
	numb=0
	for j in text_file:
		if j.strip().isdigit():
			numb+=int(j.strip().isdigit())
"""

time1 = timeit.timeit(test1, number=10)
print(time1)

test2 = """
with open('number.txt', 'r') as open_file:
	numb=0
	for i in open_file:
		numb+=int(i.strip().isdigit())
"""

time2 = timeit.timeit(test2, number=10)
print(time2)

test3 = """
with open('number.txt', 'r') as open_file:
	numb=sum(int(i.strip().isdigit()) for i in open_file if i.strip().isdigit())
"""

time3 = timeit.timeit(test3, number=10)
print(time3)

