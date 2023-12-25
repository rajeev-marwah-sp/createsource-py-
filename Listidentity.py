import csv
import requests
import subprocess
import json
def read_csv(csv_file_path):

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Assuming the CSV file has only one row of data
        row = (csv_reader, {})
        for line in csv_reader:
         return(line)
def getIdentity(api_url,token):

    tokenId = token.rstrip("\n")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tokenId
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    #print(response.text)
    if response.status_code == 200:
        # Parse the JSON response
        #Get the first object from the list, convert from list to string to retrieve the ID
        data=(response_data[0])
        id=data.get('id','')
        return id
        # Access nested elements
        #IdentitiyId = response.get('id', '')
        #print("IdentityId:", IdentitiyId)
        # Print or process the nested data
    else:
        print("Error:", response.status_code, response.text)

def get_token():
    #print("In get token")
    try:
     completed_process=subprocess.run(['python','gettoken.py'],check=True,capture_output=True,text=True)
     if completed_process.returncode == 0:
         return(completed_process.stdout)
     else:
         print(f"Error: Failed to execute")
         print("Error output:")
         print(completed_process.stderr)


    except subprocess.CalledProcessError as e:
        print("Unable to get the token from get_token.py: {e}")
        return None

if __name__ == "__main__":
    token=get_token()
    # Replace 'input.csv' with your actual CSV file path
    csv_file_path = "/Users/rajeev.marwah/Documents/Customer Projects/ES Cases/Python script/Input.csv"
    source_data=read_csv(csv_file_path)
    Email=source_data.get("email",'')
    EmailId=f"\"{Email}\""
    # Replace the URL with your actual API endpoint
    api_url = 'https://company5780-poc.api.identitynow-demo.com/beta/identities?filters=email%20eq'+ EmailId
    IdentityId=getIdentity(api_url,token)
    if IdentityId:
       print(IdentityId)
    else:
       print("Identity ID retrieval failed.")
