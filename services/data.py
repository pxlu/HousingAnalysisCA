from flask import Flask
from . import regions_df_to_json, nice_json, dps, data_source, regions_data, evaluate_params, ListConverter

app = Flask(__name__)
cities_data = regions_df_to_json(dps.get_specified_regions_data('all', data_source))
app.url_map.converters['list'] = ListConverter

# Data for all cities
@app.route('/data')
def get_all_data():

  """
  Format:
    ...
  """
  
  if not cities_data:
    error = { "Error" : "Cannot get data for cities." }
    return nice_json(error, 404)
  return nice_json(cities_data)

# Data for a specific city
@app.route('/data/<city>')
def get_city_data(city):

  """
  Format:
    ...
  """

  for key, value in cities_data.items():
    if key == city:
      return nice_json(value)
  error = { "Error" : "No data is available for {}".format(city) }
  return nice_json(error, 404)

# Data for a specific categories
@app.route('/category/<category>')
def get_category_data(category):

  """
  Format:
    ...
  """

  category_data = dps.get_specified_category_data('all', regions_data, data_source)
  for key, value in category_data.items():
    if key == category:
      return nice_json(value.set_index('Date').to_dict())
  error = { "Error" : "No data is available for {}".format(category) }
  return nice_json(error, 404)

@app.route('/predict/<list:predict_params>')
def simple_predict(predict_params):

  """
  Format:
    ...
  """

  # All params are list by default, need to make some cases handling singulars later
  
  out = {}
  parameters = evaluate_params(predict_params)

  # ONLY ONE REGION RIGHT NOW, BUT WILL BE MORE LATER IN A LIST OF REGIONS
  for region in parameters['predict_region']:
    region_dict = {}
    region_dict['predicted_price'], region_dict['coef'], region_dict['y_int'] = dps.predict_by_interval(regions_data, predict_on=parameters['predict_on'][0], predict_region=parameters['predict_region'][0], num_months_ahead=int(parameters['num_months_ahead'][0]))
    out[region] = region_dict

  if not out:
    error = { "Error" : "Cannot make a prediction for {}".format(parameters['predict_region']) }
    return nice_json(error, 404)
  return nice_json(out)
