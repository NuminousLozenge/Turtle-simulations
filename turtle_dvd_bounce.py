#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from std_srvs.srv import Empty
import math



'''
IMPORTANT
copy paste below commands in terminal
after the command
rosrun turtlesim turtlesim_node
'''



'''

rosservice call /kill "turtle1"
rosservice call /clear
rosservice call /spawn 7.544444561004639 5.544444561004639 0 "turtle1"
rosrun abhiyaan_package turtle_dvd_bounce.py

''' 

X = [0.0 for i in range(17)]
Y = [0.0 for i in range(17)]
tick = 1

def spawn_turtle(x,y,theta,counter,vx,vy):
	if(counter<=16):
		spawner = rospy.ServiceProxy('/spawn', Spawn)
		response = spawner(x,y,theta,f"turtle{counter}")
	return [vx,vy]



			
def callback(Pose): # callback function for turtle1
    global X
    global Y
    global tick
    X[tick] = Pose.x - 5.544444561004639  #shifting origin to centre of window
    Y[tick] = Pose.y - 5.544444561004639
    tick = (tick%16) +1
    #rospy.loginfo(X1)

 
def turtle_bounce(): 
	

	for i in range(1,17):
		rospy.Subscriber(f'/turtle{i}/pose',Pose, callback)
		
	 
	vx = [1 for i in range(17)]#initial x vel of turtle1 
	vy = [2 for i in range(17)] #initial y vel of turtle1	
	rospy.init_node('turtlesim_bounce', anonymous=True)
	rate = rospy.Rate(150)
	vel = Twist()
	counter = 2

	while not rospy.is_shutdown():
		for i in range(1,17):
		
			Vx = vx[i]
			Vy = vy[i]
			X1 = X[i]
			Y1 = Y[i]
			
			pub = rospy.Publisher(f'/turtle{i}/cmd_vel',Twist, queue_size=0) 
			if(X1 >= 5 and Vx>0):
				Vx = -Vx
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639,0,counter,Vx,Vy)
				
				if( counter == i):
					Vy = -Vy
					
				counter += 1
				
			if(X1 <= -5 and Vx<0):
				Vx = -Vx
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639,0,counter,Vx,Vy)
				
				if( counter == i):
					Vy = -Vy
				
				counter += 1
			if(Y1 >= 5 and Vy>0):
				Vy = -Vy
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639,0,counter,Vx,Vy)
				
				if( counter == i):
					Vx = -Vx				
				
				counter += 1
			if(Y1 <= -5 and Vy<0):
				Vy = -Vy
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639,0,counter,Vx,Vy)
				
				if( counter == i):
					Vx = -Vx				
				
				counter += 1
				
				
			#modifying velocities of turtle1     	 
			vel.linear.x = Vx
			vel.linear.y = Vy
			vel.linear.z = 0
			vel.angular.x = 0
			vel.angular.y = 0
			vel.angular.z = 0

			#rospy.loginfo("X1 = %f",X1)
			#rospy.loginfo("Y1 = %f",Y1)						
			pub.publish(vel)
		rate.sleep()


 
 
if __name__ == '__main__':
    try:
    	clear_bg = rospy.ServiceProxy('clear', Empty)
    	clear_bg()
    	turtle_bounce()

    except rospy.ROSInterruptException:
        pass
               
        
