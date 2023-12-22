import requests
from configparser import ConfigParser



def read_credentials(config_file):
    #print("In credentials")
    #print(config_file)
    config=ConfigParser()
    config.read(config_file)

    client_id=config.get('Credentials','client_id')
    client_secret=config.get('Credentials','client_secret')

    token_url=config.get('Credentials', 'token_url')
    
    return client_id, client_secret, token_url

def get_token(client_id,client_secret,token_url):
    #print("In get token")
    payload_data={
        "grant_type":"client_credentials",
          "client_id":client_id,
          "client_secret":client_secret
          }
    response=requests.post(token_url,data=payload_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print("Failed to generate token:Response code{response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    config_file="/Users/rajeev.marwah/Documents/Customer Projects/ES Cases/Python script/config.ini"


    try:
        client_id, client_secret,token_url = read_credentials(config_file)
        token = get_token(client_id,client_secret,token_url)


        if token:
            print(token)
            #print(f"Token has been generated: {token}")

        else:
            print("Token retrieval failed.")
    except Exception as e:
        print(f"An error occurred: {e}")



