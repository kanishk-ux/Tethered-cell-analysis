import cv2
import numpy
import imgpros
from sklearn import linear_model
import math
import matplotlib.pyplot as plt
import csv
import utilities

slopes = []
tracedia = []
lens = []
xcomlist2 = []
ycomlist2 = []
xcomlist = []
ycomlist = []
angles = []


def analyze():
    count = 0
    meta = utilities.meta
    filename = utilities.filename
    folder_path = utilities.folder_path
    num_frames = utilities.num_frames
    delay = utilities.delay
    refPt = imgpros.refPt
    trace = imgpros.trace
    out_folder = utilities.out_folder
    global slopes, lens, tracedia, xcomlist2, ycomlist2, xcomlist, ycomlist
    prev_a = 0
    addr = folder_path + '/img_000000'
    ad = '_Default_000.tif'
    while (count < num_frames):
        if meta == 0:
            #print (count)
            frame = cv2.imread(folder_path + filename.replace("0", str(count)))
        else:
            frame = cv2.imread(addr + str("%03d" % count) + ad)
        frame = imgpros.threshold(frame)
        orgimg = frame.copy()
        cv2.rectangle(orgimg, refPt[0], refPt[1], (0, 255, 0), 2)
        frame = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        points = numpy.where(frame == 0)
        revP = []
        for i in range(len(points[0])):
            revP.append([points[1][i], points[0][i]])
        points = numpy.array(revP)
        xcom = numpy.mean(points[:, 0])
        ycom = numpy.mean(points[:, 1])
        xcomlist.append(xcom)
        ycomlist.append(ycom)
        stDevX = numpy.std(points[:, 0])
        stDevY = numpy.std(points[:, 1])
        verticality = stDevY / stDevX  # Handle div/0 cases]
        slope = 0
        regr = linear_model.LinearRegression()
        if verticality < 1:
            regr.fit(numpy.reshape([points[:, 0]], (points.shape[0], 1)), points[:, 1])
            m = math.atan(-regr.coef_)
            slope = regr.coef_
            c = regr.intercept_
        else:
            regr.fit(numpy.reshape([points[:, 1]], (points.shape[0], 1)), points[:, 0])
            slope = 1 / regr.coef_
            m = 1.57 - math.atan(-regr.coef_)
            c = -regr.intercept_ / regr.coef_
        # regr.fit(points[:,0], points[:,1])
        count += 1

        slopes.append(m)
        y1 = ycom - slope[0] * xcom
        y2 = slope[0] * (frame.shape[0] - xcom)
        point2 = [frame.shape[0], y2 + ycom]
        point1 = [0, y1]
        contours, heirarchy = cv2.findContours(frame, 1, 2)
        cnt = contours[0]
        (xxx, yyy), radi = cv2.minEnclosingCircle(cnt)
        center = ((xxx), (yyy))
        radi = (radi)
        nframe = frame.copy()
        #cv2.circle(frame, center, radi, (0, 255, 0), 1)

        lens.append(radi * 2)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 600, 600)
        frame[frame == 0] = 1
        frame[frame == 255] = 0
        frame[frame == 1] = 255
        trace = numpy.maximum(frame, trace)
        frame[frame == 0] = 1
        frame[frame == 255] = 0
        frame[frame == 1] = 255

        contours, heirarchy = cv2.findContours(trace, 1, 2)
        cnt = contours[0]
        (xx, yy), rad = cv2.minEnclosingCircle(cnt)
        center = ((xx), (yy))
        rad = (rad)
        tracedia.append(rad * 2)
        #cv2.circle(trace, center, rad, (0, 0, 0), 2)

        if((abs(y1) < 1000) or (abs(y2) < 1000)):
            cv2.line(frame, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])), (0, 255, 0), 1)
        frame = cv2.resize(frame, (300, 300))
        printtrace = trace.copy()
        printtrace = cv2.resize(printtrace, (300, 300))
        frame = numpy.concatenate((frame, printtrace), axis=0)
        orgimg = cv2.resize(orgimg, (600, 600))
        frame = numpy.concatenate((frame, orgimg), axis=1)                    # Resize image

        cv2.imshow('image', frame)

        cv2.waitKey(delay)

    plt.scatter(xcomlist, ycomlist)
    plt.title(utilities.cell_name)
    plt.xlabel('x com')
    plt.ylabel('y com')
    plt.savefig(out_folder + '/' + utilities.cell_name + 'xcom_ycom.png')

    plt.show()

    xcommean = numpy.mean(xcomlist)
    ycommean = numpy.mean(ycomlist)

    for i in xcomlist:
        xcomlist2.append(i - xcommean)
    for j in ycomlist:
        ycomlist2.append(j - ycommean)


def compute():
    time = utilities.time
    out_folder = utilities.out_folder
    a = 0
    prev_a = 0
    total_angle = 0.0  # change in total angle
    num_clock = 0       # number of frames with clockwise rotation
    num_anti = 0        # number of frames with anti clockwise rotation
    num_switch1 = 0    # number of switches from clockwise to counter
    num_switch2 = 0    # number of switches from counter to clockwise

    curr_block = 0  # number of consecutive same directions
    pos_total = 0  # total number of frames with positive direction
    neg_total = 0  # total number of frames with negative direction

    global slopes, lens, tracedia, angles
    slopes = numpy.array(slopes)
    prevang = (math.atan(0))
    # time = (data[fd1+'499'+fd2]['ElapsedTime-ms']-data[fd1+'0'+fd2]['ElapsedTime-ms'])/500
    count = 0
    blocks = []
    negfreqavg = 0
    posfreqavg = 0
    negcount = 0
    poscount = 0
    for i in slopes:
        currang = i
        diff = currang - prevang
        abs_diff = min(abs(diff), abs(diff - 3.14), (abs(diff + 3.14)))
        if abs_diff != 0:
            if ((diff / abs_diff == 1) | ((diff - 3.14) / abs_diff == 1) | ((diff + 3.14) / abs_diff == 1)):
                a = 1
            else:
                a = -1
        else:
            a = prev_a
        if count == 0:
            total_angle = currang
        else:
            total_angle += abs_diff * a
        curr_block += 1
        if a == 1:
            num_clock += 1
        else:
            num_anti += 1
        if prev_a == 1 and a == -1:
            pos_total += curr_block
            if curr_block > 5:
                blocks.append(curr_block)
                num_switch1 += 1
            curr_block = 1
        if prev_a == -1 and a == 1:
            neg_total += curr_block
            if curr_block > 5:
                blocks.append(-curr_block)
                num_switch2 += 1
            curr_block = 1
        prev_a = a
        angles.append([count, currang, diff, abs_diff, a, abs_diff * a, ((abs_diff * 1000) / time), total_angle, lens[count], tracedia[count], (1000 * abs_diff * a) / (time * 6.28)])
        if((abs_diff * a) / (time * 6.28) > 0):
            posfreqavg = posfreqavg + (abs_diff * a) / (time * 6.28)
            poscount = poscount + 1
        else:
            negfreqavg = negfreqavg + (abs_diff * a) / (time * 6.28)
            negcount = negcount + 1
        count += 1
        prevang = i

    angles = numpy.array(angles[1:])
    stDev = numpy.std(angles[:, 6])
    mean = numpy.mean(angles[:, 6])
    celllengthavg = numpy.mean(angles[:, 8])
    tracediaavg = numpy.mean(angles[:, 9])
    lastent = 0
    if(len(blocks) == 0):
        lastent = 0
    else:
        lastent = blocks[len(blocks) - 1]
    if(angles[len(angles) - 1][4] == 1):
        blocks.append(curr_block)
    else:
        blocks.append(-(curr_block))
    blocks = numpy.array(blocks)
    pos_total = 0
    neg_total = 0
    for dist in blocks:
        if dist > 0:
            pos_total += dist
        else:
            neg_total -= dist
    from radius import R_1
    with open(out_folder + 'file_details.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Frame Distribution', 'CCW rotation frames', 'CCW Rotation Time', 'CCW -> CW Switches', 'CW rotation frames', 'CW Rotation Time', 'CW -> CCW Switchs', 'Avg CCW rot time interval', 'Avg CW rot time interval', 'Mean Angular Speed', 'Deviation from mean', 'Ratio of time intervals [CCW/CW]', 'Average CCW frequency', 'Avg CW frequency', 'length(Avg)', 'Tracedia(Avg)', 'Radius'])
        if(num_switch1 == 0 and num_switch2 == 0 and neg_total == 0):
            writer.writerow([blocks, pos_total, pos_total * time, num_switch1, neg_total, neg_total * time, num_switch2, (pos_total * time), (neg_total * time), mean, stDev, 'Nan', (posfreqavg / poscount), (negfreqavg / negcount), celllengthavg, tracediaavg, R_1])
        elif(num_switch1 == 0 and num_switch2 == 0 and pos_total == 0):
            writer.writerow([blocks, pos_total, pos_total * time, num_switch1, neg_total, neg_total * time, num_switch2, (pos_total * time), (neg_total * time), mean, stDev, (pos_total) / (neg_total), (posfreqavg / poscount), (negfreqavg / negcount), celllengthavg, tracediaavg, R_1])
        elif(num_switch1 == 0):
            writer.writerow([blocks, pos_total, pos_total * time, num_switch1, neg_total, neg_total * time, num_switch2, 0, (neg_total * time) / num_switch2, mean, stDev, (pos_total) / (neg_total), (posfreqavg / poscount), (negfreqavg / negcount), celllengthavg, tracediaavg, R_1])
        elif(num_switch2 == 0):
            writer.writerow([blocks, pos_total, pos_total * time, num_switch1, neg_total, neg_total * time, num_switch2, (pos_total * time) / num_switch1, 0, mean, stDev, (pos_total) / (neg_total), (posfreqavg / poscount), (negfreqavg / negcount), celllengthavg, tracediaavg, R_1])
        else:
            writer.writerow([blocks, pos_total, pos_total * time, num_switch1, neg_total, neg_total * time, num_switch2, (pos_total * time) / num_switch1, (neg_total * time) / num_switch2, mean, stDev, (pos_total) / (neg_total), (posfreqavg / poscount), (negfreqavg / negcount), celllengthavg, tracediaavg, R_1])
