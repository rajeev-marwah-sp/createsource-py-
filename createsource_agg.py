import csv
import json
import subprocess
import gettoken as token
import requests
from json import loads

#Function for reading the csv file
def read_csv(csv_file_path):
    print("Reading CSV file")
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Assuming the CSV file has only one row of data
        row = (csv_reader, {})
        for line in csv_reader:
         return(line)




#Function for Creating the source
def create_source(api_url, csv_file_path,token,IdentityId):
    # Read values from CSV
    print("In Create Source")
    source_data = read_csv(csv_file_path)
    IdentityId = IdentityId.rstrip("\n")
    # Convert values to JSON payload
    payload = json.dumps({
        "name": source_data.get("name", ""),
        "description": source_data.get("description", ""),
        "owner": {
            "type": source_data.get("owner_type", "Identity"),
            "id":  IdentityId

        },
        "cluster": {
            "type": source_data.get("Cluster_type", "Cluster"),
            "id": source_data.get("Cluster_id", ""),
            "name": source_data.get("Cluster_name", "")
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
    }   )
    

   #Striping the token for newline character at the end
    tokenId=token.rstrip("\n")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tokenId
    }

    # Make a request to the API
    response = requests.post(api_url, data=payload, headers=headers)
    # Print the response
    if response.status_code == 201:
        # Parse the JSON response
        json_response = response.json()
        # Access nested elements
        cloudExternalId = json_response.get('connectorAttributes', {}).get('cloudExternalId', '')
        sourceId=json_response.get('id','')
        print("SourceID:",sourceId)
        # Print or process the nested data
        print("cloudExternalId:", cloudExternalId)
        aggregation(cloudExternalId,tokenId)
    else:
        print("Error:", response.status_code, response.text)

#Function for running the aggregation
def aggregation(cloudExternalId,tokenId):
    print("In Aggregation Block")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tokenId
        }
    Id=cloudExternalId
    #NOTE: This uses cc api as at the time of building the script, V3 API wasn't being released
    #Needs to be replaced by V3 API
    api_url="https://company5780-poc.api.identitynow-demo.com/cc/api/source/loadAccounts/" + Id
    response = requests.post(api_url,headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        print("Aggregation Started")
    else:
        print("Error:", response.status_code, response.text)
#Function for getting the Identity ID
def get_Identity():
    try:
        print("Calling Get Identity Script")
        completed_process = subprocess.run(['python', 'Listidentity.py'], check=True, capture_output=True, text=True)

        if completed_process.returncode == 0:
            return (completed_process.stdout)
        else:
            print(f"Error: Failed to execute")
            print("Error output:")
            print(completed_process.stderr)
    except subprocess.CalledProcessError as e:
        print("Unable to get the Identity ID from List Identity.py: {e}")
        return None
#Mathod to get the token
def get_token():

    try:
     completed_process=subprocess.run(['python','gettoken.py'],check=True,capture_output=True,text=True)
     if completed_process.returncode == 0:
         print("In get token")
         return(completed_process.stdout)
     else:
         print(f"Error: Failed to execute")
         print("Error output:")
         print(completed_process.stderr)
    except subprocess.CalledProcessError as e:
        print("Unable to get the token from get_token.py: {e}")
        return None
#MAIN FUNCTION
if __name__ == "__main__":
    # Replace 'input.csv' with your actual CSV file path
    csv_input_file = "/Users/rajeev.marwah/Documents/Customer Projects/ES Cases/Python script/Input.csv"
    # Replace the URL with your actual API endpoint
    api_url = "https://company5780-poc.api.identitynow-demo.com/v3/sources"
    token=get_token()
    IdentityId=get_Identity()
    print("Identity ID fetched")
    print(IdentityId)
    #Calling the Create source function
    create_source(api_url, csv_input_file,token,IdentityId)