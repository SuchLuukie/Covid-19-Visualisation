import requests
import json
import pandas as pd
import datetime
import csv
import os
from csv import reader

class UpdateData():
	"""docstring for UpdateData"""
	def __init__(self):
		self.data_url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
		self.csv_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

		self.update_data()
		
	
	"""The main function that updates data.json and data.csv to the new dataset"""
	def update_data(self):
		data = requests.get(self.data_url).json()
		data = self.assignGeocode(data)

		self.writeJSON("data.json", data)
		self.update_csv()


	"""Assigns the middle of the country's coordinate to the dictionary."""
	def assignGeocode(self, data):
		for item in data:
			geocode = self.findGeocode(data[item]["location"])
			data[item].update({"geocode": geocode})

		return data


	"""Finds the geocode to the given country."""
	def findGeocode(self, country):
		url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(country)
		response = requests.get(url).json()
		return [response[0]["lat"], response[0]["lon"]]


	"""Updates the CSV file to only display the current day's date"""
	def update_csv(self):
		data = self.loadJSON("data.json")

		dictionary = {"country": {}, "cases": {}}
		count = 0
		for item in data:
			country = data[item]["location"]

			try:
				cases = data[item]["data"][-1]["total_cases"]
			except KeyError:
				pass

			if country != "World":
				dictionary["country"].update({count: country})
				dictionary["cases"].update({count: round(cases)})
				count += 1

		self.writeJSON("csv.json", dictionary)

		df = pd.read_json("csv.json")
		df.to_csv("data.csv", index=None)

		os.remove("csv.json")

	"""Returns a json file."""
	def loadJSON(self, filename):
		with open(filename, "r") as json_file:
			return json.load(json_file)


	"""Writes the data to the file."""
	def writeJSON(self, filename, data):
		with open(filename, 'w') as f:
			json.dump(data, f, indent=4)