import requests


class FlightSearch:

	def __init__(self, api_key):
		self.api_key = api_key,
		self.headers = {"apikey": api_key}
		self.api_endpoint = "https://tequila-api.kiwi.com/v2/search"
		self.flight_data = None

	def get_flight_info(self, fly_from, fly_to, date_from, date_to, return_from, return_to, max_stopovers):
		"""
		:param str fly_from: city IATA code
		:param str fly_to: city IATA code
		:param str date_from: start date range (e.g. "25/03/2000")
		:param str date_to: end date range (e.g. 12/05/2001)
		:param str return_from: start date range for return (e.g. 25/07/2001)
		:param str return_to: end date range for return (e.g. 25/09/2001)
		:param str curr: currency for flight fare (e.g. "USD")
		:param int max_stopovers: number of stopovers (e.g. 2)
		:return: a list containing available flights
		"""
		data = {
			"fly_from": fly_from,
			"fly_to": fly_to,
			"date_from": date_from,
			"date_to": date_to,
			"return_from": return_from,
			"return_to": return_to,
			"curr": "USD",
			"max_stopovers": max_stopovers,

		}

		response = requests.get(url=self.api_endpoint, params=data, headers=self.headers)
		self.flight_data = response.json()
		return self.flight_data

	def find_cheapest_flights(
			self, fly_from, fly_to, date_from, date_to, return_from, return_to, max_stopovers):
		"""
		:param str fly_from: city IATA code
		:param str fly_to: city IATA code
		:param str date_from: start date range (e.g. "25/03/2000")
		:param str date_to: end date range (e.g. 12/05/2001)
		:param str return_from: start date range for return (e.g. 25/07/2001)
		:param str return_to: end date range for return (e.g. 25/09/2001)
		:param int max_stopovers: number of stopovers (e.g. 2)
		:return: a specified number of cheapest flights available
		"""
		self.get_flight_info(fly_from, fly_to, date_from, date_to, return_from, return_to, max_stopovers)
		fares_dict = []
		for flight in self.flight_data['data']:
			flight_info = {
				"carrier": flight['airlines'][0],
				"departure": flight['flyFrom'],
				"arrival": flight["flyTo"],
				"price": flight['fare']['adults'],
				"departure_date_time": flight['local_departure'],
				"arrival_date_time": flight['local_arrival']
			}
			fares_dict.append(flight_info)

		# Sort the list of dictionaries by fare in ascending order
		sorted_fares = sorted(fares_dict, key=lambda x: x['price'])

		return sorted_fares[:1]


