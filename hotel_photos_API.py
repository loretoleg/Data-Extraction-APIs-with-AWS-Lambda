import json
import requests
import base64
import os

#RAPID_API_KEY = os.environ['api_key']
RAPID_API_HOST = "booking-com.p.rapidapi.com"

us_state_codes = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "US": "US"
}

def get_hotel_id(name):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    params = {
        "locale": "en-gb",
        "name": name
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()[0]['dest_id']


def get_hotel_photos(hotel_id):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/photos"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    params = {
        "locale": "en-gb",
        "hotel_id": hotel_id
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def print_photos_url(response):
    photos_urls = []
    for item in response:
        url_max = item.get('url_max', 0)  # Use get() to handle missing key gracefully
        photos_urls.append(url_max)
    return photos_urls


def lambda_handler(event, context):
    try:
        decoded_body = base64.b64decode(event['body']).decode('utf-8')
        query = json.loads(decoded_body).get('query', '')
        loc = json.loads(decoded_body).get('location', 'US')
        if loc == 'null': loc = 'US'
        loc_state = us_state_codes[loc]
        
        print(query+' '+loc_state)
        
        hotel_id = get_hotel_id(query+' '+loc_state)
        photos_response = get_hotel_photos(hotel_id)
        photos_urls = print_photos_url(photos_response)

        return {
            'statusCode': 200,
            'body': json.dumps({'photos_urls': photos_urls})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
