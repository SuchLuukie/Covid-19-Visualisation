import requests
import json

class UpdateData():
	"""docstring for UpdateData"""
	def __init__(self):
		self.data_url = "https://covid.ourworldindata.org/data/owid-covid-data.json"

		self.update_data()
		
	
	def update_data(self):
		data = requests.get(self.data_url).json()
		data = self.assignGeocode(data)

		self.writeJSON("data.json", data)


	def assignGeocode(self, data):
		for item in data:
			geocode = self.findGeocode(data[item]["location"])
			data[item].update({"geocode": geocode})

		return data


	def findGeocode(self, country):
		print(country)
		url = 'https://nominatim.openstreetmap.org/search/{}?format=json'.format(country)
		response = requests.get(url).json()
		return [response[0]["lat"], response[0]["lon"]]


	def loadJSON(self, filename):
		with open(filename, "r") as json_file:
			return json.load(json_file)


	def writeJSON(self, filename, data):
		with open(filename, 'w') as f:
			json.dump(data, f, indent=4)