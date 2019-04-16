provider "azurerm" {
    version = "~> 1.24"
    subscription_id = "${var.ARM_SUBSCRIPTION}"
    client_id       = "${var.ARM_CLIENT_ID}"
    client_secret   = "${var.ARM_CLIENT_SECRET}"
    tenant_id       = "${var.ARM_TENANT_ID}"
}

provider "random" {
    version = "~> 2.1"
}