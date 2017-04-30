# -*- coding: utf-8 -*-
from util import *
import os
import csv
import re
from pprint import pprint 

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

def read_aspect_review( datadir_path ):
	filename = os.path.join( datadir_path, 'aspect_review.txt')
	data = list()
	with open(filename ,'r') as f_in:
		for i in range(200):
			row = dict()
			ID = f_in.readline()
			review = f_in.readline().replace('\n', '')
			pos = f_in.readline().split()
			neg = f_in.readline().split()
			row['review'] = review
			row['pos'] = pos
			row['neg'] = neg
			data.append(row)
	#print(str(data).decode('string_escape'))
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

def train_predict( aspect_review, aspect_term, str_pos, str_neg ):
	aspects = ['服務', '環境', '價格', '交通', '餐廳']
	for entry in aspect_review:
		review = entry['review']	
		print review
		sentences = list()
		for i in review.split('，'):
			for j in review.split('。'):
				for k in review.split(','):
					sentences.append(k)

		for aspect in aspects:
			have_answer = False
			for sentence in sentences:
				if any( noun in sentence for noun in aspect_term[ aspect ]):
					if any( phrase in sentence for phrase in str_pos ):
						print aspect, 1
						have_answer = True
						break
				elif any( noun in sentence for noun in aspect_term[ aspect ]):
					if any( phrase in sentence for phrase in str_neg ):
						print aspect, -1
						have_answer = True
						break
			if not have_answer:
				print aspect, 0
		print str(entry['pos']).decode('string_escape')
		print str(entry['neg']).decode('string_escape')
		print '**********************************'
		print
	
		

def main():
	test_csv = read_test_csv( DATADIR_PATH )
	test_review = read_test_review( DATADIR_PATH )
	aspect_term = read_aspect_term( DATADIR_PATH)
	str_pos = read_NTUSD_pos( DATADIR_PATH )
	str_neg = read_NTUSD_neg( DATADIR_PATH )
	aspect_review = read_aspect_review( DATADIR_PATH )	
	#baseline_predict( test_csv, test_review, aspect_term, str_pos, str_neg )
	train_predict(aspect_review, aspect_term, str_pos, str_neg)

if __name__ == '__main__':
	main()
