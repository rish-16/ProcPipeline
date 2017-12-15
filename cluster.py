import csv
from pprint import pprint
import numpy as np
import sys
import itertools
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from tfidf import get_result
# sys.setdefaultencoding('UTF8')

R = open('data.txt', 'r').read()
R = R.split('\n')
y = []
C = R
temp_array = []
unsorted = []

sim_sum_total = 0
original = 0
array_counter = 0

G = globals()

tolerance = 0.40
# Optimal: 0.35

# ------------------------------------------ CLUSTERING ------------------------------------------

try:
	for r in range(len(R)-1):
		for c in range(len(C)-1):

			if r != c and c != r:
				similarity = get_result(R[r].lower(), C[c].lower())
				if (similarity > float(tolerance)):
					print ('{} and {} = {}'.format(r, c, similarity))
					print ('')
					print ('')

					temp = ""
					temp = C[c]
					temp_array.append(temp)
					sim_sum_total += 1
					sim_sum_total = sim_sum_total - original

		G['container_{}'.format(r)] = []

		if (sim_sum_total > 0):

			array_counter = 1

			if len(temp_array) > 1:
				G['container_{}'.format(r)].append(temp_array)
				temp_array = []
				y.append([G['container_{}'.format(r)]])
			else:
				unsorted.append([G['container_{}'.format(r)]])

			print ('Similar feedback for BATCH {} = {}'.format(r, sim_sum_total))
			sim_sum_total = original

		elif (sim_sum_total < 0):
			array_counter = 0

except:
	pass

# ------------------------------------------ DATA PROCESSING SUMMARY ------------------------------------------

print ('')
print ('')
print ('Sample Instance size: {}'.format(len(R)))
print ('Sorted bucket: {}'.format(len(y)))
print ('Unsorted bucket: {}'.format(len(unsorted)))

y = np.array(y)
y = y.reshape([y.shape[0],])
class_labels = []
index = 0

for cluster in y:
	current = []
	for feedback in cluster:
		current.append(index)

	index += 1
	class_labels.append(current)

class_labels = np.array(class_labels)
class_labels = class_labels.reshape([class_labels.shape[0]])

ffile = []
cfile = []

with open('feedbacks.txt', 'a') as ftxt:
	for cluster in y:
		for feedback in cluster:
			ftxt.write('{}'.format(feedback))

with open('classes.txt', 'a') as ctxt:
	for cluster in class_labels:
		for class_label in cluster:
			ctxt.write('{}\n'.format(class_label))
