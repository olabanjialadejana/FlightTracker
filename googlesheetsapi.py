import os
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from location_finder import LocationFinder
from security_keys import KIWI_API_KEY_location_finder


class GoogleSheetsAPI:

	def __init__(self, spreadsheet_id, scopes):
		self.spreadsheet_id = spreadsheet_id
		self.scopes = scopes

	def authenticate(self):
		credentials = None
		if os.path.exists("token.json"):
			credentials = Credentials.from_authorized_user_file("token.json", self.scopes)
		if not credentials or not credentials.valid:
			if credentials and credentials.expired and credentials.refresh_token:
				credentials.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
				credentials = flow.run_local_server(port=0)
			with open("token.json", "w") as token:
				token.write(credentials.to_json())
		return credentials

	def get_spreadsheet_values(self, range_name):
		"""
		:param range_name: specifies the range of the sheet e.g. "Sheet1!A1:C10"
		:return: returns all the data in the spreadsheet as a nested list
		"""
		credentials = self.authenticate()
		try:
			service = build("sheets", "v4", credentials=credentials)
			result = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
			values = result.get("values", [])
			return values
		except HttpError as error:
			print(error)

	def update_cell(self, value, cell_location):
		"""
		:param update_body: a dictionary that contains the value to be used for updating a cell
		:param value: the value to be added to the cell
		:param cell_location: the row id to be updated e.g ("Sheet1!A3")
		:return: returns a successful message
		"""
		credentials = self.authenticate()
		service = build("sheets", "v4", credentials=credentials)
		update_body = {
			'values': [[value]]
		}
		update_result = service.spreadsheets().values().update(
			spreadsheetId=self.spreadsheet_id,
			range=cell_location,
			body=update_body,
			valueInputOption='RAW'
		).execute()
		return f"Updated cell {cell_location} with value: {value}"

	def find_data_along_column(self, column_number, range_name):
		"""

		:param column_number: The first column in the googlesheet is number 0
		:param range_name: specifies the range of the sheet e.g. "Sheet1!A1:C10"
		:return: all data along the specified column
		"""
		full_spreadsheet = self.get_spreadsheet_values(range_name)
		column_values = [row[column_number] for row in full_spreadsheet]
		return column_values

	def register_new_user(self, range_name):
		first_name = input("Enter your first name: ")
		last_name = input("Enter your last name: ")
		home_city = input("Enter your home city: ")
		dream_city = input("Enter your dream vacation city: ")
		email = input("Enter your email: ")
		confirmation = input("Enter your email again: ")
		departure_start_date = input("What departure date do you want to start your search from? ")
		departure_end_date = input("What departure date do you want to your search to end? ")
		return_start_date = input("What return date do you want to start your search from? ")
		return_end_date = input("What return date do you want to your search to end? ")
		max_stop_over = int(input("What is the maximum number of stopovers you want? "))
		cut_off_price = int(input("What is your lowest price? (all fares are in USD) "))

		if email != confirmation:
			print("Emails do not match. Registration aborted.")
			return

		location_codes = LocationFinder(KIWI_API_KEY_location_finder)
		home_city_code = location_codes.find_city_code(city=home_city)
		dream_city_code = location_codes.find_city_code(city=dream_city)

		new_row = [first_name, last_name, email, home_city, dream_city, home_city_code, dream_city_code,
				   departure_start_date, departure_end_date, return_start_date, return_end_date, max_stop_over,
				   cut_off_price]
		next_row_range = f"Sheet1!A{len(self.find_data_along_column(0, range_name)) + 2}:" \
						 f"M{len(self.find_data_along_column(0, range_name)) + 2}"

		self.update_cell(new_row[0], next_row_range.split(":")[0])  # Update first name
		self.update_cell(new_row[1], next_row_range.split(":")[0].replace("A", "B"))  # Update last name
		self.update_cell(new_row[2], next_row_range.split(":")[0].replace("A", "C"))  # Update email
		self.update_cell(new_row[3], next_row_range.split(":")[0].replace("A", "D"))  # Update home city
		self.update_cell(new_row[4], next_row_range.split(":")[0].replace("A", "E"))  # Update dream city
		self.update_cell(new_row[5], next_row_range.split(":")[0].replace("A", "F"))  # Update home city code
		self.update_cell(new_row[6], next_row_range.split(":")[0].replace("A", "G"))  # Update dream city code
		self.update_cell(new_row[7], next_row_range.split(":")[0].replace("A", "H"))  # Update departure start date
		self.update_cell(new_row[8], next_row_range.split(":")[0].replace("A", "I"))  # Update departure end date
		self.update_cell(new_row[9], next_row_range.split(":")[0].replace("A", "J"))  # Update return start date
		self.update_cell(new_row[10], next_row_range.split(":")[0].replace("A", "K"))  # Update return end date
		self.update_cell(new_row[11], next_row_range.split(":")[0].replace("A", "L"))  # Update max stop overs
		self.update_cell(new_row[12], next_row_range.split(":")[0].replace("A", "M"))  # Update cut off price
		print("Welcome to the Cheap Flight Club!!!")
