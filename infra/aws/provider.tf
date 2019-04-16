provider "aws" {
    version = "~> 2.5"
    access_key = "${var.ACCESS_KEY}"
    secret_key = "${var.SECRET_KEY}"
    region = "${var.REGION}"
}