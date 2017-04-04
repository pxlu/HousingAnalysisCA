from flask import Flask
from . import dps, data_source, nice_json, prep_df_for_json, ListConverter

app = Flask(__name__)

cities_data = prep_df_for_json(dps.get_specified_regions_data('all', data_source))
app.url_map.converters['list'] = ListConverter

@app.route('/compare/<list:cities_to_compare>')
def compare_cities(cities_to_compare):
  cities = []
  for city in cities_to_compare:
    cities.append(city)

  return nice_json(cities)