import numpy as np
import cv2
import os

def drawDiversityOverlay(fin,xy,colors,fout=''):

	# Set scale to 0-255 not 0-1
	if np.max(colors) <= 1:
		colors = colors * 255

	# Create file name
	if len(fout) == 0:
		nm,ext = os.path.splitext(os.path.basename(fin))
		newName = nm + '_diversity.tif'
		fout = os.path.join(os.path.dirname(fin), newName)

	
	# Create blank BGRA image
	im = np.zeros((2000, 2000, 4), dtype=np.uint8)


	# Modify color vector to have alpha channel, switch RGBA to BGRA
	alp = np.ones(np.shape(colors)[0]) * 255
	colors = cv2.merge((colors[:,2], colors[:,1], colors[:,0], alp))
	colors = colors.astype(int)


	# Draw circles 
	for i in range(0, np.shape(colors)[0]):
		cv2.circle(im, tuple(xy[i,:].astype(int)), 13, tuple(colors[i,:,:][0]),thickness=-1)


	# Save image as fout name
	cv2.imwrite(fout,im)
	cv2.destroyAllWindows()
