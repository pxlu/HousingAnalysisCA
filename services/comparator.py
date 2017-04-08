from flask import Flask
from . import dps, data_source, nice_json, df_dict_to_json, regions_df_to_json,ListConverter

app = Flask(__name__)

regions_data = dps.get_specified_regions_data('all', data_source)
app.url_map.converters['list'] = ListConverter

@app.route('/compare/<list:params>')
def compare_cities(params):

  parameters = {str(param.split("=")[0]) : str(param.split("=")[1]) for param in params}
  for key, value in parameters.items():
    parameters[key] = value.split('+')

  out = dps.compare_on_regions(regions_data, None, None, None, cities=parameters['Cities'])
  
  return nice_json(df_dict_to_json(out))