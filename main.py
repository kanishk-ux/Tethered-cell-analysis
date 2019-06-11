'''
	main file which takes argument from encrypt.py and executes further functions as documented in the file
'''
import imgpros
import sys
import utilities
import model
import results

'''Initializes the inputs taken from encrypt.py and stores them for furthur use'''
utilities.intializer(sys.argv)


'''Displays a preview of initial 50 frames to help cropping of rotating cell by the user'''
utilities.preview()


'''Allows user to select a free-size rectangular portion of the first frame consisting of a cell for furthur analysis'''
imgpros.crop()


'''Performs Linear Regression Analysis the cropped portion of all the frames and outputs 
	the centre of mass(COM) data for and a plot of COM for furthur use'''
model.analyze()


'''Calculates frequency, change in angle per frame, total clockwise/counter-clockwise time interval and no of frames and 
	all else necessary outputs. Also outputs the finally analyzed data in the form of CSV files and graphs'''
model.compute()


'''Saves the graphs and CSV files obtained after analysis in the required folder'''
results.save()