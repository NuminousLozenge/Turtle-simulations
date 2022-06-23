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
rosrun abhiyaan_package turtle_dvd_bounce_2.py

''' 
t_num = 16  # number of turtles
X =  [0] * (t_num+1)  #[0 for i in range(17)]
Y =  [0] * (t_num+1)


def spawn_turtle(x,y,theta,counter,vx,vy):
	global t_num
	if(counter<=t_num):
		spawner = rospy.ServiceProxy('/spawn', Spawn)
		response = spawner(x,y,theta,f"turtle{counter}")
	return vx, vy


class makeCall:
	
	def __init__(self, index):
		self.index = index 	
			
	def callback(self,Pose): # callback function for turtle1
	    global X
	    global Y
	    X[self.index] = Pose.x - 5.544444561004639  #shifting origin to centre of window
	    Y[self.index] = Pose.y - 5.544444561004639
	    #rospy.loginfo(X1)

 
def turtle_bounce():
	global t_num 
	
	mcb = [0 for i in range(t_num+1)]
	
	for i in range(t_num+1):
		mcb[i]  = makeCall(i)

	
	for i in range(1,t_num+1):
		rospy.Subscriber(f'/turtle{i}/pose',Pose, mcb[i].callback)
	
	rospy.init_node('turtlesim_bounce', anonymous=True)
	rate = rospy.Rate(1500)
	vx = [1.5 for i in range(t_num+1)]
	vy = [2 for i in range(t_num+1)]
	counter = 2
	spawner = 1
	d = 0.1
	vel = Twist()
	
	pub = [rospy.Publisher(f'/turtle{i}/cmd_vel',Twist, queue_size=10)  for i in range(0,t_num+5)]

	while not rospy.is_shutdown():
		
		
		for i in range(1,t_num+1):
			X1 = X[i]
			Y1 = Y[i] 
			Vx = vx[i]
			Vy = vy[i]
			
			flag = 0
			
			if(X1 >= 5 and Vx>0):
				Vx = -Vx
				spawn_turtle(X1+5.544444561004639-d,Y1+5.544444561004639,0,counter,Vx,Vy)
				spawner = i	
				flag = 1
													
				counter += 1
				
				
			if(X1 <= -5 and Vx<0):
				Vx = -Vx
				spawn_turtle(X1+5.544444561004639+d,Y1+5.544444561004639,0,counter,Vx,Vy)
				spawner = i
				flag = 1
				counter += 1
							
			if(Y1 >= 5 and Vy>0):
				Vy = -Vy
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639-d,0,counter,Vx,Vy)
				spawner = i				
				flag = 1
				counter += 1
				
			if(Y1 <= -5 and Vy<0):
				Vy = -Vy
				spawn_turtle(X1+5.544444561004639,Y1+5.544444561004639+d,0,counter,Vx,Vy)
				spawner = i
				flag = 1				
				counter += 1
				
			
			#print(spawner,counter)
			
			if(counter<=t_num and flag == 1):
				vx[counter-1] = -vx[spawner]
				vy[counter-1] = -vy[spawner]
				
			
			flag = 0	
			vx[i] = Vx
			vy[i] = Vy
		
		for i in range(1, t_num + 1):
			vel.linear.x = vx[i]
			vel.linear.y = vy[i]
			vel.linear.z = 0
			vel.angular.x = 0
			vel.angular.y = 0
			vel.angular.z = 0
			pub[i].publish(vel)
			
		rate.sleep()

"""
- use some ide, pycharm - vscode
- kill the older turtles
- look at pep 8
- try to earse the old paths
- put constabts
- append publishers dynamically
"""

"""
class for turtles
"""
 
if __name__ == '__main__':
    try:
    	clear_bg = rospy.ServiceProxy('clear', Empty)
    	clear_bg()
    	turtle_bounce()

    except rospy.ROSInterruptException:
        pass
               
        
            
