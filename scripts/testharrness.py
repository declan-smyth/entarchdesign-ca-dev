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
    print(instance.id, instance.public_ip_address, instance.state["Name"], instance.region)