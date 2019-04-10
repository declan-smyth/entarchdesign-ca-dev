###############################################################################
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
###############################################################################
# 
# This script will read the intances that are 
# available in ECS
###############################################################################

# import 3rd party / built-in modules
import boto3
import uuid
import datetime
import time 

# import custom modules
import printinfo
import notification
import awsinformation

###############################################################################
# AWS Configuration Information
###############################################################################
awsConfiguration = {
        "autoscalegroup_name": "ead-ca-autoscalegroup",
        "topic_arn_sms": "arn:aws:sns:eu-west-1:197110341471:ead-ca-test-results-notify", # Automatically setup in the environment
        "topic_arn_email": "arn:aws:sns:eu-west-1:197110341471:AWS-Test-Results" # Manually created in the environment
}


###############################################################################
# Function Definitions
###############################################################################
# -- Function: Randomly Select Instances to disrupt.
#              The function will check if the id of the instance is in the list already
#
#               Input: List of Instances, Number to Select
#               Return: Selected Instance IDs
def RandomlySelectASDInstanceID(instLst, numSelected):
        count=0
        disruptList = list()
        from random import randint
        while count <= (numSelected -1):
                id = instLst[randint(0, len(instLst)-1)]["InstanceId"]
                if ( id not in disruptList):
                        disruptList.append (id)
                        count+=1
        return disruptList


###############################################################################
# -- Function: Randomly Select Instances to disrupt.
#              The function will check if the id of the instance is in the list already
#
#               Input: List of Instances, Number to Select
#               Return: Selected Instance IDs
def RandomlySelectEC2Instances(instLst, numSelected):
        count=0
        disruptList = list()
        from random import randint
        while count <= (numSelected -1):
                id = instLst[randint(0, len(instLst)-1)].id
                if ( id not in disruptList):
                        disruptList.append (id)
                        count+=1
        return disruptList


###############################################################################
# -- Function: Terminate Random Instances and Instance IDs
#               Input: Number of Instances to Terminate
#               Return: List of Instance IDs to Terminatated
def TerminateInstances(ec2Res,terminateLst):
        ec2Res.instances.filter(InstanceIds=terminateLst).terminate()


###############################################################################
# -- Function:  Calculate the timeout value for the tests based on
#               i.   Number of instances to terminate
#               ii.  ELB Health Checks
#               iii. Auto Scale Settings
#               Input: Number of Instances to Terminate
#               Return: List of Instance IDs to Terminatated
def CalculateTimeOutValue():
        # Setup Test Timeout value in Seconds
        testTimeoutValue = 220 * iNumberInstancesToDisrupt
        #print ("\n *** TEST TIMEOUT SET TO %s seconds ***" % testTimeoutValue)
        return testTimeoutValue 


###############################################################################
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

###############################################################################
# Print Start Title on Screen
printinfo.PrintTitle()

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get List of instances in the Auto Scale Group
#instanceListAutoScaleGrp = awsinformation.GetAutoScaleGroupInstances(awsConfiguration["autoscalegroup_name"])

# Get List of instance IDs in the Auto Scale Group
#instanceIDListAutoScaleGrp = awsinformation.GetAutoScaleGroupInstancesIDs(awsConfiguration["autoscalegroup_name"])

# Get the Target Group ARN
targetGroupARN = awsinformation.GetAutoScaleGroupTargetGrp(awsConfiguration["autoscalegroup_name"])

# Get Target Group Instance IDs
target_group_instances_ids, target_group_instances = awsinformation.GetTargetGrpInstances(targetGroupARN)

# Get Auto Scale Group Size information
autoScaleGroupInfo = awsinformation.GetAutoScaleInformation(awsConfiguration["autoscalegroup_name"])

# Get List of all Instances based on Content of Target Group
instanceFullList = awsinformation.GetListInstancesById(target_group_instances_ids)

# Get List of Running Instances based on Content of Target Group
instanceRunList, instanceIdRunList = awsinformation.GetListOfRunningInstancesById(target_group_instances_ids)

# Get Number of Instances Running
numInstancesRunning = len(instanceRunList)

# Print the Instance Information on Screen
if numInstancesRunning > 0 :
       #printinfo.PrintSAutoScaleGroupInfo(instanceListAutoScaleGrp)
       printinfo.PrintInformationToScreen(instanceFullList)
       if numInstancesRunning < autoScaleGroupInfo['desired']:
               print ("NOTE: The number of instances running does not match the desired level of your auto scale group")
else:
        print ("""\
There are ZERO instances running in your environment
        """)
        print ("============================================================")

# Ask user for input to select the number of machines to disrupt
if numInstancesRunning > 0:       
        iNumberInstancesToDisrupt = GetUserInput(len(instanceRunList))

# If the user has selected a number to disrupt and there are instnaces in the Auto Scale Group
# Start  to run the ddisruption tests
if iNumberInstancesToDisrupt > 0 and numInstancesRunning > 0:
        # Select Instances to Terminate from the list of running targets
        disruptList = RandomlySelectEC2Instances(instanceRunList,iNumberInstancesToDisrupt)
        
        # Get the number of instanace IDs selected to be terminated
        numInstancesToTerminate = len(disruptList)

        # Print Test Start Message
        printinfo.PrintTestStart(numInstancesToTerminate, disruptList)

        # Start Time to determine how long it takes to recover the system
        testStartTime = datetime.datetime.now()

        # Calculate the timeout value based on the number of instances to terminate (in Seconds)
        testTimeoutValue = CalculateTimeOutValue()
        timedout=False

        # Terminate Instances
        TerminateInstances(ec2Resource,disruptList)

        # Get list of running instances after the selected instances have been terminated 
        instanceRunListAfterTerminiation, instanceIdRunListAfterTermination = awsinformation.GetListOfRunningInstancesById(target_group_instances_ids)

        # Keep the number of running instances at the start of the test
        testStartNumRunning = runningListNum = len(instanceRunListAfterTerminiation)

        # Print list of running instances after the termination
        printinfo.PrintInformationToScreen(instanceRunListAfterTerminiation)
        print ("\nPlease wait for your system to be recovered... \n")
        printinfo.PrintThinLine

        # Desired State is:
        #       - a. Number of Instances in the target group equals desired number in auto scaling group
        #       - b. All instances in the target group are healthy
        desired_state = False
        count = 0


        while desired_state == False and timedout == False:
                count+=1

                # Get the list of Instances in the target group at the start of the test cycle
                target_group_instances_ids_in_test, target_group_instances_in_test = awsinformation.GetTargetGrpInstances(targetGroupARN)      
                
                # Test 1 - Check if the number of instances in the group is the equal to desired level of the auto scale group
                if len(target_group_instances_ids_in_test) == autoScaleGroupInfo['desired']:
                        test_1_number_of_instances_in_group = True
                else:
                        test_1_number_of_instances_in_group = False
                
                # Test 2 - Check if all instances in the group are healthy
                for target in target_group_instances_in_test:
                        #print (target['TargetHealth']['State'])
                        #print ("------")
                        if target['TargetHealth']['State'] == 'healthy':
                                test_2_instances_are_healthy = True
                        else:
                                test_2_instances_are_healthy = False

                # Check the Status of the tests...
                if test_1_number_of_instances_in_group and test_2_instances_are_healthy:
                        desired_state = True
                else:
                        desired_state = False

                # Add a time out to ensure the testing does not run forever
                if datetime.datetime.now() > testStartTime + datetime.timedelta(seconds=testTimeoutValue):
                        timedout = True
                        #print ("Timed Out !!!!")

                if (desired_state == False and timedout == False):
                        time.sleep(15) # Sleep for 15 Seconds
        else:
                # Perform Calculations when the tests stop
                testStopTime = datetime.datetime.now()

                instanceRunListAfterTest, instanceIdRunListAfterTest = awsinformation.GetListOfRunningInstancesById(target_group_instances_ids_in_test)
               
                # Get the list of new instance IDs that have been added to the target group
                newInstanceIDs = list(set(instanceIdRunListAfterTermination) ^ set(instanceIdRunListAfterTest))

                # Get the number of instances that were created
                instancesRestarted = len(newInstanceIDs)

                # Calculate the elapsed time for the test
                elapsedTime = testStopTime - testStartTime

                # Check if the test timed out or completed within the expected time
                if not timedout:
                        testStatus="PASSED"
                        print ("The test has now  completed. There are %s instances running" % len(instanceIdRunListAfterTest))
                else:
                        testStatus="FAILED:TIMED-OUT"
                        print ("The test has TIMEDOUT. Your instances did not restart within the time period allowed.")

                # Construct the Notification Messatge
                notifyMessage = {
                        "starttime" : '{0:%Y-%m-%d %H:%M:%S}'.format(testStartTime),
                        "endtime":'{0:%Y-%m-%d %H:%M:%S}'.format(testStopTime),
                        "instancesstopped":numInstancesToTerminate,
                        "instancesrestarted":instancesRestarted,
                        "elapsedtime": str(elapsedTime),
                        "teststatus": testStatus,
                        "newinstanceid": newInstanceIDs
                }

                # Print Infomration on screen
                printinfo.PrintTestResult(notifyMessage)
                
                # Print Instance Information to Screen
                printinfo.PrintInformationToScreen(instanceRunListAfterTest)
                
                # Send Notifications of test results
                notification.SendNotification(notifyMessage)
                #notification.SendEmailNotification(notifyMessage, awsConfiguration['topic_arn_email'])
                notification.SendSMSNotification(notifyMessage, awsConfiguration['topic_arn_sms'])
# Print a line at the end... 
printinfo.PrintThickLine()

