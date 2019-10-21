import sys
import func
import os

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    from tkinter.filedialog import askopenfilename

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

global filename
password = ""
mode = ""
global outputfile

variable_1 = -1
variable_2 = -1
variable_3 = -1
variable_4 = -1


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def callback():
    global filename, outputfile
    filename = askopenfilename()
    # w.var2.set(filename)
    print (filename)
    # outputfile = os.path.split(filename)[0]
    # print (filename + " " + outputfile)


def encrypt_decrypt_dummy():
    # print ("enetered " + outputfile)

    frames = w.Entry1.get()
    metadata = w.Entry2.get()
    fps = w.Entry3.get()
    delay = w.Entry4.get()

    print (filename.replace(" ","@@@"))

    # print (a)
    os.system("python3" + " Tcap3.py " + filename + " " + frames + " " + metadata + " " + fps + " " + delay)
    # mode = w.var.get()
    # password = w.Entry2.get()
    # outputfile1 = outputfile + "/" + w.Entry1.get()
    # print ("filename : " + filename + " mode : " + mode + " Password : " + password + " outputfile : " + outputfile1)
    # func.encrypt_decrypt(["a", filename, mode, password, outputfile1])


if __name__ == '__main__':
    import gui_handeller
    gui_handeller.vp_start_gui()
    