import os
import numpy as np
from random import randint

def listdir_nohidden(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			yield f

def structureData(path,xy_ind=1,feat_ind=5,log_flag='1'):
	'''
	inputs: string containing location and name of csv file(s)
	options: give xy start index, feature index, log flag
	outputs: numpy array of expression and centroid data
	'''

	# Grab individual directory and filename components
	fold = os.path.dirname(path)
	base = os.path.basename(path)


	# Construct full file name
	# TO DO: allow processing of all files in path (save in nd array?)
	if len(base) is 0:
		file_list = list(listdir_nohidden(fold))
		base = file_list[randint(0,len(file_list)-1)]
	fname = os.path.join(fold,base)
	

	# Load data
	# TO DO: make data class(?), assign column types through regex(?)
	data = np.loadtxt(fname,dtype=float,delimiter=',',skiprows=1)
	xy = data[:,xy_ind:(xy_ind+2)]
	feat = data[:,feat_ind]


	# Perform log transform
	# TO DO: more rigorous log transform test(?)
	log_flag = str(log_flag)
	if log_flag == '1' or log_flag[0].lower() == 'y':
		feat = np.log(feat)

	
	# Return centroid and features
	return xy, feat
	
	
