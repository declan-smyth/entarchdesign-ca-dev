# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# This script will read the intances that are 
# available in ECS
#
import boto3
import uuid

print ("""\
********************************************

       Welcome to the Chaos Monkey 
            AWS Test Harness

********************************************
""")

#-------------------------------------------
# Function Definitions
#-------------------------------------------

# -- Function: Get List of Running Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Running Instances
def GetListOfRunningInstances(ec2Res):
        # Get all running instances in the environment
        ec2Instances = ec2Res.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList

# -- Function: Print on Screen
#               Input: List of Instances
#               Return: None
def PrintInformationToScreen(instLst):
        # Print the list of Instances to the screen
        for instance in instLst:
                print(instance.id, instance.public_ip_address, instance.state["Name"])

# -- Function: Terminate Random Instances and Instance IDs
#               Input: Number of Instances to Terminate
#               Return: List of Instance IDs to Terminatated
def TerminateInstances(instLst):
        pass

#-------------------------------------------

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get List of Running Instances
instanceRunList = GetListOfRunningInstances(ec2Resource)

if len(instanceRunList) > 0 :
        # Print out available instances by quering the Reservations and Instances dict
        print ("""\
There are %s instances running your environment

"""
        % len(instanceRunList))
else:
        print ("""\
There are ZERO instances running in your environment
        """)

# Print the list of Instances that are running
PrintInformationToScreen(instanceRunList)


print ("============================================================")

# Ask user for input to select the number of machines to disrupt
iNumberInstancesToDisrupt = -1
while iNumberInstancesToDisrupt < 0:
        iNumberInstancesToDisrupt = int(input ("How many instances do you want to disrupt (MAX: %s, Min: 0):" % len(instanceRunList)))
        if iNumberInstancesToDisrupt > len(instanceRunList):
                print ("You input more than the max number of machines available in the environment")
                iNumberInstancesToDisrupt = -1
        else:
                print ("You requested to disrupt %s instances" %iNumberInstancesToDisrupt)

# Select two instances at random from the list to disrupt
print ("============================================================")
count=0
disruptList = list()
from random import randint
while count <= (iNumberInstancesToDisrupt -1):
        disruptList.append (instanceRunList[randint(0, len(instanceRunList))-1].id)
        count+=1

# Terminate the the randomly selected instances
if iNumberInstancesToDisrupt > 0:
        print ("The following instances are now being TERMINATED")
        for dInstance in disruptList:
                print (dInstance)
        ec2Resource.instances.filter(InstanceIds=disruptList).terminate()
        print ("============================================================")

