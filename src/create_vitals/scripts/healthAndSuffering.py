#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32,Float64
import math
import numpy as np

class SufferingAndHealth:

	def __init__(self):
		self.probSuff_total_pub = rospy.Publisher('/probSuffering_total', Float32, queue_size=10)
		self.robotHealth_pub = rospy.Publisher('/robotHealth', Float32, queue_size = 10)
		self.rv_magROC_ProbSuff_sub = rospy.Subscriber('/probSuffering_rv_magROC', Float64, self.ps_magROC_callback)
		self.rv_velocityEvent_ProbSuff_sub = rospy.Subscriber('/probSuffering_rv_velocityEvent', Float64, self.ps_velocityEvent_callback)
		self.rv_odomPosErrEvent_ProbSuff_sub = rospy.Subscriber('/probSuffering_rv_odomPosErrEvent', Float64, self.ps_poserr_callback)
		self.rv_linAccROC_ProbSuff_sub = rospy.Subscriber('/probSuffering_rv_linAccROC', Float64, self.ps_linacc_callback)
		self.rv_snr_ProbSuff_sub = rospy.Subscriber('/probSuffering_rv_snr', Float64, self.ps_snr_callback)

		self.totalProbabilityOfSuffering = rospy.Timer(rospy.Duration(0.5),self.probSuff_callback)

		self.probabilityOfsufferingVector = np.array([0.,0.,0.,0.,0.]) # for 5 vitals
		self.robotHealthVector = []
		self.healthTimeWindow = 4 #number of time steps that the robot health is calculated over.

	def ps_magROC_callback(self,msg):
		# print("1",msg.data)
		self.probabilityOfsufferingVector[0] = msg.data
	def ps_velocityEvent_callback(self,msg):
		# print("2",msg.data)
		self.probabilityOfsufferingVector[1] = msg.data
	def ps_poserr_callback(self,msg):
		# print("3",msg.data)
		self.probabilityOfsufferingVector[2] = msg.data
	def ps_linacc_callback(self,msg):
		# print("4",msg.data)
		self.probabilityOfsufferingVector[3] = msg.data
	def ps_snr_callback(self,msg):
		# print("5",msg.data)
		self.probabilityOfsufferingVector[4] = msg.data

	def probSuff_callback(self, event=None):

		print("Vector of values is ",self.probabilityOfsufferingVector)

		probSuff = Float32()
		probSuff.data = self.probabilityOfsufferingVector.sum()/len(self.probabilityOfsufferingVector)

		self.probSuff_total_pub.publish(probSuff)
		
		robotHealth = Float32()
		if(len(self.robotHealthVector)<self.healthTimeWindow):
			if(probSuff.data>0):
				self.robotHealthVector.append(probSuff.data*np.log10(probSuff.data))
			robotHealth.data = (2.0)/2.0
		else:
			robotHealth.data = ((1.0+(sum(self.robotHealthVector) + (1 - probSuff.data)))/2.0)
			if(probSuff.data>0):
				self.robotHealthVector.pop(0)
				self.robotHealthVector.append(probSuff.data*np.log10(probSuff.data))

		# robotHealth = Float64()
		# if(len(self.robotHealthVector)<self.healthTimeWindow):
		# 	if(probSuff.data>=0):
		# 		self.robotHealthVector.append(1-probSuff.data)
		# 	robotHealth.data = 0
		# else:
		# 	robotHealth.data = sum(self.robotHealthVector)/self.healthTimeWindow
		# 	if(probSuff.data>0):
		# 		self.robotHealthVector.pop(0)
		# 		self.robotHealthVector.append(1-probSuff.data)
		self.robotHealth_pub.publish(robotHealth)



rospy.init_node('sufferingAndHealth')
createEvents = SufferingAndHealth()
rospy.spin()