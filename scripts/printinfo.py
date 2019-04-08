# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# Module to Provide Print functionality
#

import boto3
import json

# -- Function: Print Starting Title on Screen
#               Input:  None
#               Return: None
def PrintTitle():
    print ("""\
******************************************************

             Welcome to the Chaos Monkey 
                  AWS Test Harness

******************************************************
    """)


# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintInformationToScreen(instLst):
        print ("============================================================")

        # Print the list of Instances to the screen
        for instance in instLst:
                print(instance.id, instance.public_ip_address, instance.state["Name"])
        print ("""\
There are %s instances running your environment
        """ % len(instLst))
        print ("============================================================")


# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintSAutoScaleGroupInfo(instLst):
        print ("===========================================================================")
        print ("Instance ID\t\t Health Status\t LifeCycleState\t Availability Zone")
        print ("---------------------------------------------------------------------------")
        
        # Print the list of Instances to the screen
        
        for instance in instLst:
                print("{0}\t {1}\t {2}\t {3}\t".format(instance["InstanceId"], instance["HealthStatus"], instance["LifecycleState"], instance["AvailabilityZone"]))
        print ("""\
\nThere are %s instances your auto scale group
        """ % len(instLst))
        print ("==========================================================================")

# -- Function: Print List Informatgion on Screen
#               Input: A List of data
#               Return: None
def PrintListToScreen(aLst):
        # The content of a list
        for item in aLst:
                print(item)


# -- Function: Print Results of testings
#               Input: JSON Results
#               Return: None
def PrintTestResults(startTime, endTime, numberRestarted,elapsedTime):
               
        print ("""\
******************************************************
                Results of AWS Testing
******************************************************
""")
        print (
            "Start Time:          {0}\nEnd Time:            {1}\nInstances Restarted: {2}\nElapsed Time:        {3}".format(
            startTime, endTime, numberRestarted,elapsedTime)
        )
        print ("\n******************************************************")
