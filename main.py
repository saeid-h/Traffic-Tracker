'''
#############################################################################
#																			#
# Copyright (c) 2021 under MIT License                                      #
# Code by Saeid Hosseinipoor <https://saeid-h.github.io/>		            #
# All rights reserved.														#
#																			#
############################################################################# 

References:
    https://www.learnpythonwithrune.org/opencv-counting-cars-a-simple-approach/
    https://towardsdatascience.com/build-a-motion-heatmap-videousing-opencv-with-python-fd806e8a2340
    https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
'''

import cv2
import imutils
import numpy as np
import argparse
from collections import OrderedDict
from tracker import CentroidTracker

RED = (0, 0, 255)
GREEN = (0, 255, 0)
PPF_to_MPH = 15.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@', description="")

    parser.add_argument('--video-file', default='traffic.mp4', help='')
    parser.add_argument('--blur-window', type=int, default=5, help='')
    parser.add_argument('--threshold', type=int, default=25, help='')
    parser.add_argument('--object-area', type=int, default=180, help='')
    parser.add_argument('--invalid-length', type=int, default=3, help='')
    parser.add_argument('--dilation-kernel', type=int, default=3, help='')
    parser.add_argument('--dilation-iter', type=int, default=3, help='')
    parser.add_argument('--heatmap-threshold', type=int, default=3, help='')
    parser.add_argument('--no-heatmap', action="store_true", help='')
    parser.add_argument('--no-car-detection', action="store_true", help='')
    parser.add_argument('--no-speed-check', action="store_true", help='')
    parser.add_argument('--speed-limit', type=int, default=60, help='')
    parser.add_argument('--save-video', default=None, help='')
   
    args = parser.parse_args()

    blur_window = args.blur_window
    threshold = args.threshold
    object_area = args.object_area
    invalid_length = args.invalid_length
    dilation_kernel = np.ones((args.dilation_kernel, args.dilation_kernel), 'uint8')
    dilation_iter = args.dilation_iter
    heatmap_threshold = args.heatmap_threshold
    video_file = args.video_file

    ct = CentroidTracker(500)

    cap = cv2.VideoCapture(video_file)
    first_iteration_indicator = True
    while cap.isOpened():
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (blur_window, blur_window), 0)

        if first_iteration_indicator:
            last_frame = gray
            accum_image = np.zeros_like(gray)
            first_iteration_indicator = False
            last_tracked_boxes = OrderedDict()
            last_tracked_centroids = OrderedDict()
            continue
        
        delta_frame = cv2.absdiff(last_frame, gray)
        last_frame = gray
        thresh1 = cv2.threshold(delta_frame, threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh1, dilation_kernel, iterations=dilation_iter)
        if thresh.max() == 0: continue

        if not args.no_car_detection or not args.no_speed_check:
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            total_number_cars = 0
            rects = []
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if w < invalid_length or h < invalid_length:
                    continue
                if not args.no_car_detection:
                    total_number_cars += 1
                    cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 2)
                if not args.no_speed_check:
                    rects.append([x, y, x+h, y+w])

            if not args.no_speed_check:
                ct.update(rects)
                tracked_boxes = ct.boxes
                tracked_centroids = ct.objects
                for objectID in tracked_centroids.keys():
                    if not objectID in last_tracked_centroids.keys():
                        continue
                    speed_pixel_per_frame = np.sqrt((tracked_centroids[objectID][0]-last_tracked_centroids[objectID][0])**2 + 
                                                    (tracked_centroids[objectID][1]-last_tracked_centroids[objectID][1])**2)
                    speed_MPH = speed_pixel_per_frame * PPF_to_MPH
                    if speed_MPH > args.speed_limit:
                        cv2.rectangle(frame, (tracked_boxes[objectID][0], tracked_boxes[objectID][1]), (tracked_boxes[objectID][2], tracked_boxes[objectID][3]), RED, 2)
                        # cv2.putText(frame, "{:4.0f} mph".format(speed_MPH) , (tracked_boxes[objectID][0]-5, tracked_boxes[objectID][1]-5), cv2.FONT_HERSHEY_PLAIN, 1, RED, 2)
                last_tracked_boxes = tracked_boxes.copy()
                last_tracked_centroids = tracked_centroids.copy()
          
        if not args.no_heatmap:
            accum_image = cv2.addWeighted(accum_image, 0.98, thresh, 0.1, 0.0)
            color_image_video = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
            frame = cv2.addWeighted(color_image_video, 0.5, frame, 0.8, 0.0)
        if not args.no_car_detection:
            cv2.putText(frame, "Total Number of Cars: {}".format(total_number_cars) , (800, 700), cv2.FONT_HERSHEY_PLAIN, 2, GREEN, 2)            

        cv2.imshow("Car counter", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()