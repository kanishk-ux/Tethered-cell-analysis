'''
GUI handler file for displaying external window and taking desired input from user
'''

import sys
import encrypt

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

w = None

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root
	root = Tk()
	top = New_Toplevel_1(root)
	encrypt.init(root, top)
	root.mainloop()



def create_New_Toplevel_1(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w, w_win, rt
	rt = root
	w = Toplevel(root)
	top = New_Toplevel_1(w)
	encrypt.init(w, top, *args, **kwargs)
	return (w, top)


def destroy_New_Toplevel_1():
	'''
	Destroying top level window when program needs to be closed
	'''
	global w
	w.destroy()
	w = None


class New_Toplevel_1:
	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''

		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9'  # X11 color: 'gray85'
		_ana1color = '#d9d9d9'  # X11 color: 'gray85'
		_ana2color = '#d9d9d9'  # X11 color: 'gray85'
		self.var = StringVar()
		self.var2 = StringVar()
		top.geometry("600x450+630+130")
		top.title("Cell Analyzer 0.100")
		top.configure(highlightcolor="black")

		self.Frame1 = Frame(top)
		self.Frame1.place(relx=0.1, rely=0.11, relheight=0.68, relwidth=0.81)
		self.Frame1.configure(relief=GROOVE)
		self.Frame1.configure(borderwidth="2")
		self.Frame1.configure(relief=GROOVE)
		self.Frame1.configure(width=485)

		self.Label1 = Label(self.Frame1)
		self.Label1.place(relx=0.19, rely=0.21, height=18, width=71)
		self.Label1.configure(activebackground="#f9f9f9")
		self.Label1.configure(text='''# frames''')

		self.Entry1 = Entry(self.Frame1)
		self.Entry1.place(relx=0.39, rely=0.21, relheight=0.07, relwidth=0.3)
		self.Entry1.configure(background="white")
		self.Entry1.configure(font="TkFixedFont")
		self.Entry1.configure(selectbackground="#c4c4c4")

		self.Label2 = Label(self.Frame1)
		self.Label2.place(relx=0.19, rely=0.31, height=18, width=71)
		self.Label2.configure(activebackground="#f9f9f9")
		self.Label2.configure(text='''MData_0/1''')

		self.Entry2 = Entry(self.Frame1)
		self.Entry2.place(relx=0.39, rely=0.31, relheight=0.07, relwidth=0.3)
		self.Entry2.configure(background="white")
		self.Entry2.configure(font="TkFixedFont")
		self.Entry2.configure(selectbackground="#c4c4c4")

		self.Label3 = Label(self.Frame1)
		self.Label3.place(relx=0.19, rely=0.41, height=18, width=71)
		self.Label3.configure(activebackground="#f9f9f9")
		self.Label3.configure(text='''FPS VALUE''')

		self.Entry3 = Entry(self.Frame1)
		self.Entry3.place(relx=0.39, rely=0.41, relheight=0.07, relwidth=0.3)
		self.Entry3.configure(background="white")
		self.Entry3.configure(font="TkFixedFont")
		self.Entry3.configure(selectbackground="#c4c4c4")

		self.Entry4 = Entry(self.Frame1)
		self.Entry4.place(relx=0.39, rely=0.51, relheight=0.07, relwidth=0.3)
		self.Entry4.configure(background="white")
		self.Entry4.configure(font="TkFixedFont")
		self.Entry4.configure(selectbackground="#c4c4c4")

		self.Label4 = Label(self.Frame1)
		self.Label4.place(relx=0.19, rely=0.51, height=18, width=71)
		self.Label4.configure(activebackground="#f9f9f9")
		self.Label4.configure(text='''Dlay 1-100''')

		self.Browse = Button(self.Frame1, command=encrypt.callback)
		self.Browse.place(relx=0.45, rely=0.0, height=26, width=67)
		self.Browse.configure(activebackground="#d9d9d9")
		self.Browse.configure(text='''Folder''')


		self.Message1 = Message(self.Frame1)
		self.Message1.place(relx=0.35, rely=0.1, relheight=0.11, relwidth=0.31)
		self.Message1.configure(text='''Enter Parameters''')
		self.Message1.configure(width=150)

		self.Done = Button(top, command=encrypt.encrypt_decrypt_dummy)
		self.Done.place(relx=0.8, rely=0.82, height=26, width=67)
		self.Done.configure(activebackground="#d9d9d9")
		self.Done.configure(text='''Done''')

		self.Message2 = Message(top)
		self.Message2.place(relx=0.08, rely=0.89, relheight=0.04, relwidth=0.46)
		self.Message2.configure(text='''''')
		self.Message2.configure(width=273)


if __name__ == '__main__':
	vp_start_gui()
