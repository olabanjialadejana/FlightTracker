import requests
import json


class LocationFinder:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self, api_key):
        self.api_key = api_key
        self.location_endpoint = "https://api.tequila.kiwi.com/locations/query"
        self.headers = {"apikey": self.api_key}

    def get_location_information(self, city=None):
        if city is None:
            city = input("What city do you want? ")

        query = {
            "term": city,
            "locale": "en-US",
            "location_types": "airport",
            "limit": 10,
            "active_only": True,
            "sort": "name"
        }

        response = requests.get(url=self.location_endpoint, params=query, headers=self.headers)
        response_data = response.json()
        return response_data

    def find_city_code(self, city):
        response_data = self.get_location_information(city)
        final_city_code = ""
        if (len(response_data['locations'])) > 1:
            for airport in response_data['locations']:
                if airport['city']['name'].lower() == city.lower():
                    city_code = airport['city']['code']
                    final_city_code = city_code
                    break
        else:
            city_name = response_data['locations'][0]['city']['name']
            city_code = response_data['locations'][0]['city']['code']
            if city.lower() == city_name.lower():
                final_city_code = city_code
        return final_city_code


if __name__ == "__main__":
    API_KEY = "rgURLGpOzDpY1UK8vTWexzExHY71yL-8"




