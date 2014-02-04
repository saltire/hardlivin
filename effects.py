import csv
import itertools


with open('Art Show Game Square Write Ups.txt', 'rb') as f:
	lines = [line.strip() for line in f.readlines()]
with open('square-effects.txt', 'rb') as f:
	lines.extend([line.strip() for line in f.readlines()])
	
groups = groups = [list(g) for k, g in itertools.groupby(lines, lambda v: v != '') if k]

with open('info.csv', 'wb') as c:
	writer = csv.writer(c)
	for group in groups:
		writer.writerow(group)
		