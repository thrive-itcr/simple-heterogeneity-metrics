import string
import os
import numpy as np

def diversity2csv(fin,heat,colors=None):
	'''
	input: input file, heat vector, color matrix
	output: none, writes an file as fout
	'''

	# Handle no color input
	if colors == None:
		colors = np.zeros((np.size(heat),3))


	# Package together heat and colors
	newCols = np.concatenate((heat[:,None],colors),axis=1)
	colNames = ['Diversity','R','G','B']


	# Create output file name
	nm, ext  = os.path.splitext(os.path.basename(fin))
	newName = nm + '_diversity' + ext
	fout = os.path.join(os.path.dirname(fin), newName)


	# Open input and output files
	fi = open(fin,'r')
	fo = open(fout,'w')


	# Convert new columns into string array
	nC = np.array(["%f" % x for x in newCols.reshape(newCols.size)])
	nC = nC.reshape(newCols.shape)

	
	# Write new header
	hdr = fi.readline().rstrip()
	hdr = hdr + ',' + string.join(colNames,',') + '\r\n'
	fo.write(hdr)


	# Write new data files
	i  = 0
	for line in fi.readlines():
		newLine = nC[i,:]
		fo.write(line.rstrip() + ',' + string.join(newLine,',') + '\r\n')
		i+=1

	fi.close()
	fo.close()
