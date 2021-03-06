###############################################################################
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
###############################################################################
# 
# Module to Provide Print functionality
#
###############################################################################

import boto3
import json

###############################################################################
# -- Function: Print Starting Title on Screen
#               Input:  None
#               Return: None
def PrintTitle():
        PrintThickLine()
        print ("""\

             \t     Welcome to the Chaos Monkey 
                  \tAWS Test Harness
        """)
        PrintThickLine()



###############################################################################
# -- Function: Print a think line
#               Input:  None
#               Return: None
def PrintThickLine():
        print ("===========================================================================")



###############################################################################
# -- Function: Print a thin line
#               Input:  None
#               Return: None
def PrintThinLine():
        print ("---------------------------------------------------------------------------")



###############################################################################
# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintInformationToScreen(instLst):
        PrintThickLine()
        print ("Instance ID\t\t Public IP\t Instance State\t Availability Zone")
        PrintThinLine()
        # Print the list of Instances to the screen
        for instance in instLst:
                print("{0}\t {1}\t {2}\t {3}\t".format(instance.id, instance.public_ip_address, instance.state["Name"], instance.placement["AvailabilityZone"]))
        print ("""\
\nThere are %s instances running your environment
        """ % len(instLst))
        PrintThickLine()


###############################################################################
# -- Function: Print Instance Informatgion on Screen
#               Input: List of Instances
#               Return: None
def PrintSAutoScaleGroupInfo(instLst):
        PrintThickLine()
        print ("Instance ID\t\t Health Status\t LifeCycleState\t Availability Zone")
        PrintThinLine()
        
        # Print the list of Instances to the screen
        for instance in instLst:
                print("{0}\t {1}\t {2}\t {3}\t".format(instance["InstanceId"], instance["HealthStatus"], instance["LifecycleState"], instance["AvailabilityZone"]))
        print ("""\
\nThere are %s instances your auto scale group
        """ % len(instLst))
        PrintThickLine()




###############################################################################
# -- Function: Print List Informatgion on Screen
#               Input: A List of data
#               Return: None
def PrintListToScreen(aLst):
        # The content of a list
        for item in aLst:
                print(item)




###############################################################################
# -- Function: Print Results of testings
#               Input: JSON Results
#               Return: None
def PrintTestResult(notifymessage):
        PrintThickLine()
        print ("""\

                Results of Test Run
        """)
        PrintThinLine()
        print (             
            "Start Time:          {0}\n \
             End Time:            {1}\n \
             Instances Stopped:   {2}\n \
             Instances Restarted: {3}\n \
             Elapsed Time:        {4}\n \
             Test Status:         {5}\n \
             New Instance IDs:    {6}\n".format(
            notifymessage['starttime'], 
            notifymessage['endtime'], 
            notifymessage['instancesstopped'],
            notifymessage['instancesrestarted'], 
            notifymessage['elapsedtime'], 
            notifymessage['teststatus'], 
            notifymessage['newinstanceid'])
        )
        PrintThickLine()



###############################################################################
# -- Function: Print Results of testings
#               Input: JSON Results
#               Return: None
def PrintTestStart(numDisrupt, disruptionList):
        PrintThickLine()
        print ("""\
                \t      Starting Test Run
        """)
        PrintThinLine()
        print ("This test will terminate {0} instances and monitor re-instatement time".format(numDisrupt))
        print ("\nThe following instances will be disrupted:\n")
        print ("\t%s\n" %disruptionList)
        PrintThickLine()