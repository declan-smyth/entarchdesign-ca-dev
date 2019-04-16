# ------------------------------------------------------------------------------------------------
# The following sites were referenced to create this deployment script
#   * https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-create-complete-vm
#   * https://www.terraform.io/docs/providers/azurerm/
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
#
# RESOURCE GROUP CONFIGURATION
#
# ------------------------------------------------------------------------------------------------

# Create a resource group that will contain all created resources
resource "azurerm_resource_group" "ead-ha-resourcegrp" {
    name     = "${var.KEY_NAME}-ha-resourcegrp"
    location = "${var.REGION}"

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}

# ------------------------------------------------------------------------------------------------
#
# NETWORK CONFIGURATION
#
# ------------------------------------------------------------------------------------------------

# Create a virtual network within the resource group
resource "azurerm_virtual_network" "ead-ha-network" {
  name                = "${var.KEY_NAME}-ha-network"
  resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
  location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
  address_space       = ["10.0.0.0/16"]

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}

# Create a subnet linked to the virtual network and the resource group
resource "azurerm_subnet" "ead-ha-subnet-1" {
    name                 = "${var.KEY_NAME}-ha-subnet-1"
    resource_group_name  = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    virtual_network_name = "${azurerm_virtual_network.ead-ha-network.name}"
    address_prefix       = "10.0.2.0/24"
}

# Create a second subnet and linked to the virtual network and resource group
resource "azurerm_subnet" "ead-ha-subnet-2" {
    name                 = "${var.KEY_NAME}-ha-subnet-2"
    resource_group_name  = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    virtual_network_name = "${azurerm_virtual_network.ead-ha-network.name}"
    address_prefix       = "10.0.3.0/24"
}

# Create a public IP Address
resource "azurerm_public_ip" "ead-ha-publicip" {
  name                = "${var.KEY_NAME}-ha-publicip"
  location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
  resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
  domain_name_label   = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
  allocation_method   = "Dynamic"

  tags {
    environment = "${var.CA_ENVIRONMENT}"
    purpose = "${var.CA_PURPOSE}"
    owner = "${var.CA_AUTHOR_NAME}"
  }
}

resource "azurerm_public_ip" "ead-ha-publicip-2" {
  name                = "${var.KEY_NAME}-ha-publicip-2"
  location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
  resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
  domain_name_label   = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
  allocation_method   = "Dynamic"

  tags {
    environment = "${var.CA_ENVIRONMENT}"
    purpose = "${var.CA_PURPOSE}"
    owner = "${var.CA_AUTHOR_NAME}"
  }
}

# Create a virtual network card to connect the virtual machine to a virtual network
resource "azurerm_network_interface" "ead-ha-vm-networkcard" {
    name                = "${var.KEY_NAME}-ha-vm-networkcard"
    location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
    resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    network_security_group_id = "${azurerm_network_security_group.ead-ha-network-securitygrp.id}"

    ip_configuration {
        name                          = "myNicConfiguration"
        subnet_id                     = "${azurerm_subnet.ead-ha-subnet-1.id}"
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = "${azurerm_public_ip.ead-ha-publicip.id}"
    }

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}

# Create a loadbalancer and link it to the Public IP Address
resource "azurerm_lb" "ead-ha-loadbalancer" {
  name                = "${var.KEY_NAME}-ha-loadbalancer"
  location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
  resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"

  frontend_ip_configuration {
    name                 = "${var.KEY_NAME}-ha-loadbalancer-publicip"
    public_ip_address_id = "${azurerm_public_ip.ead-ha-publicip-2.id}"
  }

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}


# ------------------------------------------------------------------------------------------------
#
# STORAGE ACCOUNT CONFIGURATION
#
# ------------------------------------------------------------------------------------------------

# Create a storage account for diagnostic information
resource "azurerm_storage_account" "ead-ha-storage-account" {
    name                = "${var.KEY_NAME}${random_id.randomId.hex}"
    resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
    account_replication_type = "LRS"
    account_tier = "Standard"

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}

# Provide assistance creating unique naming of the storage account
resource "random_id" "randomId" {
    keepers = {
        # Generate a new ID only when a new resource group is defined
        resource_group = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    }
    
    byte_length = 8
}

# ------------------------------------------------------------------------------------------------
#
# SECURITY CONFIGURATION
#
# ------------------------------------------------------------------------------------------------

# Create a network security group that is linked to the Network Card to only allow traffic into the 
# virtual environmento on port 22
resource "azurerm_network_security_group" "ead-ha-network-securitygrp" {
    name                = "${var.KEY_NAME}-ha-network-securitygrp"
    location            = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
    resource_group_name = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}

