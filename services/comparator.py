from flask import Flask
from . import dps, data_source, nice_json, df_dict_to_json, regions_df_to_json,ListConverter

app = Flask(__name__)

regions_data = dps.get_specified_regions_data('all', data_source)
app.url_map.converters['list'] = ListConverter

def evaluate_params(params):

  parameters = {str(param.split("=")[0]) : str(param.split("=")[1]) for param in params}
  for key, value in parameters.items():
    parameters[key] = value.split('+')

  return parameters

def compare(params, compare_on):

  # start_date='Jan 2005', time_interval=12, interval_type='monthly'

  parameters = evaluate_params(params)
  out = dps.compare_on(compare_on, regions_data, parameters[compare_on])

  return nice_json(df_dict_to_json(out))

@app.route('/compare/cities/<list:params>')
def compare_cities(params):

  return compare(params, 'cities')

@app.route('/compare/categories/<list:params>')
def compare_categories(params):

  return compare(params, 'categories')


