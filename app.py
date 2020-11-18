# Import files and libraries.
from flask import Flask
import pandas as pd
import folium
import json

from update import UpdateData

app = Flask(__name__)
UpdateData()

@app.route("/")
def base():
	map = update()
	return map._repr_html_()
		

data = pd.read_csv("data.csv")
def update():
	geo = loadJSON("geojson.json")

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
	    fill_color='YlGn',
	    fill_opacity=0.7,
	    line_opacity=0.2,
	    legend_name='Total Cases'
	).add_to(map)

	return map


def loadJSON(filename):
	with open(filename, "r") as json_file:
		return json.load(json_file)


def writeJSON(filename, data):
	with open(filename, 'w') as f:
		json.dump(data, f, indent=4)


if __name__ == "__main__":
	app.run(debug=True)