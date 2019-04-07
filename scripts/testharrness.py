# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# This script will read the intances that are 
# available in ECS

# import 3rd party / built-in modules
import boto3
import uuid
import datetime

# import custom modules
import printinfo
import notification

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

# -- Function: Get List of Starting Instances & Print on Screen
#               Input: ec2 Resrouce 
#               Return: List of Starting Instances
def GetListOfStartingInstances(ec2Res):
        # Get all running instances in the environment
        ec2Instances = ec2Res.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['pending']}])
        instanceList = [instance for instance in ec2Instances]
        return instanceList

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

# -- Function:  Calculate the timeout value for the tests based on
#               i.   Number of instances to terminate
#               ii.  ELB Health Checks
#               iii. Auto Scale Settings
#               Input: Number of Instances to Terminate
#               Return: List of Instance IDs to Terminatated
def CalculateTimeOutValue():
        # Setup Test Timeout value in Seconds
        testTimeoutValue = 0

#-------------------------------------------
# Print Start Title on Screen
printinfo.PrintTitle()

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get List of Running Instances
instanceRunList = GetListOfRunningInstances(ec2Resource)

# Get Number of Instances Running
numInstancesRunning = len(instanceRunList)

# Print the Instance Information on Screen
if numInstancesRunning > 0 :
        printinfo.PrintInformationToScreen(instanceRunList)
else:
        print ("""\
There are ZERO instances running in your environment
        """)
        print ("============================================================")

# Ask user for input to select the number of machines to disrupt
iNumberInstancesToDisrupt = -1
if numInstancesRunning > 0:       
        while iNumberInstancesToDisrupt < 0:
                iNumberInstancesToDisrupt = int(input ("How many instances do you want to disrupt (MAX: %s, Min: 0):" % len(instanceRunList)))
                if iNumberInstancesToDisrupt > len(instanceRunList):
                        print ("You input more than the max number of machines available in the environment")
                        iNumberInstancesToDisrupt = -1
                else:
                        print ("You requested to disrupt %s instances" %iNumberInstancesToDisrupt)

# Select instances at random from the list to disrupt
print ("============================================================")

if iNumberInstancesToDisrupt > 0 and numInstancesRunning > 0:
        # Select Instances to Terminate
        disruptList = RandomlySelectInstances(instanceRunList,iNumberInstancesToDisrupt)

        # Terminate Instances
        TerminateInstances(ec2Resource,disruptList)


        # Start Time to determine how long it takes to recover the system
        testStartTime = datetime.datetime.now()
        

        # Get List of Running Instances
        instanceRunList = GetListOfRunningInstances(ec2Resource)
        testStartNumRunning = runningListNum = len(instanceRunList)

        # Print Instance Information to Screen
        printinfo.PrintInformationToScreen(instanceRunList)

        # Monitor the environment until machines have been recovered
        print ("\n\nAWS HA is recovering your instances, please wait for this to complete")
        print ("")
        timedout=False
        # Calculate the timeout value based on the number of instances to terminate (in Seconds)
        testTimeoutValue = 150 * iNumberInstancesToDisrupt
        print ("\n *** TIMEOUT SET TO %s ***" % testTimeoutValue)
        while runningListNum != numInstancesRunning and timedout == False:
                
                # Get the list of instances in a starting state
                startingList = GetListOfStartingInstances(ec2Resource)

                # Get the list of instances in a running state
                instanceRunList = GetListOfRunningInstances(ec2Resource)

                # Get the number of instances in a list
                runningListNum = len(instanceRunList)
                startingListNum = len(startingList)

                # Add a time out to ensure the testing does not run forever
                if datetime.datetime.now() > testStartTime + datetime.timedelta(seconds=testTimeoutValue):
                        timedout = True
                        print ("Timed Out !!!!")
        else:
                # Perform Calculations when the tests stop
                testStopTime = datetime.datetime.now()
                instancesRestarted = runningListNum - testStartNumRunning
                elapsedTime = testStopTime - testStartTime
                if not timedout:
                        notifyMessage = {
                                "starttime" : '{0:%Y-%m-%d %H:%M:%S}'.format(testStartTime),
                                "endtime":'{0:%Y-%m-%d %H:%M:%S}'.format(testStopTime),
                                "instancesrestarted":instancesRestarted,
                        }
                        printinfo.PrintTestResults(testStartTime,testStopTime, instancesRestarted, elapsedTime)
                        notification.SendEmailNotification(notifyMessage)
                        print ("The test has now stopped. There are %s instances running" % runningListNum)
                else:
                        print ("The test has TIMEDOUT")
print ("============================================================")

