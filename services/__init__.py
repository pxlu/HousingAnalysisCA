from flask import make_response
from ..scripts import data_processing as dps
import json
import pandas as pd

data_source = 'MLS_HPI_data_en'

def prep_df_for_json(dataframe_dict):

  out = {}
  for key in dataframe_dict.keys():
    dataframe = dataframe_dict[key][0].set_index('Date')
    out[key] = dataframe.to_dict()

  return out

def nice_json(arg, status=200):
  response = make_response(json.dumps(arg, sort_keys=True, indent=4))
  response.status_code = status
  response.headers['Content-Type'] = "application/json"
  return response
