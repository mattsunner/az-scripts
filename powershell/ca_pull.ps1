# Install the Az module if you haven't already
# Install-Module -Name Az -AllowClobber -Scope CurrentUser

# Login to Azure
Connect-AzAccount

# Define the time period for the last month
$startDate = (Get-Date).AddMonths(-1).ToString("yyyy-MM-dd")
$endDate = (Get-Date).ToString("yyyy-MM-dd")

# Get the access token
$context = Get-AzContext
$tenantId = $context.Tenant.Id
$subscriptionId = $context.Subscription.Id
$accountId = $context.Account.Id
$token = (Get-AzAccessToken -ResourceUrl "https://management.azure.com/").Token

# Define the REST API endpoint
$uri = "https://management.azure.com/subscriptions/$subscriptionId/providers/Microsoft.CostManagement/query?api-version=2021-10-01"

# Define the query for resource-level cost analysis
$body = @{
    type = "ActualCost"
    timeframe = "Custom"
    timePeriod = @{
        from = $startDate
        to = $endDate
    }
    dataset = @{
        granularity = "Daily"
        aggregation = @{
            totalCost = @{
                name = "PreTaxCost"
                function = "Sum"
            }
        }
        grouping = @(
            @{
                name = "ResourceId"
                type = "Dimension"
            }
        )
    }
} | ConvertTo-Json

# Query the cost management data
$result = Invoke-RestMethod -Method Post -Uri $uri -Headers @{Authorization = "Bearer $token"} -Body $body -ContentType "application/json"

# Convert the result to JSON and output it
$result | ConvertTo-Json -Depth 10
