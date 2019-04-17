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
lambdaClient = boto3.client('lambda')
lambdaNotifyARN = 'arn:aws:lambda:eu-west-1:197110341471:function:send_notification_of_results'

#-------------------------------------------
# Function Definitions
#-------------------------------------------

###############################################################################
# -- Function: 
#               Input:  
#               Return: 
def GetTopicARN():
    response = snsClient.list_topics()
    print (response['Topics'])


###############################################################################
# -- Function: Send Email notification using SNS
#               Input:  
#               Return: 
def SendEmailNotification(message,topic_arn_email):
    sendMessage = {
        'default':"",
        'email': json.dumps(message)
    }

    response = snsClient.publish(
        TargetArn=topic_arn_email,
        Message=json.dumps(sendMessage),
        Subject='Declan Smyth - AWS Chaos Monkey Test Results',
        MessageStructure='json'
    )


###############################################################################
# -- Function: Send SMS notification using SNS
#               Input:  
#               Return: 
def SendSMSNotification(message, topic_arn_sms):
    sendMessage = {
        'default': "",
        'sms': json.dumps(message)
    }
    response = snsClient.publish(
        TargetArn=topic_arn_sms,
        Message=json.dumps(sendMessage),
        Subject='Declan Smyth - AWS Chaos Monkey Test Results',
        MessageStructure='json'
    )

###############################################################################
# -- Function: Send notification using Lambda function
#               Input:  
#               Return: 
def SendNotification(message):

    response = lambdaClient.invoke(FunctionName=lambdaNotifyARN,
                                    InvocationType='Event',
                                    ClientContext='EAD-CA-AWSTEST-APP',
                                    Payload=json.dumps(message))
    if response['StatusCode'] != "200":
        print ("SendNotification: Error Code: %s \n Please check AWS logs for further information.",% response['StatusCode'])
    
    
