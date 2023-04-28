from dotenv import load_dotenv, set_key
import requests, os, dotenv

# Creates the payload and makes the API request
# Validates key and updates env. var to specified key

class Ebay:
    code = 0 # Store the response status code
    
    # Args will be set within the gui class, then passed based on contents of input controls
    def make_payload(self, keywords, excluded_keywords, max_search_results, category_id,
                    remove_outliers, site_id, aspects) -> dict:
        # Specify search term and filters / can add custom filters using key 'aspects'
        payload = {
            "keywords": keywords,  # str
            "excluded_keywords": excluded_keywords,  # str
            "max_search_results": max_search_results,  # str
            "category_id": category_id,  # str
            "remove_outliers": remove_outliers,  # bool
            "site_id": site_id,  # str
            "aspects": aspects  # list[dict[str, str]]
        }
        return payload

    def make_request(self, in_payload) -> dict:
        # Retrieve api key from .env file
        dotenv.load_dotenv()
        api_key = os.getenv("APP_ID")

        # Request url
        url = "https://ebay-average-selling-price.p.rapidapi.com/findCompletedItems"
        # Get the defined payload
        payload = in_payload
        headers = self.get_headers(api_key)

        # Make the request, parse respones to .json, update the status code
        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        Ebay.code = response.status_code
        print(Ebay.code)
        
        return data

    def is_valid_key(self, api_key:str, pl:dict):
        headers = self.get_headers(api_key)

        url = 'https://ebay-average-selling-price.p.rapidapi.com/findCompletedItems'

        try:
            response = requests.request("POST", url, json=pl, headers=headers)
            if response.status_code == 200:
                print(f"Success: {response.status_code}")
                return True
            else:
                print(f"Failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(e)
            return False
        
    def get_headers(self, api_key):
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "ebay-average-selling-price.p.rapidapi.com"
        }
        return headers
        
    def set_appid(self, api_key:str):
        load_dotenv()  # Load values from .env file into os.environ
        # Update value in os.environ
        os.environ['APP_ID'] = api_key
        # Update value in .env file
        set_key('.env', 'APP_ID', os.environ['APP_ID'])


