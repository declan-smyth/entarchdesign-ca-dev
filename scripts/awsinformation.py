# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# This script will send notification infomration
# to AWS SNS and CloudWatch 
# available in ECS
# ######################################

import boto3
import json

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an Auto Scale Client
autoScaleClient = boto3.client('autoscaling')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

#-------------------------------------------
# Function Definitions
#-------------------------------------------

# -- Function: Get List of Running Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListOfRunningInstances():
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList

# -- Function: Get List of Running Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListInstancesById(instanceIds):
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(InstanceIds=instanceIds)
        instanceList = [instance for instance in ec2Instances]
        return instanceList

# -- Function: Get List of Starting Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Starting Instances
def GetListOfPendingInstances():
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['pending']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList

# -- Function: Get List of instances in an autoscale group
#               Input: Autoscale Group Name
#               Return: List of Dictionary values with instance Information
def GetAutoScaleGroupInstances(groupname):
    # Get all instances in an autoscaling group
    instanceList=[]
    autoScaleInfo = autoScaleClient.describe_auto_scaling_groups(AutoScalingGroupNames=[groupname])
    for i in autoScaleInfo['AutoScalingGroups']:
        instanceList = [instance for instance in i["Instances"]]
    return instanceList


# -- Function: Get List of instances in an autoscale group
#               Input: Autoscale Group Name
#               Return: List of Dictionary values with instance Information
def GetAutoScaleGroupInstancesByID(instanceIDs):
    # Get all instances in an autoscaling group
    instanceList=[]
    autoScaleInfo = autoScaleClient.describe_auto_scaling_instances(InstanceIds=[instanceIDs])
    for i in autoScaleInfo['AutoScalingInstances']:
        instanceList = [instance for instance in i["Instances"]]
    return instanceList


# -- Function: Get List of instances in an autoscale group
#               Input: Autoscale Group Name
#               Return: Desired Size of Group
def GetAutoScaleGroupSize(groupname):
        autoScaleInfo = autoScaleClient.describe_auto_scaling_groups(AutoScalingGroupNames=[groupname])
        
        for i in autoScaleInfo['AutoScalingGroups']:
            groupsize = dict(desired=i['DesiredCapacity'], max=i['MaxSize'],min=i['MinSize'])
        return groupsize

# -- Function: Get Autoscale Target Group
#               Input: Autoscale Group Name
#               Return: ARN of Target Group
def GetAutoScaleGroupTargetGrp(groupname):
        autoScaleInfo = autoScaleClient.describe_load_balancer_target_groups(AutoScalingGroupName=groupname)
        for i in autoScaleInfo['LoadBalancerTargetGroups']:
            TargetGroupARN = i['LoadBalancerTargetGroupARN']
        return TargetGroupARN

