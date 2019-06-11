'''Saves all required data to corresponding files'''

import csv
import model
import matplotlib.pyplot as plt
import cv2
import utilities
def save():
	'''
		Saves all required data to corresponding files
	'''

	#defining variables and getting values from utilities.py file
	out_folder = utilities.out_folder
	time = utilities.time
	outfilename = utilities.outfilename

	import radius	
	with open(out_folder + 'COM.csv', 'w') as f:	#opening COM.csv where all centre of mass data has to be saved
		writer = csv.writer(f)
		writer.writerow(['X coordinate', 'Y coordinate'])	#write COM data in row of CSV file
		for i in range(len(model.xcomlist)):		#for each row in array of COM
			writer.writerow([model.xcomlist[i], model.ycomlist[i]])	#writes COM till end of array is reached
		writer.writerow(['','',''])
		
		writer.writerow(['radius', 'residues1', 'residues2'])	
		for j in range(3):
			writer.writerow([radius.radius2[j], radius.residues12[j], radius.residues22[j]])

	#next 3 chunks of code involve plotting required data using pyplot library
	plt.ylim(-2, 2)															#limiting y coordinates of plot
	plt.plot(time*model.angles[:,0], model.angles[:,5], '-')				#specifications of plot
	plt.title(utilities.cell_name)											#title of plot
	plt.xlabel('time')														#x axis label
	plt.ylabel('change in angle in rad')									#y axis label
	plt.savefig(out_folder + '/'  +utilities.cell_name+'_del_theta.png')	#saving plot as .png file
	plt.show()																#showing the plot in display for user

	plt.clf()																#clear previous plot
	plt.plot(time*model.angles[:,0], model.angles[:,5]/(time*6.28), '-')
	plt.title(utilities.cell_name)
	plt.xlabel('time')
	plt.ylabel('Frequency(Hz)')
	plt.savefig(out_folder + '/' + utilities.cell_name+'_frequency.png')
	plt.show()

	plt.clf()
	plt.plot(model.angles[:,0], model.angles[:,7], 'ro')
	plt.title(utilities.cell_name)
	plt.xlabel('frame count')
	plt.ylabel('total angle')
	plt.savefig(out_folder + '/' +  utilities.cell_name+'_total_angle.png')
	plt.show()
	plt.clf()

	with open(out_folder + outfilename, 'w') as f:		#opening new file for writing relevant data
		writer = csv.writer(f)							#defining pointer to open csv file
		writer.writerow(['frame count', 'currant angle', 'angle difference', 'absolute difference', 'direction', 'difference with direction', 'angular speed', 'total angle', 'cell length', 'trace diameter', 'frequency'])
		for i in model.angles:
				writer.writerow(i)
		writer.writerow(['radius', 'residues1', 'residues2'])
		for j in range(3):
			writer.writerow([radius.radius2[j], radius.residues12[j], radius.residues22[j]])
	cv2.destroyAllWindows()								#closing all cv2 windows