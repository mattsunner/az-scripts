"""
az_delete_env - Python script to remove all Azure resources in a resource group

A utility function to delete Azure data within a specified subscription. NOTE: 
This utility will delete all resources within a subscription. Only use for
testing and development subscriptions, NOT FOR USE IN PRODUCTION.


Author: Matthew Sunner, 2024
"""

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import HttpResponseError


subscription_id = ""
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

resource_groups = resource_client.resource_groups.list()

for rg in resource_groups:
    rg_name = rg.name
    print(f"Deleting resource group: {rg_name}")
    try:
        resource_client.resource_groups.begin_delete(rg_name)
        print(f"Deleted resource group: {rg_name}")
    except HttpResponseError as e:
        print(f"Failed to delete resource group {rg_name}: {e.message}")