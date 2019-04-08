# #################################### #
# Author: Declan Smyth
# Email : declan.smyth@gmail.com
# #################################### #
# 
# This script will send notification infomration
# to AWS SNS and CloudWatch 
# available in ECS
# ######################################
import boto3
import json

snsClient = boto3.client('sns')
ARN='arn:aws:sns:eu-west-1:197110341471:AWS-Test-Results'

#-------------------------------------------
# Function Definitions
#-------------------------------------------

def GetTopicARN():
    response = snsClient.list_topics()
    print (response['Topics'])


def SendEmailNotification(message):
    sendMessage = {
        'email': json.dumps(message)
    }
    response = snsClient.publish(
        TargetArn=ARN,
        Message=json.dumps(sendMessage),
        Subject='AWS Chaos Monkey Test Results',
        MessageStructure='json'
    )


def SendSMSNotification(message):
    sendMessage = {
        'sms': json.dumps(message)
    }
    response = snsClient.publish(
        TargetArn=ARN,
        Message=json.dumps(sendMessage),
        Subject='AWS Chaos Monkey Test Results',
        MessageStructure='json'
    )

def SendAllNotification(message):
    SendEmailNotification(message)
    SendSMSNotification(message)

#-------------------------------------------
