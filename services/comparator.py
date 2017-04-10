from flask import Flask
from . import dps, regions_data, nice_json, df_dict_to_json, regions_df_to_json, evaluate_params, ListConverter

app = Flask(__name__)
app.url_map.converters['list'] = ListConverter

def compare(params, compare_on):

  # start_date='Jan 2005', time_interval=12, interval_type='monthly'

  parameters = evaluate_params(params)
  out = dps.compare_on(compare_on, regions_data, parameters[compare_on])

  return nice_json(df_dict_to_json(out))

@app.route('/compare/cities/<list:params>')
def compare_cities(params):

  """
  Format:
    ...
  """

  out_data = compare(params, 'cities')
  if not out_data:
      error = { "Error" : "No data is available for {}".format(params['cities']) }
      return nice_json(error, 404)
  return out_data

@app.route('/compare/categories/<list:params>')
def compare_categories(params):

  """
  Format:
    ...
  """

  out_data = compare(params, 'categories')
  if not out_data:
    error = { "Error" : "No data is available for {}".format(params['categories']) }
    return nice_json(error, 404)
  return out_data


