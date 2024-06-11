import requests
import json
import urllib.parse
import random

### this code takes in a url from any character from chub.ai's website, and outputs the json for channel ai's bot creation admin site.
### scraper 

def fetch_character_data(url):
    # simulate a web browser request 
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'ch-api-key': 'glpat-UZXEBupEVv2vMCdFDkfJ',
        'origin': 'https://chub.ai',
        'priority': 'u=1, i',
        'referer': 'https://chub.ai/',
        'samwise': 'glpat-UZXEBupEVv2vMCdFDkfJ',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    # send request to retrieve unique character data
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()

            # extract data, remove unnecessary characters
            personality = data['node']['definition']['personality'].replace('\r', '').replace('\n', '')
            description = data['node']['definition']['description'].replace('\r', '').replace('\n', '')
            first_message = data['node']['definition']['first_message'].replace('\r', '').replace('\n', '').replace('*', '')

            # create json 
            prompt = {
                "type": "duo-image",
                "model": "gpt-4-0314",
                "state": "LIVE",
                "top_p": 0.8,
                "memory": 20,
                "prompt": description + personality,
                "greeting": first_message,
                "temperature": 0.7
            }

            # print json
            print(json.dumps(prompt, indent=2))
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
    else:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")

### api process  

### we need a unique api for each request

def construct_api_url(base_url):
    # parse the input URL
    parsed_url = urllib.parse.urlparse(base_url)
    
    # extract the path and replace the domain
    path = parsed_url.path
    api_base_url = f"https://api.chub.ai/api{path}"
    
    # gen a random nocache value
    nocache_value = random.random()
    
    # Construct the full api url
    api_url = f"{api_base_url}?full=true&nocache={nocache_value}"
    
    return api_url

def main():
    # obtain character url to begin 
    base_url = input("Enter the base URL: ").strip()
    
    # construct api url from base url
    api_url = construct_api_url(base_url)
    
    # fetch data & output json
    fetch_character_data(api_url)

### run script
if __name__ == "__main__":
    main()
