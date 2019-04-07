# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# Module to Provide Print functionality
#

import boto3

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



# -- Function: Print List Informatgion on Screen
#               Input: A List of data
#               Return: None
def PrintListToScreen(aLst):
        # The content of a list
        for item in aLst:
                print(item)


# -- Function: Print List Informatgion on Screen
#               Input: A List of data
#               Return: None
def PrintTestResults(startTime, endTime, numberRestarted,elapsedTime):
        # The content of a list
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