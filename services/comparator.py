from flask import Flask
from . import dps, data_source, nice_json, df_dict_to_json, regions_df_to_json, evaluate_params, ListConverter

app = Flask(__name__)

regions_data = dps.get_specified_regions_data('all', data_source)
app.url_map.converters['list'] = ListConverter

@app.route('/compare/cities/<list:params>')
def compare_cities(params):

  parameters = evaluate_params(params)

  out = dps.compare_on_regions(regions_data, None, None, None, cities=parameters['cities'])

  return nice_json(df_dict_to_json(out))

@app.route('/compare/categories/<list:params>')
def compare_categories(params):

  parameters = evaluate_params(params)

  out = dps.compare_on_categories(regions_data, attributes=parameters['categories'])

  return nice_json(df_dict_to_json(out))


