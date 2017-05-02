from __future__ import division
import json

# Things to implement:
  # Describes average increase of parameter over the data for the time interval given
  # Growth comparisons: 
    # One vs One -- For cities/categories
    # One vs All -- For cities/categories

def load_json(json_name):
  with open(json_name, "r") as json_file:
    data = json.load(json_file)
  return data

def calculate_ratio_one_date(name, city_1, city_2, city_1_value, city_2_value, date=None):

  reverse = False
  if not date:
    return False
  c1_v, c2_v = city_1_value[date], city_2_value[date]
  if c1_v > c2_v:
    larger_value,smaller_value = c1_v,c2_v
  else:
    larger_value,smaller_value = c2_v,c1_v
    reverse = True
  ratio = larger_value / smaller_value
  if not reverse: 
    return "{} -- {}'s {} is {}% greater than {}'s".format(date, city_1, name, round((ratio-1)*100, 2), city_2)
  else:
    return "{} -- {}'s {} is {}% greater than {}'s".format(date, city_2, name, round((ratio-1)*100, 2), city_1)

def calculate_ratio_multi_dates(name, city_1, city_2, c1_values, c2_values, dates=[]):

  msgs = [calculate_ratio_one_date(name, city_1, city_2, c1_values, c2_values, date) for date in dates]

  return msgs

def one_vs_one_cities(data, city_1, city_2, compare_on, dates):

  shared_categories = list(set([str(key) for key in data[city_1].keys()]) & set([str(key) for key in data[city_2].keys()]))

  for key in compare_on:
    if key not in shared_categories:
      continue
    # Over one date?
    if len(dates) == 1:
      ratio_quote = calculate_ratio_one_date(key, city_1, city_2, data[city_1][key], data[city_2][key], dates[0])
      return ratio_quote
    else:
    # Over multiple dates ...
      ratio_quotes = calculate_ratio_multi_dates(key, city_1, city_2, data[city_1][key], data[city_2][key], dates)
      return ratio_quotes

# ===== #

def one_vs_all_cities(json_name, city, compare_on, dates):

  data = load_json(json_name)
  out = {city + " vs " + city_name : one_vs_one_cities(data, city, city_name, compare_on, dates) for city_name, city_data in data.items() if city_name != city}

  return out

def main():
  # one_vs_one_cities("../test-data/cal_vic.json", "Calgary", "Victoria", ['One_Storey_Benchmark', 'Apartment_Benchmark'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  out = one_vs_all_cities("../test-data/cal_vic.json", "Calgary", ['One_Storey_Benchmark', 'Apartment_Benchmark'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  print out

if __name__=='__main__':
  main()