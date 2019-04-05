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

# Setup an EC2 Client
ec2Client = boto3.client('ec2')

# Setup an EC2 Resource
ec2Resource = boto3.resource('ec2')

# Get all running instances in the environment
instances = ec2Resource.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

instanceList = [instance for instance in instances]

if len(instanceList) > 0 :
        # Print out available instances by quering the Reservations and Instances dict
        print ("""\
There are %s instances running your environment

"""
        % len(instanceList))
else:
        print ("""\
There are ZERO instances running in your environment
        """)

# Print the list of Instances that are running
for instance in instanceList:
    print(instance.id, instance.public_ip_address, instance.state["Name"])



# Ask user for input to select the number of machines to disrupt
iNumberInstancesToDisrupt = -1
while iNumberInstancesToDisrupt < 0:
        iNumberInstancesToDisrupt = int(input ("How many instances do you want to disrupt (MAX: %s, Min: 0):" % len(instanceList)))
        if iNumberInstancesToDisrupt > len(instanceList):
                print ("You input more than the max number of machines available in the environment")
                iNumberInstancesToDisrupt = -1
        else:
                print ("You requested to disrupt %s instances" %iNumberInstancesToDisrupt)


