variable "ACCESS_KEY" {}
variable "SECRET_KEY" {}

variable "AMI" {
  default = "ami-03d6469eda9235f8e"
}

variable "NUMBER_OF_INSTANCES" {
  description= "The number of instances that are in the auto scale group"
  default = 6
}

variable "REGION" {
  description = "Default Region for creating instances"
  default = "eu-west-1"
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

variable "CA_ENVIRONMENT" {
  default = "MSc. in DevOps"
}

variable "CA_PURPOSE" {
  default = "Ent. Arch. Design - Assignment"
}