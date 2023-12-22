import csv
import json
import requests
from json import loads


def read_csv(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Assuming the CSV file has only one row of data
        row = (csv_reader, {})
        for line in csv_reader:
            print(line)
        return (line)


def create_source(api_url, csv_file_path):
    # Read values from CSV
    print("In Create Source")
    source_data = read_csv(csv_file_path)
    print("In Create Source 2")
    print(source_data)

    # Convert values to JSON payload
    payload = json.dumps({

        "name": source_data.get("name", ""),
        "description": source_data.get("description", "Test1234"),
        "owner": {
            "type": source_data.get("owner_type", "Identity"),
            "id": source_data.get("owner_id", "5af30204f5eb4e04910ebcdd7ed4ca6d"),
            "name": source_data.get("owner_name", "Rajeev Marwah")
        },
        "cluster": {
            "type": source_data.get("Cluster_type", "Cluster"),
            "id": source_data.get("Cluster_id", "185f7043f4034ed1be92c243ea79f368"),
            "name": source_data.get("Cluster_name", "AWS")
        },
        "type": source_data.get("source_type", "Active Directory - Direct"),
        "connector": source_data.get("connector", "active-directory-angularsc"),

        "connectorClass": source_data.get("connector_class", "sailpoint.connector.ADLDAPConnector"),
        "connectorAttributes": {
            "healthCheckTimeout": 30,
            "forestSettings": [
                {
                    "password": None,
                    "isResourceForest": False,
                    "gcServer": None,
                    "forestName": source_data.get("ForestName", ""),
                    "authorizationType": "simple",
                    "user": None,
                    "useSSL": False
                }
            ],
            "deltaAggregationEnabled": False,
            "domainSettings": [
                {
                    "password": source_data.get("DomainPassword", ""),
                    "servers": [
                        source_data.get("DomainServer", "")
                    ],
                    "port": source_data.get("DomainPort", ""),
                    "forestName": source_data.get("ForestName", ""),
                    "authorizationType": "simple",
                    "user": source_data.get("DomainUser", ""),
                    "domainDN": source_data.get("DomainDN", ""),
                    "useSSL": False
                }
            ],
            "deleteThresholdPercentage": source_data.get("DeleteThreshold", ""),
            "searchDNs": [
                {
                    "groupMembershipSearchDN": source_data.get("groupMembershipSearchDN", ""),
                    "searchDN": source_data.get("searchDN", ""),
                    "groupMemberFilterString": source_data.get("groupMemberFilterString", ""),
                    "iterateSearchFilter": source_data.get("iterateSearchFilter", ""),
                }
            ],

        }
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOiJlOWI2NjZlYi0wYjFhLTRkZGUtYWIyZS03Y2EzYWJlOTA2NmUiLCJwb2QiOiJzZTAxLXVzZWFzdDEiLCJzdHJvbmdfYXV0aF9zdXBwb3J0ZWQiOmZhbHNlLCJvcmciOiJjb21wYW55NTc4MC1wb2MiLCJpZGVudGl0eV9pZCI6IjVhZjMwMjA0ZjVlYjRlMDQ5MTBlYmNkZDdlZDRjYTZkIiwidXNlcl9uYW1lIjoicmFqZWV2Lm1hcndhaCIsInNjb3BlIjpbIkJnPT0iXSwic3Ryb25nX2F1dGgiOnRydWUsImV4cCI6MTcwMzIzMzA1MiwiYXV0aG9yaXRpZXMiOlsiT1JHX0FETUlOIiwic3A6dXNlciJdLCJqdGkiOiJhb01UVXR2V2tUZS1XWnh1a1JCajJNYVhiM1EiLCJjbGllbnRfaWQiOiJkNDdlNDNiOTQwZmU0MTdkYThiNWRjZDI5MmM5YjAxYyJ9.HNmwgwanh5cSjsva2kH9wwZebWw9A6TcNudJb6KlT4k'
    }

    # Make a request to the API
    response = requests.post(api_url, data=payload, headers=headers)

    # Print the response
    print(response.status_code)
    print(response.text)
    print(response.json)


if __name__ == "__main__":
    # Replace 'input.csv' with your actual CSV file path
    csv_input_file = "/Users/rajeev.marwah/Documents/Customer Projects/ES Cases/Python script/Input.csv"
    # Replace the URL with your actual API endpoint
    api_url = "https://company5780-poc.api.identitynow-demo.com/v3/sources"

    create_source(api_url, csv_input_file)