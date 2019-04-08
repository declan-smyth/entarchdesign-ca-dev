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
import time 

# import custom modules
import printinfo
import notification
import awsinformation

#-------------------------------------------
# AWS Configuration Information
#-------------------------------------------
awsConfiguration = {
        "autoscalegroup_name": "EAD-AUTOSCALE-DECLANS-HA",
        "topic_arn": "arn:aws:sns:eu-west-1:197110341471:AWS-Test-Results"
}


#-------------------------------------------
# Function Definitions
#-------------------------------------------

# -- Function: Randomly Select Instances to disrupt.
#              The function will check if the id of the instance is in the list already
#
#               Input: List of Instances, Number to Select
#               Return: Selected Instance IDs
def RandomlySelectInstanceID(instLst, numSelected):
        count=0
        disruptList = list()
        from random import randint
        while count <= (numSelected -1):
                id = instLst[randint(0, len(instLst)-1)]["InstanceId"]
                if ( id not in disruptList):
                        disruptList.append (id)
                        count+=1
        return disruptList

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
        testTimeoutValue = 150 * iNumberInstancesToDisrupt
        print ("\n *** TEST TIMEOUT SET TO %s seconds ***" % testTimeoutValue)
        return testTimeoutValue 

# -- Function:  Ask the user for the number of instances to disrupt
#               Input: None
#               Return: List of Instance IDs to Terminatated
def GetUserInput(max_running):
        iNumberInstancesToDisrupt = -1
        while iNumberInstancesToDisrupt < 0:
                try:
                        iNumberInstancesToDisrupt = int(input ("How many instances do you want to disrupt (MAX: %s, Min: 0):" % max_running))
                        if iNumberInstancesToDisrupt > len(instanceRunList):
                                print ("You input more than the max number of machines available in the environment")
                                iNumberInstancesToDisrupt = -1
                        else:
                                print ("You requested to disrupt %s instances" %iNumberInstancesToDisrupt)
                except ValueError:
                        print ("An error was encountered with your input...\n Please provide an integer between 0 and %s "  % max_running)
                        iNumberInstancesToDisrupt = -1
        return iNumberInstancesToDisrupt

#-------------------------------------------
# Print Start Title on Screen
printinfo.PrintTitle()

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get List of Running Instances
instanceRunList = awsinformation.GetListOfRunningInstances()

# Get Number of Instances Running
numInstancesRunning = len(instanceRunList)

# Get List of instances in the Auto Scale Group
instanceListAutoScaleGrp = awsinformation.GetAutoScaleGroupInstances(awsConfiguration["autoscalegroup_name"])

# Get Auto Scale Group Size information
autoScaleGroupSize = awsinformation.GetAutoScaleGroupSize(awsConfiguration["autoscalegroup_name"])

# Print the Instance Information on Screen
if numInstancesRunning > 0 :
       printinfo.PrintSAutoScaleGroupInfo(instanceListAutoScaleGrp)
       #printinfo.PrintInformationToScreen(instanceRunList)
else:
        print ("""\
There are ZERO instances running in your environment
        """)
        print ("============================================================")

# Ask user for input to select the number of machines to disrupt
if numInstancesRunning > 0:       
        iNumberInstancesToDisrupt = GetUserInput(len(instanceRunList))

# Select instances at random from the list to disrupt
print ("============================================================")

if iNumberInstancesToDisrupt > 0 and numInstancesRunning > 0:
        # Select Instances to Terminate
        disruptList = RandomlySelectInstances(instanceRunList,iNumberInstancesToDisrupt)
        
        # Get the number of instanace IDs selected to be terminated
        numInstancesToTerminate = len(disruptList)

        # Calculate the timeout value based on the number of instances to terminate (in Seconds)
        testTimeoutValue = CalculateTimeOutValue()
        timedout=False

        # Terminate Instances
        TerminateInstances(ec2Resource,disruptList)

        # Start Time to determine how long it takes to recover the system
        testStartTime = datetime.datetime.now()

        # Monitor the environment until machines have been recovered
        print ("\n\nAWS HA is recovering your instances, please wait for this to complete\n")

        # Get List of Running Instances
        instanceRunList = awsinformation.GetListOfRunningInstances()
        testStartNumRunning = runningListNum = len(instanceRunList)

        # Print Instance Information to Screen
        printinfo.PrintInformationToScreen(instanceRunList)

        
        while runningListNum != numInstancesRunning and timedout == False:
                
                # Get the list of instances in a starting state
                startingList = awsinformation.GetListOfPendingInstances()

                # Get the list of instances in a running state
                instanceRunList = awsinformation.GetListOfRunningInstances()

                # Get the number of instances in a list
                runningListNum = len(instanceRunList)
                startingListNum = len(startingList)

                # Add a time out to ensure the testing does not run forever
                if datetime.datetime.now() > testStartTime + datetime.timedelta(seconds=testTimeoutValue):
                        timedout = True
                        print ("Timed Out !!!!")
                
                time.sleep(60)
        else:
                # Perform Calculations when the tests stop
                testStopTime = datetime.datetime.now()

                # Get the number of instances that were created
                instancesRestarted = runningListNum - testStartNumRunning

                # Calculate the elapsed time for the test
                elapsedTime = testStopTime - testStartTime

                # Check if the test timed out or completed within the expected time
                if not timedout:
                        testStatus="PASSED"
                        notifyMessage = {
                                "starttime" : '{0:%Y-%m-%d %H:%M:%S}'.format(testStartTime),
                                "endtime":'{0:%Y-%m-%d %H:%M:%S}'.format(testStopTime),
                                "instancesrestarted":instancesRestarted,
                                "teststatus": testStatus
                        }
                        printinfo.PrintTestResults(testStartTime,testStopTime, instancesRestarted, elapsedTime)
                        #notification.SendEmailNotification(notifyMessage)
                        print ("The test has now  completed. There are %s instances running" % runningListNum)
                else:
                        testStatus="FAILED:TIMED-OUT"
                        notifyMessage = {
                                "starttime" : '{0:%Y-%m-%d %H:%M:%S}'.format(testStartTime),
                                "endtime":'{0:%Y-%m-%d %H:%M:%S}'.format(testStopTime),
                                "instancesrestarted":instancesRestarted,
                                "teststatus":testStatus
                        }
                        print ("The test has TIMEDOUT")
print ("============================================================")

