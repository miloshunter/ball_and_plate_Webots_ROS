"""python_forward controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from distutils.cmd import Command
from controller import Robot
from math import sqrt
from geometry_msgs.msg import Point
import rospy

import threading


# create the Robot instance.
robot = Robot()
TIME_STEP = 8

class Ball_and_Plate:
    def __init__(self):

        self.commands = []
        self.current_time = robot.getTime()
        self.last_time = robot.getTime()

        """ Constants """
        self.K_p = 0.2
        self.K_i = 0.0
        self.K_d = 0.0
        
        self.cummulative_error_x = 0
        self.cummulative_error_y = 0
        self.last_error_x = 0
        self.last_error_y = 0

        
        """ Get and init all of the necesary sensors/actuators """
        self.motorX = robot.getDevice('motor_pitch')
        self.motorY = robot.getDevice('motor_roll')
       
    def regulate_PID_x(self, x):
        #print("Greska po X = ", x)
        x_scaled = x/310
        #print("Skalirana greska po X = ", x_scaled)
        
        elapsed_time = self.current_time - self.last_time
        self.last_time = self.current_time
        
        error_x = 0 - x_scaled
        
        self.cummulative_error_x += error_x*elapsed_time
        
        if elapsed_time:
            rate_error = (error_x - self.last_error_x)/elapsed_time
        
            angle = error_x*self.K_p \
                    + self.cummulative_error_x*self.K_i \
                    + rate_error*self.K_d
            
            if angle > 1:
                angle = 1
            if angle < -1:
                angle = -1
            
            self.motorX.setPosition(angle)
            
            self.last_error_x = error_x

        
    def regulate_PID_y(self, y):
        #print("Greska po y = ", y)
        y_scaled = y/310
        #print("Skalirana greska po y = ", y_scaled)
        
        elapsed_time = self.current_time - self.last_time
        self.last_time = self.current_time
        
        error_y = 0 - y_scaled
        
        self.cummulative_error_y += error_y*elapsed_time
                
        if elapsed_time:
            rate_error = (error_y - self.last_error_y)/elapsed_time
        
            angle = error_y*self.K_p \
                    + self.cummulative_error_y*self.K_i \
                    + rate_error*self.K_d
            
            if angle > 1:
                angle = 1
            if angle < -1:
                angle = -1
            
            self.motorY.setPosition(angle)
            
            self.last_error_y = error_y

        
        #self.error_y = 0 - y
            
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

myRobot = Ball_and_Plate()

# Mora u novom Thread-u jer rospy.spin() blokira dalji rad
# Ovako se ROS Subscriber izvrsava u glavnom thread-u, a redovno azuriranje
# simulacije se izvrsava u posebnom thread-u (robot.step(timestep))
class WebotsThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):

        # Main loop:
        # - perform simulation steps until Webots is stopping the controller
        while robot.step(timestep) != -1:
            myRobot.current_time = robot.getTime()

            pass

webots_thread = WebotsThread(myRobot)
webots_thread.start()

# Make ROS Subscriber in main thread
def sub_callback(data):
    myRobot.regulate_PID_x(data.x)
    myRobot.regulate_PID_y(data.y)
    

rospy.init_node('ball_and_plate_driver')

rospy.Subscriber('ball_coordinates', Point, sub_callback)

rospy.spin()



# Enter here exit cleanup code.