from flask import make_response
from ..scripts import data_processing as dps
import json
import pandas as pd

data_source = 'MLS_HPI_data_en'

def regions_df_to_json(dataframe_dict):

  out = {}
  for key in dataframe_dict.keys():
    dataframe = dataframe_dict[key][0].set_index('Date')
    out[key] = dataframe.to_dict()

  return out

def df_dict_to_json(dataframe_dict):

  return {key : value.to_dict() for key, value in dataframe_dict.items()}

def nice_json(arg, status=200):
  response = make_response(json.dumps(arg, sort_keys=True, indent=4))
  response.status_code = status
  response.headers['Content-Type'] = "application/json"
  return response

def evaluate_params(params):

  parameters = {str(param.split("=")[0]) : str(param.split("=")[1]) for param in params}
  for key, value in parameters.items():
    parameters[key] = value.split('+')

  return parameters

from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):

  def to_python(self, value):
    return value.split('&')

  def to_url(self, values):
    return '&'.join(BaseConverter.to_url(value) for value in values)
