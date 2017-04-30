from __future__ import division
import json
import pprint
import os

# Things to implement:
  # Describes average increase of parameter over the data for the time interval given
  # Growth comparisons: 
    # One vs One -- For cities/categories
    # One vs All -- For cities/categories

def calculate_ratio(name, city_1, city_2, city_1_value, city_2_value, date=None):

  if not date:
    return False
  ratio = city_1_value[date] / city_2_value[date]
  # Reformat later using decimal notation [2fe or something...]
  # Need to change as:
    # For [name], on [Date], [Larger_Value_City] is [ratio]% over [Smaller_Value_Cities] 
  return "For {}, the ratio between {} and {} is {}".format(name, city_1, city_2, "1 : "+str(1+ratio))

def one_vs_one_cities(json_name, city_1, city_2, compare_on):

  with open(json_name, "r") as json_file:
    data = json.load(json_file)
  shared_categories = list(set([str(key) for key in data[city_1].keys()]) & set([str(key) for key in data[city_2].keys()]))

  for key in compare_on:
    if key not in shared_categories:
      continue
    # Over one date?
    ratio_quote = calculate_ratio(key, city_1, city_2, data[city_1][key], data[city_2][key], 'Apr 2005')
    print ratio_quote
    # Over multiple dates ...
    pass

def main():
  one_vs_one_cities("../test-data/cal_vic.json", "Calgary", "Victoria", ['One_Storey_Benchmark', 'Apartment_Benchmark'])

if __name__=='__main__':
  main()