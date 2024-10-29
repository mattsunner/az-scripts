import requests
import json
from datetime import datetime, timedelta
import sys

from azure.identity import DefaultAzureCredential
import pandas as pd


if len(sys.argv) != 2:
    print("Usage: python script.py <subscription_id>")
    sys.exit(1)

subscription_id = sys.argv[1]

# Authenticate with Azure
credential = DefaultAzureCredential()
access_token = credential.get_token("https://management.azure.com/.default").token


start_date = (datetime.today().replace(day=1) - timedelta(days=1)).replace(day=1).isoformat()
end_date = datetime.today().replace(day=1).isoformat()

uri = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2021-10-01"


query_body = {
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
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(uri, headers=headers, data=json.dumps(query_body))
cost_data = response.json()

df = pd.DataFrame(cost_data['properties']['rows'], columns=[col['name'] for col in cost_data['properties']['columns']])

print(df.head())
print(f"Total PreTaxCost: {df['PreTaxCost'].sum()}")