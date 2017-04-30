# -*- coding: utf-8 -*-
import jieba
import sys

if len(sys.argv) < 2:
	str1 = '請多輸入一組參數'.decode('utf-8').encode('utf-8')
else:
	str1 = sys.argv[1].decode('utf-8').encode('utf-8')
jieba.set_dictionary('../../data/dict.txt.big')
seg_list = jieba.cut(str1, cut_all=False)

#print ", ".join(seg_list)
print('Full mode: ' + "/ ".join(seg_list))

