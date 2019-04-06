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

# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintInformationToScreen(instLst):
        print ("""\
There are %s instances running your environment
""" % len(instLst))

        # Print the list of Instances to the screen
        for instance in instLst:
                print(instance.id, instance.public_ip_address, instance.state["Name"])

# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintListToScreen(aLst):
        # Print the list of Instances to the screen
        for item in aLst:
                print(item)

# -- Function: Randomly Select Instances to disrupt.
#              The function will check if the id of the instance is in the list already
#
#               Input: List of Instances, Number to Select
#               Return: Selected Instance IDs
def RandomlySelectInstances(instLst, numSelected):
        count=0
        disruptList = list()
        from random import randint
        while count <= (numSelected -1):
                id = instLst[randint(0, len(instLst)-1)].id
                if ( id not in disruptList):
                        disruptList.append (id)
                        count+=1
        return disruptList


# -- Function: Terminate Random Instances and Instance IDs
#               Input: Number of Instances to Terminate
#               Return: List of Instance IDs to Terminatated
def TerminateInstances(ec2Res,terminateLst):
        print ("The following instances are now being TERMINATED")
        for instance in terminateLst:
                print (instance)
        ec2Res.instances.filter(InstanceIds=terminateLst).terminate()

#-------------------------------------------

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get List of Running Instances
instanceRunList = GetListOfRunningInstances(ec2Resource)

# Print the Instance Information on Screen
if len(instanceRunList) > 0 :
        PrintInformationToScreen(instanceRunList)
else:
        print ("""\
There are ZERO instances running in your environment
        """)
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

# Select instances at random from the list to disrupt
print ("============================================================")

if iNumberInstancesToDisrupt > 0:
        # Select Instances to Terminate
        disruptList = RandomlySelectInstances(instanceRunList,iNumberInstancesToDisrupt)

        # Terminate Instances
        TerminateInstances(ec2Resource,disruptList)

        # Get List of Running Instances
        instanceRunList = GetListOfRunningInstances(ec2Resource)

        # Print Instance Information to Screen
        PrintInformationToScreen(instanceRunList)
