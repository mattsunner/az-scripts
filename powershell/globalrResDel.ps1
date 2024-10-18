<#
Global Delete - Azure Resources in Subscription




Author: Matthew Sunner
#>

# Set the subscription context
$SubscriptionId = "<SUBSCRIPTION_ID>"
az account set --subscription $SubscriptionId

# Get all resource groups in the subscription
$ResourceGroups = az group list --query "[].name" -o tsv

# Loop through each resource group and delete it along with its resources
foreach ($RG in $ResourceGroups) {
    az group delete --name $RG --yes --no-wait
}