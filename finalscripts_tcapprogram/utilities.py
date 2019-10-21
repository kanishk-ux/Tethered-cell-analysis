import cv2
import os
import json
import imgpros
import cv2

image = []
refPt = []
cropping = False
folder_path = ''
filename = ''
num_frames = 0
meta = 0
delay = 0
outfilename = ''
out_folder = ''
time = 0
cell_name = ''


def intializer(argv):
    global folder_path, filename, num_frames, meta, delay, outfilename, out_folder, time, cell_name
    folder_path = argv[1]
    print (folder_path)
    folder = folder_path.split("/")
    a = 0
    folder_path = ""

    while a < (len(folder) - 1):
        folder_path += folder[a]
        folder_path += "/"
        a = a + 1
    filename = folder[a]
    tuta = folder_path.split('/')
    cell_name = tuta[len(tuta) - 2]
    out_folder = folder_path + cell_name + "_out/"
    global num_frames
    num_frames = argv[2]
    num_frames = int(num_frames)

    # int(raw_input('Enter number of frames to process: '))
    if not os.path.isdir(out_folder):
        print ('creating new directory')
        os.makedirs(out_folder)
    outfilename = "raw_data.csv"

    meta = int(argv[3])
    if meta == 1:
        fd1 = 'FrameKey-'
        fd2 = '-0-0'
        print (fd1 + str(num_frames - 1) + fd2)
        with open(folder_path + '/metadata.txt') as f:
            data = json.load(f)
        time = (data[fd1 + str(num_frames - 1) + fd2]['ElapsedTime-ms'] - data[fd1 + '0' + fd2]['ElapsedTime-ms']) / num_frames
    else:
        fps = argv[4]
        fps = int(fps)
        # int(raw_input('Enter FPS: '))
        time = 1.0 / float(fps)
    print ('time between frames ' + str(time))

    delay = argv[5]
    delay = int(delay)


def preview():
    global meta, filename, folder_path, delay
    addr = folder_path + '/img_000000'
    ad = '_Default_000.tif'
    frame = addr + '000' + ad
    if meta == 0:
        frame = cv2.imread(folder_path + filename)
    else:
        frame = cv2.imread(addr + '000' + ad)
    print ('\nPreviewing.....\n')
    count = 0
    while (count < 50):
        if meta == 0:
            print (count)
            print (filename)
            print (folder_path + filename.replace("0", str("%1d" % count)))
            frame = cv2.imread(folder_path + filename.replace("0", str("%1d" % count)))
        else:
            frame = cv2.imread(addr + str("%03d" % count) + ad)
        image = imgpros.threshold(frame)
        cv2.imshow('image', image)
        cv2.waitKey(delay)
        count += 1


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, image
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


def crop(meta, filename, folder_path):
    global image
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
    image = threshold.threshold(image)
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
    trace = numpy.zeros((a.shape[0], a.shape[1]), numpy.uint8)
    return refPt, trace
