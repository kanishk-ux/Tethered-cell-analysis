'''Used for fitting circle to the COM data of each frame of the rotating cell by 3 methods: Least Square, ODR, Algebraic
	Analyzes the centre of rotation and calculates the radius, meaning the distance b/w the centre of rotation and the COM

	Credits: User mpastell on Github in repo SciPy-CookBook
	Original Code on https://github.com/mpastell/SciPy-CookBook/blob/master/originals/Least_Squares_Circle_attachments/least_squares_circle.py
'''

import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.optimize as opt
from numpy import *
from scipy import optimize
from scipy import odr
from __main__ import *
import model
import utilities


limit = max(utilities.num_frames,500)	#limits number of frames to 500

#defines variables for furthur use
radius2 = []
residues12 = []
residues22 = []
x = model.xcomlist2[:limit]
y = model.ycomlist2[:limit]

x_m = mean(x)	#calculates mean of all values in list x
y_m = mean(y)	#calculates mean of all values in list y

method_1 = 'algebraic'
method_2 = "leastsq"
basename = 'circle'

u = x - x_m
v = y - y_m


#  == METHOD 1 ==
#  ALGEBRAIC METHOD

#defines variables to be used in Method 1
Suv = sum(u * v)
Suu = sum(u**2)
Svv = sum(v**2)
Suuv = sum(u**2 * v)
Suvv = sum(u * v**2)
Suuu = sum(u**3)
Svvv = sum(v**3)

# Solving the linear system
A = array([[Suu, Suv], [Suv, Svv]])
B = array([Suuu + Suvv, Svvv + Suuv]) / 2.0
uc, vc = linalg.solve(A, B)		#use function to solve by algebraic method

xc_1 = x_m + uc
yc_1 = y_m + vc

# Calculation of all distances from the center (xc_1, yc_1)
Ri_1 = sqrt((x - xc_1)**2 + (y - yc_1)**2)
R_1 = mean(Ri_1)
residu_1 = sum((Ri_1 - R_1)**2)
residu2_1 = sum((Ri_1**2 - R_1**2)**2)

print('method 1 starts')
print(R_1)
print(residu_1)
print(residu2_1)
radius2.append(R_1)
residues12.append(residu_1)
residues22.append(residu2_1)
print('method 1 ends')

# Decorator to count functions calls
import functools


def countcalls(fn):
	'''decorator function count function calls'''
	@functools.wraps(fn)
	def wrapped(*args):
		wrapped.ncalls += 1
		return fn(*args)

	wrapped.ncalls = 0
	return wrapped


#  == METHOD 2 ==
#  LEAST SQUARE METHOD

def calc_R(xc, yc):
	""" calculate the distance of each 2D points from the center (xc, yc) """
	return sqrt((x - xc)**2 + (y - yc)**2)


@countcalls
def f_2(c):
	""" calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
	Ri = calc_R(*c)
	return Ri - Ri.mean()


center_estimate = x_m, y_m
center_2, ier = optimize.leastsq(f_2, center_estimate)

xc_2, yc_2 = center_2
Ri_2 = calc_R(xc_2, yc_2)
R_2 = Ri_2.mean()
residu_2 = sum((Ri_2 - R_2)**2)
residu2_2 = sum((Ri_2**2 - R_2**2)**2)
ncalls_2 = f_2.ncalls

print('method 2a starts')
print(R_2)
print(residu_2)
print(residu2_2)
radius2.append(R_2)
residues12.append(residu_2)
residues22.append(residu2_2)
print('method 2a ends')


# == METHOD 3 ==
# ODR METHOD

method_3 = "odr"


@countcalls
def f_3(beta, x):
	""" implicit definition of the circle """
	return (x[0] - beta[0])**2 + (x[1] - beta[1])**2 - beta[2]**2


# initial guess for parameters
R_m = calc_R(x_m, y_m).mean()
beta0 = [x_m, y_m, R_m]

# for implicit function :
#       data.x contains both coordinates of the points
#       data.y is the dimensionality of the response
lsc_data = odr.Data(row_stack([x, y]), y=1)
lsc_model = odr.Model(f_3, implicit=True)
lsc_odr = odr.ODR(lsc_data, lsc_model, beta0)
lsc_out = lsc_odr.run()

xc_3, yc_3, R_3 = lsc_out.beta
Ri_3 = calc_R(xc_3, yc_3)
residu_3 = sum((Ri_3 - R_3)**2)
residu2_3 = sum((Ri_3**2 - R_3**2)**2)
ncalls_3 = f_3.ncalls

print('method 3 starts')
print(R_3)
print(residu_3)
print(residu2_3)
radius2.append(R_3)
residues12.append(residu_3)
residues22.append(residu2_3)
print('method 3 ends')

# plotting functions
from matplotlib import pyplot as p, cm, colors
p.close('all')


def plot_all(residu2=False):
	''' function to plot all the graphs'''
	f = p.figure(facecolor='white')  # figsize=(7, 5.4), dpi=72,
	p.axis('equal')

	theta_fit = linspace(-pi, pi, 180)

	x_fit1 = xc_1 + R_1 * cos(theta_fit)
	y_fit1 = yc_1 + R_1 * sin(theta_fit)
	p.plot(x_fit1, y_fit1, 'b-', label=method_1, lw=2)

	x_fit2 = xc_2 + R_2 * cos(theta_fit)
	y_fit2 = yc_2 + R_2 * sin(theta_fit)
	p.plot(x_fit2, y_fit2, 'k--', label=method_2, lw=2)

	x_fit3 = xc_3 + R_3 * cos(theta_fit)
	y_fit3 = yc_3 + R_3 * sin(theta_fit)
	p.plot(x_fit3, y_fit3, 'r-.', label=method_3, lw=2)

	p.plot([xc_1], [yc_1], 'bD', mec='y', mew=1)
	p.plot([xc_2], [yc_2], 'gD', mec='r', mew=1)
	p.plot([xc_3], [yc_3], 'kD', mec='w', mew=1)

	# draw
	p.xlabel('x')
	p.ylabel('y')

	# plot the residu fields
	nb_pts = 100

	p.draw()
	left, right = p.xlim()
	bottom, top = p.ylim()

	vmin = min(left, bottom)
	vmax = max(right, top)

	xg, yg = ogrid[vmin:vmax:nb_pts * 1j, vmin:vmax:nb_pts * 1j]
	xg = xg[..., newaxis]
	yg = yg[..., newaxis]

	Rig = sqrt(power((xg - x),2) + power((yg - y),2))
	Rig_m = Rig.mean(axis=2)[..., newaxis]

	if residu2:
		residu = sum((Rig**2 - Rig_m**2)**2, axis=2)
	else:
		residu = sum((Rig - Rig_m)**2, axis=2)

	lvl = exp(linspace(log(residu.min()), log(residu.max()), 15))

	p.contourf(xg.flat, yg.flat, residu.T, lvl, alpha=0.4, cmap=cm.Purples_r)  # , norm=colors.LogNorm())
	cbar = p.colorbar(fraction=0.175, format='%.f')
	p.contour(xg.flat, yg.flat, residu.T, lvl, alpha=0.8, colors="lightblue")

	if residu2:
		cbar.set_label('Residu_2 - algebraic approximation')
	else:
		cbar.set_label('Residu')

	# plot data
	p.plot(x, y, 'ro', label='data', ms=8, mec='b', mew=1)
	p.legend(loc='best', labelspacing=0.1)

	p.xlim(left=vmin, right=vmax)
	p.ylim(bottom=vmin, top=vmax)

	p.grid()
	p.title(utilities.cell_name)
	p.savefig(utilities.out_folder+utilities.cell_name+'%s_residu%d.png' % (basename, 2 if residu2 else 1))


plot_all(residu2=False)
plot_all(residu2=True)

p.show()	#displays the graphs
print ([R_1, R_2, R_3])		#outputs radius obtained by 3 methods