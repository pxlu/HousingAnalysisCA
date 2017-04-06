from flask import Flask
from . import regions_df_to_json, nice_json, dps, data_source

app = Flask(__name__)

cities_data = regions_df_to_json(dps.get_specified_regions_data('all', data_source))
regions_data = dps.get_specified_regions_data('all', data_source)

# Data for all cities
@app.route('/data')
def get_all_data():
  return nice_json(cities_data)

# Data for a specific city
@app.route('/data/<city>')
def get_city_data(city):
  for key, value in cities_data.items():
    if key == city:
      return nice_json(value)
  error = { "Error" : "No data is available for {}".format(city) }
  return nice_json(error, 404)

# Data for a specific categories
@app.route('/category/<category>')
def get_category_data(category):
  category_data = dps.get_specified_category_data('all', regions_data, data_source)
  for key, value in category_data.items():
    if key == category:
      return nice_json(value.set_index('Date').to_dict())
  error = { "Error" : "No data is available for {}".format(category) }
  return nice_json(error, 404)
