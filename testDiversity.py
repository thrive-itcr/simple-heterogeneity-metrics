import numpy as np
import matplotlib.pyplot as plot
from structureData import *
from quantifyDiversity import *

def testDiversity():
	fname = '/home/dms167/Documents/research/I3TH/quant_output/testOut3.csv'
	#fname = '/home/dms167/Documents/research/I3TH/quan/quan_021.csv'

	#5=CD68,9=CD8,13=CD3,17=DAPI,21=CD20,25=NaK,29=Ecad
	xy, feat = structureData(fname,1,5,'1') 
	print feat

	nTest = 100
	divs = np.zeros(nTest)
	for i in range(0,nTest):
		_, specs = phenotypeCells(feat,4,100)
		di = quantifyDiversity(specs,'default','QE')
		divs[i] = di
	print "median value is ", np.median(divs)

	hist,bins = np.histogram(divs,bins = 11)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plot.bar(center,hist.astype(float)/np.sum(hist),align='center',width=width)
	plot.title('median QE = %f'%np.median(divs))
	plot.show()

if __name__ == '__main__':
	testDiversity()
