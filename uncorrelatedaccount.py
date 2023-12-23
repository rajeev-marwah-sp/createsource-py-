import csv
import requests
import subprocess
#Read the CSv file
def read_csv(csv_file_path):

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Assuming the CSV file has only one row of data
        row = (csv_reader, {})
        for line in csv_reader:
         return(line)
#Calling the uncorrelated account
def uncorrelatedaccounts(api_url,token):
    tokenId = token.rstrip("\n")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tokenId
    }
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    print(response.text)
#Calling the get token function, get_token script should be in the same folder
def get_token():
    #print("In get token")
    try:
     completed_process=subprocess.run(['python','gettoken.py'],check=True,capture_output=True,text=True)
     if completed_process.returncode == 0:
         return(completed_process.stdout)
     else:
         print(f"Error: Failed to execute")
         print(completed_process.stderr)


    except subprocess.CalledProcessError as e:
        print("Unable to get the token from get_token.py: {e}")
        return None
#Main Function
if __name__ == "__main__":

    token = get_token()

    # Replace 'input.csv' with your actual CSV file path
    csv_file_path = "<File path with File Name>"
    sourceId=read_csv(csv_file_path)

    srcId=sourceId.get("sourcename", "")
    # Replace the URL with your actual API endpoint
    api_url = f'https://<tenant-url>/v3/accounts?filters=uncorrelated%20eq%20true%20and%20sourceId%20eq%20\"{srcId}\"'
    #Calling the uncorrelated function
    uncorrelatedaccounts(api_url,token)