import csv
import requests
import subprocess
def read_csv(csv_file_path):

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Assuming the CSV file has only one row of data
        row = (csv_reader, {})
        for line in csv_reader:
            print(line)
        return(line)
def uncorrelatedaccounts(api_url,token):

    tokenId = token.rstrip("\n")
    print(tokenId)
    print(api_url)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + tokenId
    }
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    print(response.text)

def get_token():
    #print("In get token")
    try:
     completed_process=subprocess.run(['python','gettoken.py'],check=True,capture_output=True,text=True)
     if completed_process.returncode == 0:
         #print("Execution successful.")
         #print("Output:")
         #print(completed_process.stdout)
         return(completed_process.stdout)
     else:
         print(f"Error: Failed to execute")
         print("Error output:")
         print(completed_process.stderr)


    except subprocess.CalledProcessError as e:
        print("Unable to get the token from get_token.py: {e}")
        return None

if __name__ == "__main__":

    token = get_token()
    print(token)

    # Replace 'input.csv' with your actual CSV file path
    csv_file_path = "/Users/rajeev.marwah/Documents/Customer Projects/ES Cases/Python script/sourceoutput.csv"
    sourceId=read_csv(csv_file_path)
    print(sourceId)
    srcId=sourceId.get("sourcename", "")
    Id=str(srcId)
    print(srcId)
    # Replace the URL with your actual API endpoint
    api_url = f'https://company5780-poc.api.identitynow-demo.com/v3/accounts?filters=uncorrelated%20eq%20true%20and%20sourceId%20eq%20\"{srcId}\"'
    print(api_url)
    uncorrelatedaccounts(api_url,token)