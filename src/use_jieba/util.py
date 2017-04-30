# -*- coding: utf-8 -*-
import sys
import os

def read_file( input_path ):
	with open(input_path, 'r') as f_in:
		data = f_in.read()
	return data
