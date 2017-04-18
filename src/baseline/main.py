# -*- coding: utf-8 -*-
from util import *
import os
import csv
import re

BASEDIR = '../../'
DATADIR_PATH=os.path.join( BASEDIR, 'data/' )

### read test.csv
### return a list of dict.
### a dict contain 3 dim: 'Id', 'Aspect', 'Review_id'
def read_test_csv( datadir_path ):
	filename = os.path.join( datadir_path, 'test.csv')
	data = list()

	with open( filename, 'r' ) as f_in:
		content = csv.DictReader(f_in)
		for row in content:
			data.append(row)
	return data

### read test_review.txt
### return a dict which key=number, value=text
def read_test_review( datadir_path ):
	filename = os.path.join( datadir_path, 'test_review.txt' )
	
	content = dict()
	with open(filename, 'r') as f_in:
		while(1):
			number = f_in.readline().replace('\n', '')
			if not number:
				break
			text = f_in.readline().replace('\n','')
			content[number] = text
	return content

### read aspect_term.txt
### return a dict of list
def read_aspect_term( datadir_path ):
	filename = os.path.join( datadir_path, 'aspect_term.txt' )
	
	data = dict()
	with open( filename, 'r') as f_in:
		for line in f_in:
			row = line.split()
			texts = list()
			for i in range(1,):
				texts.append(row[i])
			data[ row[0] ] = texts
	return data

### a list of positive word
def read_NTUSD_pos( datadir_path ):
	filename = os.path.join( datadir_path, 'NTUSD_pos.txt' )
	data = list()
	with open( filename, 'r' ) as f_in:
		for line in f_in:
			data.append(line.replace('\n', '').replace('\r',''))
	return data

### a list of negative word
def read_NTUSD_neg( datadir_path ):
	filename = os.path.join( datadir_path, 'NTUSD_neg.txt' )
	data = list()
	with open( filename, 'r' ) as f_in:
		for line in f_in:
			data.append(line.replace('\n', '').replace('\r',''))
	return data


def baseline_predict( test_csv, test_review, aspect_term, str_pos, str_neg ):
	print 'Id,Label'
	for test_entry in test_csv:
		entry_id = test_entry['Id']
		aspect = test_entry['Aspect']
		review_id = test_entry['Review_id']

		article = test_review[ review_id ]
		sentences = list()
		for i in article.split('，'):
			for j in i.split('。'):
				for k in j.split(','):
					sentences.append(k) 
				

		have_answer = False
		for sentence in sentences:
			if any( noun in sentence for noun in aspect_term[ aspect ]):
				#print aspect, sentence
				if any( phrase in sentence for phrase in str_pos ):
					print str(entry_id)+',1'
					have_answer = True
					break
				elif any( phrase in sentence for phrase in str_neg ):
					print str(entry_id)+',-1'
					have_answer = True
					break
		if not have_answer:
			print str(entry_id)+',0'

		

def main():
	test_csv = read_test_csv( DATADIR_PATH )
	test_review = read_test_review( DATADIR_PATH )
	aspect_term = read_aspect_term( DATADIR_PATH)
	str_pos = read_NTUSD_pos( DATADIR_PATH )
	str_neg = read_NTUSD_neg( DATADIR_PATH )
	baseline_predict( test_csv, test_review, aspect_term, str_pos, str_neg )

if __name__ == '__main__':
	main()
