import sys
import pickle as pk
with open('dict_all.pk', 'r') as f_in:
	data = pk.load(f_in)

#for entry in data:
#	print entry, data[entry]
#print str(data).decode('string_escape')
search = sys.argv[1].decode('utf-8')
print search
#print data
#for entry in data:
#	print entry
print data[ search ]
