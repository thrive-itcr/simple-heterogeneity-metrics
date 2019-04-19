import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.vq import kmeans2
from quantifyDiversity import *
import matplotlib.pyplot as plot

def getColors(vals,colormap,vmin=None,vmax=None):
	norm = plot.Normalize(vmin,vmax)
	return colormap(norm(vals))

def diversityHeatmap(xy,feats,maxRange=200,nSpecies=4,simMat='default',metric='QE'):
	'''
	inputs: centroid matrix, feature vector
	options: microdomain range, # of species, similarity matrix flag, metric flag
	outputs: heat vector, color vector
	'''

	# Precompute k-means clustering (phenotyping) labels for all cells
	# TO DO: allow for automated # of species discovery
	centroid,label = phenotypeCells(feats,4,100)


	# Precompute cell connections within microdomain range
	I = squareform(pdist(xy))
	

	# Execute for each cell
	heat = np.zeros_like(feats)
	for cell in range(0,np.shape(xy)[0]):

		# Extract neighbors within microdomain range
		Ic = I[cell,:]
		Ir = np.where(Ic < maxRange)[0]

		# Set heat to 0 if cell has no neighbors in range
		if np.size(Ir) == 0:
			heat[cell] = 0
			continue

		# Extract phenotype values
		lab_r = label[Ir]

		# Calculate diversity metric and save
		diversity = quantifyDiversity(lab_r,'default',metric)
		heat[cell] = diversity

	# convert diversity metric vector to color (3D) vector
	colors = getColors(heat, plot.cm.jet)
	#print('diversityHeatmap, colors:')
	#print(colors)


	return heat, colors
