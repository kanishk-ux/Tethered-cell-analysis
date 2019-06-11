'''
	File takes input from user using GUI and passes arguments taken to tcap3
'''

import sys
import func
import os


'''
	Importing package Tkinter and handling errors
	Tkinter is a GUI processing library which helps to create window which exists independetly on the screen
'''
try:
	from Tkinter import *
except ImportError:
	from tkinter import *
	from tkinter.filedialog import askopenfilename


'''Importing package ttk and handing errors
   ttk is a dependency of Tkinter
'''
try:
	import ttk
	py3 = 0
except ImportError:
	import tkinter.ttk as ttk
	py3 = 1


'''Defining global variable filename and outputfile'''
global filename
password = ""
mode = ""
global outputfile

variable_1 = -1
variable_2 = -1
variable_3 = -1
variable_4 = -1


def init(top, gui, *args, **kwargs):
	'''
	Initializing function calls the GUI handler
	Input Variables: top, gui
	'''
	global w, top_level, root
	w = gui
	top_level = top
	root = top


def destroy_window():
	'''
	Function which closes the window.
	'''
	global top_level
	top_level.destroy()
	top_level = None


def callback():
	'''
	Callback function used to loop back to original 
	'''
	global filename, outputfile
	filename = askopenfilename()
	print (filename)


def encrypt_decrypt_dummy():
	'''
	Function which is used to execute command after inputs are taken from GUI
	'''
	frames = w.Entry1.get()
	metadata = w.Entry2.get()
	fps = w.Entry3.get()
	delay = w.Entry4.get()
	print (filename.replace(" ","@@@"))
	os.system("python3" + " main.py " + filename + " " + frames + " " + metadata + " " + fps + " " + delay)


if __name__ == '__main__':
	import gui_handeller
	gui_handeller.vp_start_gui()
	