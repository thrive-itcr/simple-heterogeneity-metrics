import numpy as np
import matplotlib.pyplot as plot
import cv2
from structureData import *
from quantifyDiversity import *
from diversityHeatmap import *
from diversity2csv import *
from drawDiversityOverlay import *

def testOverlay():
	fname = '/home/dms167/Documents/research/I3TH/test/055_Quant.csv'
	
	xy, feat = structureData(fname,1,9) # 9 is ER_NUC
	heat, colors = diversityHeatmap(xy,feat, 200,4,'default','QE')
	
	drawDiversityOverlay(fname,xy,colors)
	

def testMap():
	imname = '/home/dms167/Documents/research/I3TH/test/055_DAPI.tif'
	fname = '/home/dms167/Documents/research/I3TH/test/055_Quant.csv'

	xy, feat = structureData(fname,1,9) # 9 is ER_NUC
	heat, colors = diversityHeatmap(xy,feat, 200,4,'default','QE')
	colors = colors * 255
	#im = cv2.imread(imname,-1)
	im = cv2.imread(imname) #for some reason removing -1 works

	for i in range(0, np.size(heat)):
	#for i in range(0, 20):
		cv2.circle(im, tuple(xy[i,:].astype(int)), 13, tuple(colors[i,:].astype(int)),thickness=-1)

	cv2.namedWindow('055',cv2.WINDOW_NORMAL)
	cv2.imshow('055',im)
	cv2.resizeWindow('055', 600, 600)
	cv2.waitKey()
	cv2.imwrite('ex_055.png',im)
	cv2.destroyAllWindows()


def testHeat():
	# Define input CSV
	fname = '/home/dms167/Documents/research/I3TH/test/055_Quant.csv'

	# Extract cell centroids and feature
	xy, feat = structureData(fname,1,9,'1') # 9 is ER_NUC

	# Compute diversity and color for each cell
	heat, colors = diversityHeatmap(xy,feat,200,4,'default','QE')

	# Write output
	diversity2csv(fname, heat, colors)

	# Display overall diversity histogram
	print "min heat is %0.3f, max heat is %0.3f" %(np.min(heat), np.max(heat))
	hist,bins = np.histogram(heat,bins = 11)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plot.bar(center,hist.astype(float)/np.sum(hist),align='center',width=width)
	plot.title('median QE = %0.3f' % np.median(heat))
	plot.show()

if __name__ == '__main__':
	#testHeat()
	testMap()
	#testOverlay()
