'''
	Contains 2 primary 
		analyze: Performs Linear Regression Analysis the cropped portion of all the frames and outputs the
				 centre of mass(COM) data for and a plot of COM for furthur use
		compute: Calculates frequency, change in angle per frame, total clockwise/counter-clockwise time 
				interval and no of frames and all else necessary outputs. Also outputs the finally analyzed 
				data in the form of CSV files and graphs

'''

import cv2
import numpy
import imgpros
from sklearn import linear_model
import math
import matplotlib.pyplot as plt
import csv
import utilities

#defining variables
slopes = []
tracedia =[]
lens = []
xcomlist2 = []
ycomlist2 = []
xcomlist = []
ycomlist = []
angles = []


def analyze():
	'''
		Calculates the slope of the regression line of the cropped region for each frame after thresholding 
		which is used by the compute function to calculate the change in angle per frame and the angular frequency.
		Also calculates the diameter of the least fitting circle of the trace of the rotating cell which gives
		us the length of the cell Other calculations include xcom and ycom of the the thresholded cell for each frame
	'''
	
	count = 0

	#importing required variables from previous corresponding files
	meta = utilities.meta
	filename = utilities.filename
	folder_path = utilities.folder_path
	num_frames = utilities.num_frames
	delay = utilities.delay
	refPt = imgpros.refPt
	trace = imgpros.trace
	out_folder = utilities.out_folder

	global slopes,lens,tracedia,xcomlist2,ycomlist2,xcomlist,ycomlist 	#defining global variales
	prev_a = 0
	addr = folder_path + '/img_000000'
	ad = '_Default_000.tif'
	while (count<num_frames):		#looping over all frames
		if meta == 0:				#when metadata is not availbale
			frame = cv2.imread(folder_path + filename.replace("00000",str("%05d" % count)))
		else:						#when metadata is available
			frame = cv2.imread(addr+ str("%03d" % count)+ad)
		frame = imgpros.threshold(frame)
		orgimg= frame.copy()
		cv2.rectangle(orgimg, refPt[0], refPt[1], (0, 255, 0), 2)		#using rectangle function of cv2 library
		frame = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]		#definfing final frame coordinates
		points = numpy.where(frame==0)
		revP=[]						#initializing variable revP
		for i in range(len(points[0])):
			revP.append([points[1][i],points[0][i]])
		points=numpy.array(revP)	#storing data in numpy array for easier analysis
		xcom = numpy.mean(points[:,0])		#caluclting xcom by finding average
		ycom = numpy.mean(points[:,1])		#caluclting ycom by finding average
		xcomlist.append(xcom)				#appending to xcomlist
		ycomlist.append(ycom)				#appending to ycom list
		stDevX = numpy.std(points[:,0])		#calculating standard deviation using std function of numpy library
		stDevY = numpy.std(points[:,1])
		verticality = stDevY/stDevX 		# handle div by 0 cases
		slope=0								#initializing slope to 0
		regr = linear_model.LinearRegression()		#calculating linear regression to find best fit line
		if verticality<1:					#in case the slope of line does not tend to 90 degrees
			regr.fit(numpy.reshape([points[:,0]], (points.shape[0],1)), points[:,1])
			m =math.atan(-regr.coef_)		#since slope is not close to 90, taninv will work
			slope =regr.coef_
			c= regr.intercept_
		else:								#in case slope of line is close to 90 degrees
			regr.fit(numpy.reshape([points[:,1]], (points.shape[0],1)), points[:,0])
			slope = 1/regr.coef_
			m =1.57 - math.atan(-regr.coef_)	#since slope is close to 90 degrees, calculate cotinv instead of taninv
			c= -regr.intercept_/regr.coef_
		count+=1							#increases counter

		slopes.append(m)
		y1 = ycom-slope[0]*xcom
		y2=slope[0]*(frame.shape[0]-xcom)
		point2 = [frame.shape[0],y2+ycom]
		point1 = [0,y1]
		contours, heirarchy = cv2.findContours(frame, 1, 2)		#calling findContours function of cv2 library
		cnt = contours[0]
		(xxx, yyy), radi = cv2.minEnclosingCircle(cnt)
		center = (int(xxx), int(yyy))		#initializing variable for coordinates of centre
		radi = int(radi)					#initializing variable for radius
		nframe = frame.copy()
		lens.append(radi*2)
		cv2.namedWindow('image',cv2.WINDOW_NORMAL)		#calling namesWindow function of cv2 library
		cv2.resizeWindow('image', 600,600)				#calling resizeWindow function of cv2 library
		frame[frame == 0] = 1
		frame[frame == 255] = 0
		frame[frame == 1] = 255
		trace = numpy.maximum(frame,trace)				#setting maximum coordinates as frame size
		frame[frame == 0] = 1
		frame[frame == 255] = 0
		frame[frame == 1] = 255

		contours, heirarchy = cv2.findContours(trace, 1, 2)		#calling findContours function of cv2 library
		cnt = contours[0]
		(xx, yy), rad = cv2.minEnclosingCircle(cnt)		#calling minEnclosingCircle function of cv2 library
		center = (int(xx), int(yy))
		rad = int(rad)
		tracedia.append(rad*2)
		if( (abs(y1)<1000) or (abs(y2)<1000) ):
			cv2.line(frame,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])),(0,255,0),1)
		frame = cv2.resize(frame, (300, 300))			#calling resize function of cv2 library
		printtrace = trace.copy()
		printtrace = cv2.resize(printtrace,(300,300))
		frame = numpy.concatenate((frame, printtrace), axis=0)	#concatenating arrays using numpys inbuilt function
		orgimg = cv2.resize(orgimg, (600, 600))
		frame = numpy.concatenate((frame, orgimg), axis=1)    #Resize image
		cv2.imshow('image',frame)
		cv2.waitKey(delay)

	plt.scatter(xcomlist,ycomlist)			#computing scatter plot using pyplot library
	plt.title(utilities.cell_name)			#defining title of plot
	plt.xlabel('x com')						#defining x coordinate of plot
	plt.ylabel('y com')						#defining y coordinate of plot
	plt.savefig(out_folder + '/'+utilities.cell_name  +'xcom_ycom.png')

	plt.show()

	xcommean = numpy.mean(xcomlist)			#calculating mean by calling numpys function
	ycommean = numpy.mean(ycomlist)

	for i in xcomlist:
		xcomlist2.append(i-xcommean)
	for j in ycomlist:
		ycomlist2.append(j-ycommean)


def compute():
	'''
	Calculates frequency, change in angle per frame, total clockwise/counter-clockwise time 
	interval and no of frames and all else necessary outputs. Also outputs the finally analyzed 
	data in the form of CSV files and graphs

	'''
	
	#defines variables for furthur use
	time = utilities.time
	out_folder = utilities.out_folder
	a=0
	prev_a =0
	total_angle = 0.0	#change in total angle
	num_clock = 0		#number of frames with clockwise rotation
	num_anti = 0		#number of frames with anti clockwise rotation
	num_switch1 = 0		#number of switches from clockwise to counter
	num_switch2 = 0		#number of switches from counter to clockwise
	curr_block = 0 		#number of consecutive same directions
	pos_total = 0 		#total number of frames with positive direction
	neg_total = 0 		#total number of frames with negative direction
	global slopes,lens,tracedia,angles		#define global variable
	slopes = numpy.array(slopes)			#covert slopes array to numpy array
	prevang = (math.atan(0))
	count=0
	blocks=[]
	negfreqavg =0
	posfreqavg =0
	negcount=0
	poscount =0

	for i in slopes:	#for each slope in list (each frame's slope)
		currang = i 	#defining current angle
		diff = currang-prevang		#calculating difference
		abs_diff= min(abs(diff),abs(diff-3.14),(abs(diff+3.14)))	#calculating absolute difference
		if abs_diff!=0:		#if cell has rotated from previous frame
			if ((diff/abs_diff==1)|((diff-3.14)/abs_diff==1)|((diff+3.14)/abs_diff==1)):
				a=1
			else:
				a=-1
		else:				#if cell has not rotated
			a=prev_a
		if count == 0:
			total_angle = currang
		else:
			total_angle += abs_diff*a
		curr_block += 1
		if a == 1:
			num_clock += 1		#clockwise rotation
		else:
			num_anti += 1		#anticlockwise rotation
		if prev_a == 1 and a == -1:
			pos_total += curr_block
			if curr_block>5:
				blocks.append(curr_block)	
				num_switch1 += 1		#switch from clockwise to counter-clockwise
			curr_block = 1	
		if prev_a == -1 and a == 1:
			neg_total += curr_block		#switch from anti-clockwise to clockwise
			if curr_block>5:
				blocks.append(-curr_block)
				num_switch2 += 1
			curr_block = 1
		prev_a = a
		angles.append([count,currang,diff,abs_diff,a,abs_diff*a,((abs_diff*1000)/time), total_angle, lens[count], tracedia[count],(1000*abs_diff*a)/(time*6.28)])
		if((abs_diff*a)/(time*6.28)>0):
			posfreqavg = posfreqavg + (abs_diff*a)/(time*6.28)
			poscount= poscount +1		#increasing postive count
		else:
			negfreqavg = negfreqavg + (abs_diff*a)/(time*6.28)
			negcount = negcount +1		#increasing negative count
		count+=1
		prevang=i
	angles = numpy.array(angles[1:])	#triuncating numpy array
	stDev = numpy.std(angles[:,6])		#calculating standard deviation
	mean = numpy.mean(angles[:,6])		#calculating mean
	lastent = 0
	if(len(blocks) == 0):				#blocks to calcuate number of changes b/w clockwise and counter clockwise rotations
		lastent = 0
	else:
		lastent = blocks[len(blocks)-1]
	if(angles[len(angles)-1][4] == 1):
		blocks.append(curr_block)		#if rotation direction has changed
	else:
		blocks.append(-(curr_block))	#if rotation direction has not changed
	blocks = numpy.array(blocks)
	pos_total =0
	neg_total =0
	for dist in blocks:
		if dist>0:
			pos_total+=dist 			#counts number of clockwise rotations
		else:
			neg_total-=dist 			#counts numebr of counter-clockwise rotations
	
	with open(out_folder + 'file_details.csv', 'w') as f:		#saving output in file named file_details.csv
		writer = csv.writer(f)
		writer.writerow(['Frame Distribution', 'CW rotation frames', 'CW Rotation Time', 'CCW -> CW Switches','CCW rotation frames', 'CCW Rotation Time', 'CW -> CCW Switchs', 'Avg CW rot time interval', 'Avg CCW rot time interval', 'Mean Angular Speed', 'Deviation from mean', 'Ratio of time intervals [CW/CCW]', 'Average CCW frequency', 'Avg CW frequency'])
		if(num_switch1 == 0 and num_switch2 == 0 and neg_total == 0):
			writer.writerow([blocks, pos_total, pos_total*time, num_switch1, neg_total, neg_total*time, num_switch2, (pos_total*time), (neg_total*time), mean, stDev, 'Nan', (posfreqavg/poscount), (negfreqavg/negcount)])
		elif(num_switch1 == 0 and num_switch2 == 0 and pos_total == 0):
			writer.writerow([blocks, pos_total, pos_total*time, num_switch1, neg_total, neg_total*time, num_switch2, (pos_total*time), (neg_total*time), mean, stDev, (pos_total*num_switch2)/(neg_total), (posfreqavg/poscount), (negfreqavg/negcount)])
		elif(num_switch1 == 0):
			writer.writerow([blocks, pos_total, pos_total*time, num_switch1, neg_total, neg_total*time, num_switch2, 0, (neg_total*time)/num_switch2, mean, stDev, (pos_total*num_switch2)/(neg_total*num_switch1), (posfreqavg/poscount), (negfreqavg/negcount)])
		elif(num_switch2 == 0):
			writer.writerow([blocks, pos_total, pos_total*time, num_switch1, neg_total, neg_total*time, num_switch2, (pos_total*time)/num_switch1, 0 , mean, stDev, (pos_total*num_switch2)/(neg_total*num_switch1), (posfreqavg/poscount), (negfreqavg/negcount)])
		else:
			writer.writerow([blocks, pos_total, pos_total*time, num_switch1, neg_total, neg_total*time, num_switch2, (pos_total*time)/num_switch1, (neg_total*time)/num_switch2, mean, stDev, (pos_total*num_switch2)/(neg_total*num_switch1), (posfreqavg/poscount), (negfreqavg/negcount)])	