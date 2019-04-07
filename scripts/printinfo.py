# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# This script will read the intances that are 
# available in ECS
#

import boto3


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


# -- Function: Print List Informatgion on Screen
#               Input: A List of data
#               Return: None
def PrintListToScreen(aLst):
        # The content of a list
        for item in aLst:
                print(item)