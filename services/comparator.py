from flask import Flask
from . import dps, data_source, nice_json, df_dict_to_json, regions_df_to_json,ListConverter

app = Flask(__name__)

cities_data = regions_df_to_json(dps.get_specified_regions_data('all', data_source))
regions_data = dps.get_specified_regions_data('all', data_source)
app.url_map.converters['list'] = ListConverter

@app.route('/compare/<list:cities_to_compare>')
def compare_cities(cities_to_compare):

  cities = []
  for city in cities_to_compare:
    cities.append(city)

  compared_regions_data = dps.compare_on_regions(regions_data, None, None, None, cities=cities)

  return nice_json(df_dict_to_json(compared_regions_data))