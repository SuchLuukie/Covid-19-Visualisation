# Import files and libraries.
from flask import Flask
import pandas as pd
import folium
import json

from update import UpdateData

UpdateData()
app = Flask(__name__)

"""Route for the choropleth map."""
@app.route("/choropleth")
def choro():
	map = choro_updater()
	return map._repr_html_()

"""Route for the circle map."""
@app.route("/")
def base():
	map = circle_updater()
	return map._repr_html_()


"""Function to showcase the data as a choropleth map."""
def choro_updater():
	geo = loadJSON("geojson.json")
	data = pd.read_csv("data.csv")

	map = folium.Map(
		location=[-0.023559, 37.9061928],
		max_bounds=True,
		zoom_start=2,
		)

	folium.Choropleth(
	    geo_data=geo,
	    name='choropleth',
	    data=data,
	    columns=['country', 'cases'],
	    key_on='feature.properties.name',
	    fill_color='YlOrRd',
	    fill_opacity=0.7,
	    line_opacity=0.2,
	    legend_name='Total Cases'
	).add_to(map)

	return map


"""Function to showcase the data as a circle map."""
def circle_updater():
	data = loadJSON("data.json")

	map = folium.Map(
		location=[-0.023559, 37.9061928],
		max_bounds=True,
		zoom_start=2,
		tiles='CartoDB dark_matter'
		)

	for point in data:
		country = data[point]["location"]

		if country != "World":
			try:
				cases = data[point]["data"][-1]["total_cases"] / 10
			except KeyError:
				continue

			folium.Circle(
				location=data[point]["geocode"],
				popup=f'''{country} <br> {round(data[point]["data"][-1]["total_cases"])}''',
				radius=cases,
				color='crimson',
				fill=True,
				fill_color='crimson'
			).add_to(map)

	return map

"""Function to easily return json files."""
def loadJSON(filename):
	with open(filename, "r") as json_file:
		return json.load(json_file)

"""Functiont o easily write to a json file."""
def writeJSON(filename, data):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=4)

"""Function that starts the Flask app."""
if __name__ == "__main__":
	app.run(debug=True)
