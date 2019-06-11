'''
	Connector file between giu_handler.py and encrypt.py
	Takes data from gui_handler.py, decodes it to the desired format and outputs it to be stored to varaibles
'''

import base64
import sys
import random
import tkinter

def encrypt_decrypt(argv1):
	'''
	Decodes data taken from the user to the desired format
	Input: argv1 (input taken from the user)
	'''

	try:
		#takes inputs from user and stores them in corresponding variables
		arg=argv1[2]
		filename =argv1[1]
		filename2 =argv1[4]		
		dummyname =argv1[3]
		
		if (( arg !='d') & (arg != 'en')) :		#filename corrupt
		    print ("ERROR:\nenter: filename d|en corruptionword[greater than 3] outputfil ")
	    
	except Exception as e:					#4 arguments not given by user
	    print ('ERROR: requires 4 arguements: ')
	    print ("enter: filename d|en corruptionword[greater than 3] outputfile ")
	    tkinter.tkMessageBox.showinfo("4 arguements")

	try:									#opening files whose names were given by user
	    fileobject=open(filename,"rb")
	    fileobject1=open(filename2,"wb")
	except Exception as e:					#throws exception
	    print ('Did I jump directly to here?' + str(e))
	    

	data=fileobject.read()					#reads object from file
	
	try:									#try reading data from specified file
		encoded_data="123"
		if(arg=='en'):
		   encoded_data1=base64.b64encode(data)		#decodes data to base64
		   x=random.randint(20,100)					#defines random integer from 20 to 100
		   if (x<len(encoded_data)/2):				#decodes first half of data
		       encoded_data = encoded_data1[:x]+bytes(dummyname, 'utf-8')+encoded_data1[x:]
		   else:									#decodes second half of data
		       encoded_data = encoded_data1[:10]+bytes(dummyname, 'utf-8')+encoded_data1[10:]
		   x=random.randint( int(len(encoded_data)/2),len(encoded_data))
		   random_encoded=encoded_data[:x]+bytes(dummyname, 'utf-8')+encoded_data[x:]
		elif(arg=='d'):
		   data1=data.replace(bytes(dummyname, 'utf-8'),bytes('', 'utf-8'))
		   encoded_data = base64.b64decode(data1)
		   random_encoded=encoded_data
	except Exception as e:					#exception thrown because of wrong password
	    print ('ERROR: wrong password :p '+ str(e))
	    

	fileobject1.write(random_encoded)		#writes data to output file
	fileobject1.close()						#closes fileobject1 pointer
	fileobject.close()						#closes fileobject pointer
