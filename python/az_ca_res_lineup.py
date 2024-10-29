import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient, ResourceManagementClient

# Authenticate with Azure
credential = DefaultAzureCredential()
subscription_client = SubscriptionClient(credential)

# Function to list resources in a subscription
def list_resources(subscription_id):
    resource_client = ResourceManagementClient(credential, subscription_id)
    resources = resource_client.resources.list()
    resource_list = []
    for resource in resources:
        resource_data = {
            "name": resource.name,
            "type": resource.type,
            "subscription_id": subscription_id,
            "resource_group": resource.id.split("/")[4],
            "application_tag": resource.tags.get('application', 'N/A') if resource.tags else 'N/A'
        }
        resource_list.append(resource_data)
    return resource_list

# Main script
all_resources = []
for subscription in subscription_client.subscriptions.list():
    subscription_id = subscription.subscription_id
    all_resources.extend(list_resources(subscription_id))

# Convert to pandas DataFrame
df = pd.DataFrame(all_resources)

# Print DataFrame
print(df)
