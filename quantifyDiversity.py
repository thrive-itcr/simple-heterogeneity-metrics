import numpy as np
from scipy.cluster.vq import kmeans2
#import matplotlib.pyplot as plot

def phenotypeCells(feats,nSpecies=4,nIter=100):
	'''
	input: feature vector
	options: # of species, # of kmeans iterations
	output: centroids of k means clusters, label for each feat
	'''

	# TO DO: allow discovery of ideal nSpecies
	# TO DO: optional visualization(?)

	centroid, label = kmeans2(feats,nSpecies,iter=nIter,minit='random')
	return centroid,label

def quantifyDiversity(phenos,simMat='default', metric='QE'):
	'''
	inputs: phenotype vector
	options: similarity matrix flag, metric flag
	outputs: heterogeneity value
	'''

	# Cast phenotype vector to numpy array if list
	# Grab number of species from phenotype vector
	phenos = np.asarray(phenos)
	nSpecies = max(np.size(np.unique(phenos)),np.max(phenos)+1)


	# Set sensitivity parameter, q
	# TO DO: set q accordingly for other metrics (only works for QE now)
	if metric == 'QE':
		q = 2
	elif metric == 'Shannon' or metric == 'shannon':
		q = 2
	elif metric == 'Simpson' or metric == 'simpson':
		q = 2
	else:
		print "invalid metric"


	# Construct similarity matrix, Z
	# TO DO: accept user defined similarity matrix and test validity
	# TO DO: make sure on 0 to 1 scale, use exp transform if on 0 to inf scale.
	# TO DO: test matrix properties. NOTE: need not be symmetric!
	if simMat == 'default':
		Z = np.zeros(shape=(nSpecies,nSpecies))
		minVal = 0.25 #0
		for r in range(0,nSpecies):
			for c in range(0,nSpecies):
				Z[r,c] = r-c
		Z = np.abs(Z)
		Z = Z / (np.max(Z)/(1.0-minVal))
		Z = 1.0 - Z
	elif simMat == 'identity':
		Z = np.ones(shape=(nSpecies,nSpecies))
	else:
		print "error in defining similarity matrix, Z"


	# Construct relative abundance vector, p
	# Assumes phenos are listed 0 -> nSpecies-1
	p = np.zeros(nSpecies,dtype='float')
	for n in range(0,len(phenos)):
		s = phenos[n]
		p[s] = p[s] + 1.0
	p = p / np.sum(p)
	#print p

	# Compute relative abundance of species similar to the ith, Zp_i
	# for each i
	Zp = np.zeros(nSpecies,dtype='float')
	for i in range(0,nSpecies):
		for j in range(0,nSpecies):
			Zp[i] = Zp[i] + (Z[i,j] * p[j])


	# Compute diversity of order q, D(p)	
	D = 0
	if q != 1 and q != float('inf'):
		for i in range(0,nSpecies):
			if Zp[i] == 0:
				continue
			D = D + ( p[i] * np.power(Zp[i], (q-1)) )
		D = np.power( D, (1.0 / (1-q)) )
	elif q == 1:
		denom = 1
		for s in range(0,nSpecies):
			if Zp[i] == 0:
				continue
			denom = denom * np.power(Zp[i], p[i])
		D = 1.0 / denom
	elif q == float('inf'):
		D = 1.0 / np.max(Zp)
	else:
		print "error in defining sensitivity parameter, q"


	# Compute entropy of order q, H(p)
	H = 0
	if q != 1:
		H = (1.0 / (q-1)) * ( 1 - np.power(D, (1-q)) )
	elif q == 1:
		H = np.log(D)
	else:
		print "error in defining sensitivity paramter, q"


	# Return diversity metric
	# TO DO: set diversity accordingly for other metrics
	diversity = 0
	if metric == 'QE':
		diversity = H
	else:
		print "invalid metric"
		diversity = D

	return diversity
