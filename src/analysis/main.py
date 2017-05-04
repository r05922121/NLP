# -*- coding: utf-8 -*-
from util import *
import os
import csv
import re
import jieba
import pickle as pk
from pprint import pprint 

BASEDIR = '../../'
DATADIR_PATH=os.path.join( BASEDIR, 'data/' )
jieba.set_dictionary('../../data/dict.txt.big')
BUILD_DICT_OR_NOT = False
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
			for i in range(1,len(row)):
				texts.append(row[i].decode('utf-8'))
				#texts.append(row[i])
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


### Build a dict with a word_segment and a score
# postive value for pos
# negative value for neg

# input : datadir_path : data path contain polarity_review.txt
# 		  build_dict_or_not : load pre-saved 
# return : dict_all
def read_polarity_review( datadir_path, build_dict_or_not):
	if build_dict_or_not:
		filename = os.path.join( datadir_path, 'polarity_review.txt' )
		data = list()
		dict_all = dict()
		count = 0
		total_point = 0
		with open( filename, 'r' ) as f_in:
			for line in f_in:
				count += 1
				row = line.split()
				point = int(row[0])
				if point < 0:
					point *= 1.266
				text = row[1]
				words = jieba.cut(text, cut_all=False) 
				for word in words:
					if word in dict_all:
						dict_all[ word ] += point
					else:
						dict_all[word] = point
				print count
		with open('dict_all.pk', 'w') as f_out:
			pk.dump(dict_all, f_out)
		print str(dict_all).decode('string_escape')
		return dict_all
	else:
		with open('dict_all.pk', 'r') as f_in:
			return pk.load(f_in)	
			
### remove no-effect adv like very, super ...(In Chinese)
def remove_adv( datadir_path, dict_all ):
	filename = os.path.join( datadir_path, 'adv.txt')
	with open( filename, 'r' ) as f_in:
		data = f_in.readline().split()
	for word in data:
		dict_all[ word.decode('utf-8') ] = 0
	return dict_all

### main predict function
def jieba_dict_predict( test_csv, test_review, aspect_term, str_pos, str_neg, dict_all):
	print 'Id,Label'
	for test_entry in test_csv:
		entry_id = test_entry['Id']
		aspect = test_entry['Aspect']
		review_id = test_entry['Review_id']

		article = test_review[ review_id ]
		#print '**** DEBUG ****'
		#print article
		#print aspect
		sentences = list()
		for i in article.split('，'):
			for j in i.split('。'):
				for k in j.split(','):
					for m in k.split(' '):
						sentences.append(m) 
				
		have_answer = False
		score = 0
		
		for sentence in sentences:
			sentence = sentence.decode('utf-8')
			if any( noun in sentence for noun in aspect_term[ aspect ]):
				words = jieba.cut(sentence, cut_all=False)
				#print sentence.encode('utf-8')
				for word in words:
					if word in aspect_term[ aspect ]:
						continue
					if word in dict_all:
						score += dict_all[word]
					else:
						score += 0
		if score > 0:
			print str(entry_id)+',1'
		elif score < 0:
			print str(entry_id)+',-1'
		else:
			print str(entry_id)+',0'

				#print aspect, sentence
				#if any( phrase in sentence for phrase in str_neg ):
				#	print str(entry_id)+',-1'
				#	have_answer = True
				#	break
				#if any( phrase in sentence for phrase in str_pos ):
				#	print str(entry_id)+',1'
				#	have_answer = True
				#	break
		#if not have_answer:
		#	print str(entry_id)+',0'

''' for validation use.
def train_predict( aspect_review, aspect_term, str_pos, str_neg ):
	aspects = ['服務', '環境', '價格', '交通', '餐廳']
	for entry in aspect_review:
		review = entry['review']	
		print review
		sentences = list()
		for i in review.split('，'):
			for j in i.split('。'):
				for k in j.split(','):
					sentences.append(k)

		for aspect in aspects:
			have_answer = False
			for sentence in sentences:
				if any( noun in sentence for noun in aspect_term[ aspect ]):
					if any( phrase in sentence for phrase in str_pos ):
						print sentence, aspect, 1
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
'''	
		

def main():
	test_csv = read_test_csv( DATADIR_PATH )
	test_review = read_test_review( DATADIR_PATH )
	aspect_term = read_aspect_term( DATADIR_PATH)
	str_pos = read_NTUSD_pos( DATADIR_PATH )
	str_neg = read_NTUSD_neg( DATADIR_PATH )
	aspect_review = read_aspect_review( DATADIR_PATH )	
	#baseline_predict( test_csv, test_review, aspect_term, str_pos, str_neg )
	#train_predict(aspect_review, aspect_term, str_pos, str_neg)
	dict_all = read_polarity_review( DATADIR_PATH, BUILD_DICT_OR_NOT )
	dict_all = remove_adv( DATADIR_PATH, dict_all )
	jieba_dict_predict( test_csv, test_review, aspect_term, str_pos, str_neg, dict_all)

if __name__ == '__main__':
	main()
