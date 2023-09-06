from googlesheetsapi import GoogleSheetsAPI
from flight_search import FlightSearch
from datetime import datetime
from email_sender import EmailSender
from security_keys import SCOPES, SPREADSHEET_ID, RANGE_NAME, KIWI_API_KEY_flight_search
from security_keys import my_email, password

# Initialize the GoogleSheetsAPI and add customers. You can also view all customers within the google sheets
customer_data = GoogleSheetsAPI(spreadsheet_id=SPREADSHEET_ID, scopes=SCOPES)
# add new customer
# customer_data.register_new_user(range_name=RANGE_NAME)
# view all customers in the google sheet
all_customer_data = customer_data.get_spreadsheet_values(RANGE_NAME)

# Initialize the flight search class
search_flight = FlightSearch(KIWI_API_KEY_flight_search)

# search for flight and send email if the flight price meets customer cut-off
flight_details_list = []
flight_details = {}
for record in all_customer_data:
	fares = search_flight.find_cheapest_flights(
		fly_from=record[5],
		fly_to=record[6],
		date_from=record[7],
		date_to=record[8],
		return_from=record[9],
		return_to=record[10],
		max_stopovers=record[11])

	flight_details = {
		"Name": record[0],
		"Email": record[2],
		"Departure city": record[3],
		"Arrival city": record[4],
		"Departure time":
			(datetime.strptime(fares[0]['departure_date_time'], '%Y-%m-%dT%H:%M:%S.%fZ')).strftime(
				'%d/%m/%Y, %H:%M:%S'),
		"Arrival time":
			(datetime.strptime(fares[0]['arrival_date_time'], '%Y-%m-%dT%H:%M:%S.%fZ')).strftime('%d/%m/%Y, %H:%M:%S'),
		"Airline": fares[0]['carrier'],
		"Price": fares[0]['price'],
		"User_cutoff_price": record[12],
		"Price_difference": int(fares[0]['price'] - int(record[12]))
	}

	flight_details_list.append(flight_details)

for flight_detail in flight_details_list:
	print(flight_detail)
	if flight_detail['Price_difference'] < 0:
		emailer = EmailSender(my_email, password)
		recipient_email = flight_detail['Email']
		subject = "Cheap Flight Found!!!!!!!"
		content = f"Dear {flight_detail['Name']},\n\n" \
				  f"" \
				  f"We found a flight meeting your preference.\n\n" \
				  f"" \
				  f"Here is the flight information:\n\n" \
				  f"" \
				  f"Airline: {flight_detail['Airline']}. N.B: search for the airline name using the airline code\n\n" \
				  f"" \
				  f"Departure city: {flight_detail['Departure city']}\n\n" \
				  f"" \
				  f"Departure date and time: {flight_detail['Departure time']}\n\n" \
				  f"" \
				  f"Arrival city: {flight_detail['Arrival city']}\n\n" \
				  f"" \
				  f"Arrival date and time: {flight_detail['Arrival time']}\n\n" \
				  f"" \
				  f"Enjoy your Holidays!!!!!!!"
		emailer.send_email(to_email=recipient_email, subject=subject, content=content)
