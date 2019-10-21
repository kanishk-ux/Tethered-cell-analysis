import base64
import sys
import random
import tkinter

def encrypt_decrypt(argv1):
 try:
    arg=argv1[2]#args[1]        #input("encode/decode:")
    filename =argv1[1]#args[0]  #input("input file:")
    filename2 =argv1[4]#args[3] #input("output file")
    dummyname =argv1[3]#args[2] #input("enter dummy name")
    if (( arg !='d') & (arg != 'en')) :
        print ("ERROR:\nenter: filename d|en corruptionword[greater than 3] outputfil ")
        
 except Exception as e:
        print ('ERROR: requires 4 arguements: ')
        print ("enter: filename d|en corruptionword[greater than 3] outputfile ")
        tkinter.tkMessageBox.showinfo("4 arguements")

 try:
        fileobject=open(filename,"rb")
        fileobject1=open(filename2,"wb")
 except Exception as e:
        print ('Did I jump directly to here?' + str(e))
        

 data=fileobject.read()
 try:

    encoded_data="123"
    if(arg=='en'):
       encoded_data1=base64.b64encode(data)
       x=random.randint(20,100)
       if (x<len(encoded_data)/2):
           encoded_data = encoded_data1[:x]+bytes(dummyname, 'utf-8')+encoded_data1[x:]
       else:
           encoded_data = encoded_data1[:10]+bytes(dummyname, 'utf-8')+encoded_data1[10:]
       x=random.randint( int(len(encoded_data)/2),len(encoded_data))
       random_encoded=encoded_data[:x]+bytes(dummyname, 'utf-8')+encoded_data[x:]
    elif(arg=='d'):
       data1=data.replace(bytes(dummyname, 'utf-8'),bytes('', 'utf-8'))
       encoded_data = base64.b64decode(data1)
       random_encoded=encoded_data
 except Exception as e:
        print ('ERROR: wrong password :p '+ str(e))
        

 fileobject1.write(random_encoded)
 fileobject1.close()
 fileobject.close()

# encrypt_decrypt(["a","out2","en","password","outfuck"])