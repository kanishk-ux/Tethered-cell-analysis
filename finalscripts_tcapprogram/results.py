import csv
import model
import matplotlib.pyplot as plt
import cv2
import utilities
def save():
	out_folder =utilities.out_folder
	time =utilities.time
	outfilename =utilities.outfilename
	import radius	
	with open(out_folder + 'COM.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['X coordinate', 'Y coordinate'])
		for i in range(len(model.xcomlist)):
			writer.writerow([model.xcomlist[i], model.ycomlist[i]])
		writer.writerow(['','',''])
		
		writer.writerow(['radius', 'residues1', 'residues2'])
		for j in range(3):
			writer.writerow([radius.radius2[j], radius.residues12[j], radius.residues22[j]])

	plt.ylim(-2, 2)
	plt.plot(time*model.angles[:,0], model.angles[:,5], '-')
	plt.title(utilities.cell_name)
	plt.xlabel('time')
	plt.ylabel('change in angle in rad')
	plt.savefig(out_folder + '/'  +utilities.cell_name+'_del_theta.png')
	plt.show()

	plt.clf()
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
	# abs_diff*a vs count
	# cumulative angle change values vs frame count

	with open(out_folder + outfilename, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['frame count', 'currant angle', 'angle difference', 'absolute difference', 'direction', 'difference with direction', 'angular speed', 'total angle', 'cell length', 'trace diameter', 'frequency'])
		for i in model.angles:
				writer.writerow(i)
		writer.writerow(['radius', 'residues1', 'residues2'])
		for j in range(3):
			writer.writerow([radius.radius2[j], radius.residues12[j], radius.residues22[j]])
	# numpy.savetxt("foo.csv", angles, delimiter=",")
	cv2.destroyAllWindows()