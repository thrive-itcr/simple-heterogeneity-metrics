import string
import os
import numpy as np

def diversity2csv(prefix, fin,fout,heat,colors=None):
	'''
	input: input file, heat vector, color matrix
	output: none, writes an file as fout
	'''

	# Handle no color input.  TODO:  The test below does not work if colors is not None.
	#if colors == None:
	#	colors = np.zeros((np.size(heat),3))


	# Package together heat and colors
	#print('In diversity2csv, heat:')
	#print(heat)
	#print(type(heat))
	#print('colors:')
	#print(colors)
	#print(type(colors))
	newCols = np.concatenate((heat[:,None],colors),axis=1)
	colNames = [prefix+'-Diversity',prefix+'-R',prefix+'-G',prefix+'-B',prefix+'-color4']
	#print('diversity2csv, colNames:')
	#print(colNames)


	# Create output file name
	#nm, ext  = os.path.splitext(os.path.basename(fin))
	#newName = nm + '_diversity' + ext
	#fout = os.path.join(os.path.dirname(fin), newName)


	# Open input and output files
	fi = open(fin,'r')
	fo = open(fout,'w')


	# Convert new columns into string array
	nC = np.array(["%f" % x for x in newCols.reshape(newCols.size)])
	nC = nC.reshape(newCols.shape)
	#print('diversity2csv, nC:')
	#print(nC)

	
	# Write new header
	hdr = fi.readline().rstrip()
	hdr = hdr + ',' + string.join(colNames,',') + '\r\n'
	fo.write(hdr)
	#print('diversity2csv, hdr:')
	#print(hdr)

	# Write new data files
	i  = 0
	for line in fi.readlines():
		if i==0:
			pass
			#print('diversity2csv, first line read:')
			#print(line)
		newLine = nC[i,:]
		if i==0:
			pass
			#print('diversity2csv, first newLine:')
			#print(newLine)
			#print('diversity2csv, first line written to file:')
			#print(line.rstrip() + ',' + string.join(newLine,',') + '\r\n')
		fo.write(line.rstrip() + ',' + string.join(newLine,',') + '\r\n')
		i+=1

	fi.close()
	fo.close()
