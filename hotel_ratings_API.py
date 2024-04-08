import json
import requests
import base64
import os

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

def lambda_handler(event, context):
    try:
        # Replace 'YOUR_GOOGLE_API_KEY' with your actual API key
        api_key = os.environ['api_key']
        search_endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        # Extract the user input from the POST request
        decoded_body = base64.b64decode(event['body']).decode('utf-8')
        query = json.loads(decoded_body).get('query', '')
        loc = json.loads(decoded_body).get('location', 'US')
        
        if loc == 'null': loc = 'US'
        loc_state = us_state_codes[loc]

        #method = event['requestContext']['http'].get('method', '')
        #if method == 'POST': key_name = 'rating'
        #else: key_name = 'website'
        key_name = 'rating'

        def get_place_rating(place_id):
            details_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                'place_id': place_id,
                'key': api_key
            }

            details_response = requests.get(details_endpoint, params=details_params)
         
            rating = details_response.json().get('result', {}).get(key_name, 'N/A')

            return rating

        params = {
            'query': query+' '+loc_state,
            'key': api_key
        }

        response = requests.get(search_endpoint, params=params)
        results = response.json().get('results', [])
        
        
        #place_id = results[0].get('place_id')
        #rating = get_place_rating(place_id)
        #real_result.append({key_name : rating})
        
        real_result = []

        for result in results:
            place_id = result['place_id']
            rating = get_place_rating(place_id)
            real_result.append({key_name : rating})

        return {
            'statusCode': 200,
            'body': json.dumps({'results': real_result})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

