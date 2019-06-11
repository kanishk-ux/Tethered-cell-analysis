'''
	File for all the image processing required in the program.
	Contains 3 functions to be called as required:
		threshold: Used for thresholding all frames using python image processing library cv2 (OpenCV)
		click_and_crop: Used to enable the user to select a cell in the GUI window
		crop: Allows user to select a free-size rectangular portion of the first frame consisting of a cell for furthur analysis
'''
import numpy
import matplotlib.pyplot as plt
from sklearn import linear_model
import cv2
import math
import utilities

#defining variables for future use
image = []
refPt = []
trace = []
cropping = False

def threshold(img):
	'''
		Used for thresholding all frames using python image processing library cv2 (OpenCV)
		Input: img (Image taken as input from file)
	'''

	images = []		#defining image array
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	#convert image to black and white using cv2

	kernel = numpy.ones((3, 3), numpy.float32) / 9	#takes a 3X3 brush matrix to blur the image 

	avg_color_per_row = numpy.average(gray, axis=0)	 	#calculates average colour per row 
	avg_color = numpy.average(avg_color_per_row, axis=0)	#average colour

	if(int(avg_color) == 0):
		avg_color = 1

	ret, thresh = cv2.threshold(gray, avg_color - 1, 255, cv2.THRESH_BINARY)	#calling thresholding function of cv2 library
	binary1 = thresh
	thresh = cv2.filter2D(thresh, -1, kernel)		#calling filter2D function of cv2 library
	smooth = thresh 								#smoothening the image
	avg_color_per_row = numpy.average(thresh, axis=0)	#calculating average colour per row
	avg_color = numpy.average(avg_color_per_row, axis=0)	#calculating average colour
	ret, thresh = cv2.threshold(thresh, avg_color, 255, cv2.THRESH_BINARY)	#calling threshold function of cv2 library
	thresh1 = cv2.medianBlur(thresh, 7)		#calling medianBlur function of cv2 library
	binary2 = thresh
	thresh = cv2.dilate(thresh, kernel, iterations=1)	#calling dilate fuction of cv2 library
	return thresh1

def click_and_crop(event, x, y, flags, param):
	'''
		Used to enable the user to select a cell in the GUI window
		Called inside the crop function
		Triggered when the right mouse button is clicked and ends when the left mouse button is clicked
		Stores the chosen coordinates in global variable refPt
		Inputs: event,x,y,flags,param
	'''

	# grab references to the global variables
	global refPt, cropping,image
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False

		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)


def crop():
	'''
		Allows user to select a free-size rectangular portion of the first frame consisting of a cell for furthur analysis
	'''

	meta = utilities.meta
	filename = utilities.filename			#calling filename from utilities file
	folder_path = utilities.folder_path		#calling folder_path from utilities file
	global image,trace,refPt       			#defining global variables
	addr = folder_path + '/img_000000'		#defining address
	ad = '_Default_000.tif'
	print ('crop cell for analysis.....')
	print ('Press c to proceed after cropping')
	print ('Press r to redo')
	if meta == 1:							#case when metadata is present
		frame = addr + '000' + ad
	else:									#case when metadata is not present
		frame = folder_path + filename
	# load the image, clone it, and setup the mouse callback function
	image = cv2.imread(frame)				#calling imread function of cv2
	image = threshold(image)
	clone = image.copy()
	cv2.namedWindow("image")				#calling namedWindow function of cv2
	cv2.setMouseCallback("image", click_and_crop)	#calling setMouseCallback function of cv2

	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF

		# if the 'r' key is pressed, reset the cropping region
		if key == ord("r"):
			image = clone.copy()

		# if the 'c' key is pressed, break from the loop
		elif key == ord("c"):
			break

	# if there are two reference points, then crop the region of interest
	# from teh image and display it

	# close all open windows
	cv2.destroyAllWindows()

	a = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	trace = numpy.zeros((a.shape[0],a.shape[1]), numpy.uint8)	#output trace
