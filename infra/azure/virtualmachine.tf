
# ------------------------------------------------------------------------------------------------
#
# VIRTUAL MACHINE CONFIGURATION
#
# ------------------------------------------------------------------------------------------------

resource "azurerm_virtual_machine" "ead-ha-virtualmachine" {
    name                  = "${var.KEY_NAME}-ha-vm"
    location              = "${azurerm_resource_group.ead-ha-resourcegrp.location}"
    resource_group_name   = "${azurerm_resource_group.ead-ha-resourcegrp.name}"
    network_interface_ids = ["${azurerm_network_interface.ead-ha-vm-networkcard.id}"]
    vm_size               = "Standard_DS1_v2"

    storage_os_disk {
        name              = "${var.KEY_NAME}-ha-vm-disk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }

    storage_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "16.04.0-LTS"
        version   = "latest"
    }

    os_profile {
        computer_name  = "${var.KEY_NAME}-ha-vm-1"
        admin_username = "azureuser"
        admin_password = "Rmg_Web_012!"
    }

    os_profile_linux_config {
        disable_password_authentication = false
    }

    boot_diagnostics {
        enabled     = "true"
        storage_uri = "${azurerm_storage_account.ead-ha-storage-account.primary_blob_endpoint}"
    }

    tags {
        environment = "${var.CA_ENVIRONMENT}"
        purpose = "${var.CA_PURPOSE}"
        owner = "${var.CA_AUTHOR_NAME}"
    }
}