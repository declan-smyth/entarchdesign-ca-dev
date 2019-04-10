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
import botocore
import json

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an Auto Scale Client
autoScaleClient = boto3.client('autoscaling')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Setup an ELB Client
elbv2Client = boto3.client('elbv2')

###############################################################################
# Function Definitions
###############################################################################

###############################################################################
# -- Function: Get List of ALL Running Instances running in the EC2 environment
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListOfRunningInstances():
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList


###############################################################################
# -- Function: Get List of running instances based on a list of InstanceIDs
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListOfRunningInstancesById(instanceIds):
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}], InstanceIds=instanceIds)
        instanceList = [instance for instance in ec2Instances]
        instanceIdList = [instance.id for instance in ec2Instances]
        return instanceList, instanceIdList


###############################################################################
# -- Function: Get List of  Instances Based on a list of IDs (All Statuses)
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListInstancesById(instanceIds):
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(InstanceIds=instanceIds)
        instanceList = [instance for instance in ec2Instances]
        return instanceList


###############################################################################
# -- Function: Get List of Starting Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Starting Instances
def GetListOfPendingInstances():
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['pending']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList

###############################################################################
# -- Function: Get List of Starting Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Starting Instances
def GetListOfPendingInstancesById(instanceIds):
        # Get all running instances in the environment
        ec2Instances = ec2Resource.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['pending']}],InstanceIds=instanceIds)
        instanceList = [instance for instance in ec2Instances]
        return instanceList



###############################################################################
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


###############################################################################
# -- Function: Get List of instances IDs from the autoscale group
#               Input: Autoscale Group Name
#               Return: List of Instance IDs in the Auto Scaling Group
def GetAutoScaleGroupInstancesIDs(groupname):
    # Get all instances in an autoscaling group
    instanceIDList=[]
    autoScaleInfo = autoScaleClient.describe_auto_scaling_groups(AutoScalingGroupNames=[groupname])
    for i in autoScaleInfo['AutoScalingGroups']:
        for instance in i["Instances"]:
                instanceIDList.append(instance["InstanceId"])
    return  instanceIDList

###############################################################################
# -- Function: Get List of instances IDs from the autoscale group
#               Input: Autoscale Group Name
#               Return: List of Instance IDs in the Auto Scaling Group
def GetInstancesIDFromTargetInstances(instances):
        instanceIDList=[]
        for i in instances:
                instanceIDList.append(i['Target']['Id'])
        return instanceIDList



###############################################################################
# -- Function: Get List of instances in an autoscale group
#               Input: Autoscale Group Name
#               Return: Desired Size of Group
def GetAutoScaleInformation(groupname):
        autoScaleInfo = autoScaleClient.describe_auto_scaling_groups(AutoScalingGroupNames=[groupname])
        for i in autoScaleInfo['AutoScalingGroups']:
            group_size_info= dict(desired=i['DesiredCapacity'], max=i['MaxSize'],min=i['MinSize'])
        return group_size_info 

###############################################################################
# -- Function: Get Autoscale Target Group
#               Input: Autoscale Group Name
#               Return: ARN of Target Group
def GetAutoScaleGroupTargetGrp(groupname):
        autoScaleInfo = autoScaleClient.describe_load_balancer_target_groups(AutoScalingGroupName=groupname)
        for i in autoScaleInfo['LoadBalancerTargetGroups']:
            TargetGroupARN = i['LoadBalancerTargetGroupARN']
        return TargetGroupARN


###############################################################################
# -- Function: Get Target Group Health Information
#               Input:  Target Group ARN
#               Return: ARN of Target Group
def GetTargetGrpInstances(TargetGroupARN):
        targetGrpHealthInfo = elbv2Client.describe_target_health(TargetGroupArn=TargetGroupARN)
        
        target_group_instances = targetGrpHealthInfo['TargetHealthDescriptions']  
        
        target_group_instances_ids = []

        for instance in targetGrpHealthInfo['TargetHealthDescriptions']:
                target_group_instances_ids.append(instance['Target']['Id'])

        return target_group_instances_ids, target_group_instances

 