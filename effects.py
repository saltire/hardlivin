import csv
import itertools

files = ['Art Show Game Square Write Ups.txt', 'square-effects.txt']
fields = 

lines = []
for fn in files:
	with open(fn, 'rb') as f:
		lines.extend([line.strip() for line in f.readlines()])
	
groups = [list(g) for k, g in itertools.groupby(lines, lambda v: v != '') if k]

with open('hardlivin/data/info.csv', 'rb') as c:
	info = {line[0]: line[1:] for line in csv.reader(c)}
	
for title, desc, effect, difficulty in groups:
	if title in info:
		info[title] = 
	info.setdefault(

		
	

with open('hardlivin/data/info.csv', 'wb') as c:
	writer = csv.writer(c)
	for group in groups:
		writer.writerow(group)
		