variable "ACCESS_KEY" {}
variable "SECRET_KEY" {}

variable "AMI" {
  description = " This is the image used in the Launch Configuration"
  default = "ami-03d6469eda9235f8e"
}

variable "NUMBER_OF_INSTANCES" {
  description= "The number of instances that are in the auto scale group"
  default = 3
}

variable "REGION" {
  description = "Default Region for creating instances"
  default = "eu-west-1"
}

variable "PROTOCOL_HTTP" {
  default="HTTP"
}

variable "PORT_HTTP" {
  default = "80"
}

variable "PORT_SSL" {
  default = "22"
}

variable "INSTANCE_TYPE" {
  default = "t2.micro"
}

variable "KEY_NAME" {
  default = "ead-ca"
}

variable "CA_AUTHOR_NAME" {
  default = "Declan Smyth"
}

variable "CA_AUTHOR_EMAIL" {
  default = "declan.smyth@gmail.com"
}


variable "CA_AUTHOR_PHONE" {
  default = ""
}

variable "SUBSCRIBER_EMAIL" {
  description = "This is the email address for subscription to the topic operator"
  default = ""
}

variable "CA_ENVIRONMENT" {
  default = "MSc. in DevOps"
}

variable "CA_PURPOSE" {
  default = "Ent. Arch. Design - Assignment"
}