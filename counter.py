from collections import Counter
import csv
import re

cols = ['title', 'desc', 'effect', 'difficulty', 'column', 'row', 'locked']

with open('hardlivin/data/info.csv', 'rb') as c:
	info = csv.DictReader(c, cols)
	
	#print Counter(line['difficulty'] for line in info)
	
	patterns = {'vigour': '[+-]\dV',
				'gumption': '[+-]\dG',
				'deeds': '[+-]\dD',
				
				}
	print Counter(stat for line in info for stat, pattern in patterns.iteritems()
				  if re.search(pattern, line['effect']) is not None)