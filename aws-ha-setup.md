# AWS High Availability Setup Instructions

## Author Information

| Name          | Email                  |
| ------------- | ---------------------- |
| Declan Smyth  | declan.smyth@gmail.com |

---

## Introduction

The AWS High Availability environmnet is created using terraform to create the required infrastruction to test the re-instatement capabilities of Amazon Web Services' ability to maintain a high-availabilty environment 

This is the high-level environemnt configuration that is implemented

| AWS Element          |  Configuration                   |
|----------------------|----------------------------------|
| Load Balancer        | ead-ca-loadbalancer              |
| Target Group         | ead-ca-targetgroup               |
| Auto Scaling Group   | ead-ca-autoscalegroup            |
| Launch Configuration | ead-ca-launchconfigurator        |
| Security Groups      | ead-ca-securitygrp-autoscalegrp  |
|                      | ead-ca-securitygrp--loadbalancer |
| SNS Topics           | ead-ca-test-results-notify       |

### Auto Scale Group

Responsible for describing the desired intrastrucutre you want to deploy
Give the auto scale group charastics:

* Min number of instances = 6
* Max number of instances = 6

In this setup it will maintain the group at a fixed size and is not scalling in or out.It will monitor the availability zones and send an alert when an event happens. This takes place using CloudWatch and have SNS send out the SMS or Email. This will take place automatically.

## Environment Setup Instructions

### Pre-Requisites

#### General Software

The following software will be required to be installed on your system to run the AWS High-Availability Testing:

* GIT
* Python 3.7

#### AWS Environment Creation

You must download and deploy Terraform to create the test environment. The software is availalbe from HashiCorp at this link: <https://www.terraform.io/downloads.html>

#### Source Code Repository

All source code is maintained in a GIT repository hosted on GITHub. To download the repository run the following command in your preferred directory structure
`git clone https://github.com/declan-smyth/ent-arch-design-ca-dev`

The repository has the following layout

| Direcory             | Purpose                                                   |
|----------------------|-----------------------------------------------------------|
| scripts              | Contains the python scripts for runnning testing          |
| infra                | Contains the terraform files for creating the environment |
| images               | Images that are used in the readme files                  |

### Setting up AWS

To set up your environment you must do the following:

1 Create & Configure a new file called *terraform.tfvars*. This file is used to provide configuration information for your AWS Environment. You must provide the following configuration infomration:
  * ACCESS_KEY 
  * SECRET_KEY 
  * SUBSCRIBER_EMAIL 
  * SUBSCRIBER_PHONE 
  * NUMBER_OF_INSTANCES
  If this information is missing, the environment will be get created successfully

2 Goto the *infra* folder and execute *terraform init*
3

### Executing the Tests