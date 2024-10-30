#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <subscription_id>"
  exit 1
fi

subscription_id=$1

access_token=$(az account get-access-token --resource https://management.azure.com/ --query accessToken --output tsv)

start_date=$(date -d "$(date +%Y-%m-01) -1 month" +%Y-%m-01)
end_date=$(date +%Y-%m-01)

uri="https://management.azure.com/subscriptions/${subscription_id}/providers/Microsoft.CostManagement/query?api-version=2021-10-01"

query_body=$(jq -n --arg start_date "$start_date" --arg end_date "$end_date" '
{
  "type": "AmortizedCost",
  "timeframe": "MonthToDate",
  "dataset": {
    "granularity": "Accumulated",
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    },
    "grouping": [
      {
        "name": "ResourceId",
        "type": "Dimension"
      }
    ]
  }
}')

response=$(curl -s -X POST "$uri" -H "Authorization: Bearer $access_token" -H "Content-Type: application/json" -d "$query_body")

rows=$(echo "$response" | jq -r '.properties.rows[]')
columns=$(echo "$response" | jq -r '.properties.columns[].name')

echo "Columns: $columns"
echo "Rows:"
echo "$rows" | while read -r row; do
  echo "$row"
done
