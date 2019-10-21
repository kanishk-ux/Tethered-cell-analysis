import numpy
import matplotlib.pyplot as plt
from sklearn import linear_model
import cv2
import math
import utilities


image = []
refPt = []
trace = []
cropping = False

def threshold(img):
    images = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = numpy.ones((3, 3), numpy.float32) / 9

    avg_color_per_row = numpy.average(gray, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)

    if(int(avg_color) == 0):
        avg_color = 1

    ret, thresh = cv2.threshold(gray, avg_color - 1, 255, cv2.THRESH_BINARY)
    binary1 = thresh
    thresh = cv2.filter2D(thresh, -1, kernel)
    smooth = thresh
    avg_color_per_row = numpy.average(thresh, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    ret, thresh = cv2.threshold(thresh, avg_color, 255, cv2.THRESH_BINARY)

    thresh1 = cv2.medianBlur(thresh, 7)
    binary2 = thresh
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh1

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping,image
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

def crop():
    meta = utilities.meta
    filename = utilities.filename
    folder_path = utilities.folder_path
    global image,trace,refPt       
    addr = folder_path + '/img_000000'
    ad = '_Default_000.tif'
    print ('crop cell for analysis.....')
    print ('Press c to proceed after cropping')
    print ('Press r to redo')
    if meta == 1:
        frame = addr + '000' + ad
    else:
        frame = folder_path + filename
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(frame)
    image = threshold(image)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from teh image and display it

    # close all open windows
    cv2.destroyAllWindows()

    a = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    trace = numpy.zeros((a.shape[0],a.shape[1]), numpy.uint8)
