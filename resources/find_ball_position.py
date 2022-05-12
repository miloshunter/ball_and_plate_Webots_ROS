from ossaudiodev import control_labels
import sys
import os
from optparse import OptionParser

import rospy
import sensor_msgs.msg
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np




if __name__ == '__main__':

    rospy.init_node('ball_position')


    br = CvBridge()

    coord_publisher = rospy.Publisher('ball_coordinates', Point, queue_size=10)
    #rospy.init_node('ball_position_detector')

    def detect_and_draw(imgmsg):
        frame = br.imgmsg_to_cv2(imgmsg, "8UC3")
        # allocate temporary images

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV 
        lower_red = np.array([150, 50, 50])
        upper_red = np.array([180, 255, 255])

        imgThreshHigh = cv2.inRange(hsv, lower_red, upper_red)
        thresh = imgThreshHigh.copy()

        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        #cv2.imshow('filter', thresh)

        countours,_ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        if countours:
            M = cv2.moments(countours[0])
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            coord = cx, cy 

            cx -= frame.shape[1]/2
            cy -= frame.shape[0]/2
            cy *= -1
            
            coord = cx, cy 

            #print(coord)

            point = Point()
            point.x = cx
            point.y = cy
            point.z = 0

            coord_publisher.publish(point)

        else:
            #print("Nije pronasao konturu")
            pass

        #cv2.imshow("result", frame)
        #cv2.waitKey(1)

    rospy.Subscriber('webots_camera', sensor_msgs.msg.Image, detect_and_draw)
    rospy.spin()