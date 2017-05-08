"""
def one_vs_one_categories(ratio_type, data, category_1, category_2, cities, dates):

  shared_cities = list(set([str(key) for key in data[category_1].keys()]) & set([str(key) for key in data[category_2].keys()]))

  for key in cities:
    if key not in shared_cities:
      continue
    # Over one date?
    if len(dates) == 1:
      ratio_quote = calculate_ratio_one_date(ratio_type, key, category_1, category_2, data[category_1][key], data[category_2][key], dates[0])
      return ratio_quote
    else:
    # Over multiple dates ...
      ratio_quotes = calculate_ratio_multi_dates(ratio_type, key, category_1, category_2, data[category_1][key], data[category_2][key], dates)
      return ratio_quotes
      
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

def calculate_categories_ratio_one_date(city, benchmark_1, benchmark_2, benchmark_1_value, benchmark_2_value, date=None):

  # name = for each key in compare_on
  # city_1 = comparator 1
  # city_2 = comparator 2
  # c1 value = as is
  # c2 value = as is
  # date = date

  ## in this case, city_1_value[date] is equal to the benchmark's value for that date for [name] city

  reverse = False
  if not date:
    return False
  b1_v, b2_v = benchmark_1_value[date], benchmark_2_value[date]
  if b1_v > b2_v:
    larger_value,smaller_value = b1_v,b2_v
  else:
    larger_value,smaller_value = b2_v,b1_v
    reverse = True
  ratio = larger_value / smaller_value
  if not reverse: 
    return "{} -- {}'s {} is {}% greater than its {}".format(date, city, benchmark_1, round((ratio-1)*100, 2), benchmark_2)
  else:
    return "{} -- {}'s {} is {}% greater than its {}".format(date, city, benchmark_2, round((ratio-1)*100, 2), benchmark_1)

def calculate_categories_ratio_multi_dates(city, benchmark_1, benchmark_2, benchmark_1_value, benchmark_2_value, dates=[]):

  msgs = [calculate_categories_ratio_one_date(city, benchmark_1, benchmark_2, benchmark_1_value, benchmark_2_value, date) for date in dates]

  return msgs
"""