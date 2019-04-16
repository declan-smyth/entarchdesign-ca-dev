variable "ARM_CLIENT_ID" {}
variable "ARM_CLIENT_SECRET" {}
variable "ARM_TENANT_ID" {}
variable "ARM_SUBSCRIPTION" {}

variable "NUMBER_OF_INSTANCES" {
    description="Nunmber of server instances to start in the environment"
}

variable "SUBSCRIBER_PHONE" {
    description = "Notification mobile phone number used for environment alerts"
}

variable "REGION" {
  description = "Default Region for creating instances"
  default = "North Europe"
}

variable "KEY_NAME" {
    description = "Prefix for the name of all resources"
    default = "eadca"
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

variable "CA_ENVIRONMENT" {
  default = "MSc. in DevOps"
}

variable "CA_PURPOSE" {
  default = "Ent. Arch. Design - Assignment"
}

