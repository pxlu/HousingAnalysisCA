from __future__ import division
import json
import pprint

# Things to implement:
  # Describes average increase of parameter over the data for the time interval given
  # Growth comparisons: 
    # One vs One -- For cities/categories
    # One vs All -- For cities/categories

def load_json(json_name):
  with open(json_name, "r") as json_file:
    data = json.load(json_file)
  return data

def calculate_ratio_one_date(compare_type, compare_on, comparator_1, comparator_2, c1_value, c2_value, date=None):

  reverse = False
  if not date:
    return False
  c1_v, c2_v = c1_value[date], c2_value[date]
  if c1_v > c2_v:
    larger_value,smaller_value = c1_v,c2_v
  else:
    larger_value,smaller_value = c2_v,c1_v
    reverse = True
  ratio = larger_value / smaller_value
  if compare_type == 'categories':
    if not reverse: 
      return "{} -- {}'s {} is {}% greater than its {}".format(date, compare_on, comparator_1, round((ratio-1)*100, 2), comparator_2)
    else:
      return "{} -- {}'s {} is {}% greater than its {}".format(date, compare_on, comparator_2, round((ratio-1)*100, 2), comparator_1)
  else:
    if not reverse: 
      return "{} -- {}'s {} is {}% greater than {}'s".format(date, comparator_1, compare_on, round((ratio-1)*100, 2), comparator_2)
    else:
      return "{} -- {}'s {} is {}% greater than {}'s".format(date, comparator_2, compare_on, round((ratio-1)*100, 2), comparator_1)

def calculate_ratio_multi_dates(compare_type, compare_on, comparator_1, comparator_2, c1_value, c2_value, dates=[]):

  msgs = [xcalculate_ratio_one_date(compare_type, compare_on, comparator_1, comparator_2, c1_value, c2_value, date) for date in dates]

  return msgs

# ===== #

def one_vs_all_cities(json_name, city, compare_on, dates):

  data = load_json(json_name)
  out = {city + " vs " + city_name : one_vs_one_categories('cities', data, city, city_name, compare_on, dates) for city_name in data.keys() if city_name != city}

  return out

def convert_to_categories_dict(cities_dict):

  out = {}
  for city, data in cities_dict.items():
    for category_name, category_data in data.items():
      if category_name not in out.keys():
        out[category_name] = {city : category_data}
      else:
        out[category_name][city] = category_data

  return out

def one_vs_one_comparison(compare_type, data, comparator_1, comparator_2, compare_on, dates):

  shared_attributes = list(set([str(key) for key in data[comparator_1].keys()]) & set([str(key) for key in data[comparator_2].keys()]))

  out = []
  for key in compare_on:
    if key not in shared_attributes:
      continue
    # Over one date?
    if len(dates) == 1:
      ratio_quote = calculate_ratio_one_date(compare_type, key, comparator_1, comparator_2, data[comparator_1][key], data[comparator_2][key], dates[0])
      out.append(ratio_quote)
    else:
    # Over multiple dates ...
      ratio_quotes = calculate_ratio_multi_dates(compare_type, key, comparator_1, comparator_2, data[comparator_1][key], data[comparator_2][key], dates)
      out.append(ratio_quotes)

  return out

def main():
  data = load_json("../test-data/cal_vic.json")
  """
  out = one_vs_one_comparison('cities', data, "Calgary", "Victoria", ['One_Storey_Benchmark', 'Apartment_Benchmark'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  print out
  print one_vs_one_comparison('categories', convert_to_categories_dict(data), 'Apartment_Benchmark', 'Benchmark Average', ['Calgary'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  """
  out = one_vs_one_comparison('cities', data, "Calgary", "Victoria", ['One_Storey_Benchmark', 'Apartment_Benchmark'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  print out
  print one_vs_one_comparison('categories', convert_to_categories_dict(data), 'Apartment_Benchmark', 'Benchmark Average', ['Calgary'], ['Apr 2005', 'May 2005', 'Jun 2005'])
  # NEED TO IMPLEMENT PRINT RATIO FUNCTION FOR CATEGORIES

if __name__=='__main__':
  main()