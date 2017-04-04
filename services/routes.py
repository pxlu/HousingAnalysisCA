from flask import Flask
from . import prep_df_for_json, nice_json, dps, data_source

app = Flask(__name__)

@app.route('/city_data')
def get_all_data():
  return nice_json(prep_df_for_json(dps.get_specified_regions_data(['Victoria'], data_source)))

@app.route('/city_data/<city>')
def get_city_data(city):
  pass