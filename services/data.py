from flask import Flask
from . import prep_df_for_json, nice_json, dps, data_source

app = Flask(__name__)

cities_data = prep_df_for_json(dps.get_specified_regions_data('all', data_source))

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
@app.route('/data/<category>')
def get_category_data(category):
  # TBD, need to do it on the backend script first
  pass