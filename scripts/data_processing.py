import pandas as pd
import numpy as np
import glob
import os
from collections import OrderedDict
from scipy import stats
from sklearn import linear_model

def get_regions(data_dir):

  # Get all the regions that have data available
  # For all .csv files in data_dir, get the names of all the tables and return it in a list
  # Return all names in lowercase
  csv_files = glob.glob(os.getcwd() + "/" + data_dir + "/*.csv")
  return csv_files

def get_region_names(data_dir):

  csv_files = glob.glob(os.getcwd() + "/" + data_dir + "/*.csv")
  return [region.split("/")[-1].split("-")[0].replace("_", " ") for region in csv_files]

def read_region_data(csv_file_path):

  data = pd.read_csv(csv_file_path)
  return (data, data.columns.values)

def get_available_categories(data_dir):

  return read_region_data(get_regions(data_dir)[0])[1]

def get_specified_regions_data(specified_regions, data_dir):

  all_regions = get_regions(data_dir)
  req_table_regions = []

  if isinstance(specified_regions, str) and specified_regions.lower() == 'all':
    all_region_data = OrderedDict()

    for region_path in all_regions:
      csv_file = region_path.split("/")[-1]
      if len(csv_file.split("_")) > 1:
        all_region_data[" ".join(map(str.capitalize, csv_file.split("_"))).split("-")[0]] = read_region_data(region_path)
      else:
        all_region_data[csv_file.split("-")[:-1][0].capitalize()] = read_region_data(region_path)

    return all_region_data

  for region in all_regions:
    csv_file = region.split("/")[-1]
    if len(csv_file.split("_")) > 1 and " ".join(map(str.capitalize, csv_file.split("_"))).split("-")[0] in specified_regions:
        req_table_regions.append(region)
    elif csv_file.split("-")[:-1][0].capitalize() in specified_regions:
      req_table_regions.append(region)

  return {region.split("/")[-1].split("-")[:-1][0] : read_region_data(region) for region in req_table_regions}

def get_specified_category_data(specified_categories, regions_data, data_dir):

  if specified_categories == 'all':
    specified_categories = get_available_categories(data_dir)

  category_data = {}
  for category in specified_categories:
    category_frame = []
    region_names = []
    dates = None
    for key,value in regions_data.items():
      category_frame.append(value[0][category])
      region_names.append(key)
      dates = value[0]['Date']
    out_df = pd.concat(category_frame, axis=1, keys=[name for name in region_names])
    out_df['Date'] = dates
    category_data[category] = out_df

  return category_data

def compute_region_time(region_data, start_date, time_interval, interval_type):

  try:
    time_interval_multi = 1
    start_index = region_data[region_data['Date'] == start_date].index.tolist()[0]

    if interval_type == 'yearly':
      if time_interval < 12:
        raise ValueError
      time_interval_multi = 12

    return start_index, time_interval_multi

  except Exception as e:
    print e

def get_growth_trend(start_date, time_interval, interval_type, region, select_on=None):

  region_data, data_cols = read_region_data(region)

  try:
    start_index, time_interval_multi = compute_region_time(region_data, start_date, time_interval, interval_type)

    if select_on is None or select_on not in data_cols:
      raise TypeError

    growth_trend = (region_data.loc[:, select_on] - region_data.shift(time_interval_multi).loc[:, select_on]) / region_data.shift(time_interval_multi).loc[:, select_on]

    region_data.loc[:, " ".join([interval_type.capitalize(), 'Growth'])] = pd.Series(["{0:.2f}%".format(val * 100) for val in growth_trend])

    return region_data[['Date', select_on, " ".join([interval_type.capitalize(), 'Growth'])]][start_index:start_index+time_interval*time_interval_multi:time_interval_multi]

  except Exception, e:
    raise e

def compare_regions(to_compare_dict, start_date, time_interval, interval_type, attributes=[]):

  try:
    if len(attributes) == 0:
      raise ValueError

    all_data = {}
    for category in attributes:
      out_data = []
      dates = None      
      for df in to_compare_dict.values():
        out_data.append(df[0].loc[:, category])
        dates = df[0].loc[:, 'Date']

      # Create the dataframe from the list of Series
      out_df = pd.concat(out_data, axis=1, keys=[k for k in to_compare_dict.keys()])
      # Create the average column
      category_mean = pd.Series([row.mean() for index, row in out_df.iterrows()])
      out_df['Average'] = category_mean
      out_df['Date'] = dates
      out_df = out_df[out_df.columns.tolist()[-2:] + out_df.columns.tolist()[:-2]]

      # Change each row to the difference of the average
      for index, row in out_df.iterrows():
        for item in out_df.columns.tolist()[2:]:
          out_df.loc[(index, item)] = out_df.loc[(index, item)] - out_df.loc[(index, 'Average')]

      start_index, time_interval_multi = compute_region_time(out_df, start_date, time_interval, interval_type)
      all_data[category] = out_df[start_index:start_index+time_interval*time_interval_multi:time_interval_multi].set_index('Date')

    return all_data

  except Exception, e:
    raise e

def compare_categories(to_compare_data, start_date, time_interval, interval_type, attributes=[]):

  # Attributes is regions in this cases

  all_category_data = {}
  for category in attributes:
    category_data = []
    dates = None
    for region, data in to_compare_data.items():
      category_data.append(data[0].loc[:, category])
      dates = data[0].loc[:, 'Date']
    # Create the dataframe
    out_df = pd.concat(category_data, axis=1, keys=[k for k in to_compare_data.keys()])
    # Assign the values to the respective columns
    out_df['Date'] = dates
    out_df = out_df[out_df.columns.tolist()[-1:] + out_df.columns.tolist()[:-1]]
    # Change each row to the difference of the average
    for index, row in out_df.iterrows():
      for item in out_df.columns.tolist()[2:]:
        out_df.loc[(index, item)] = out_df.loc[(index, item)] - out_df.loc[(index, 'Aggregate')]
    # Section by specified time interval
    start_index, time_interval_multi = compute_region_time(out_df, start_date, time_interval, interval_type)
    # Add it to the dictionary
    all_category_data[category] = out_df[start_index:start_index+time_interval*time_interval_multi:time_interval_multi]

  return all_category_data

def predict_by_interval(data, predict_on=None, predict_regions=None, num_months_prior=None, num_months_ahead=12):

  dates = [i for i, b in enumerate(range(0, len([j for j, element in enumerate(data[predict_regions][0]['Date'])]), 12))]
  region_data = [element for element in data[predict_regions][0][predict_on]]
  region_data = [sum(region_data[current: current+12])/12 for current in xrange(0, len(region_data), 12)]

  if num_months_prior is None:
    num_months_prior = len(dates)

  if num_months_prior > len(dates) or not predict_on or not predict_regions:
    raise ValueError

  dates = np.reshape(dates[:num_months_prior], (len(dates[:num_months_prior]), 1))
  region_data = np.reshape(region_data[-num_months_prior:], (len(region_data[-num_months_prior:]), 1))

  linear_mod = linear_model.LinearRegression()
  linear_mod.fit(dates, region_data)
 
  prediction = linear_mod.predict(len(dates) + num_months_ahead)

  # prediction, slope, y-intercept
  return prediction[0][0], linear_mod.coef_[0][0], linear_mod.intercept_[0]

if __name__ == '__main__':

  # Use cases:
    # 1a. Use get_specified_regions_data -> Get data for those regions
    # 1b. Feed it into compare_regions with a list of attributes to compare to in order to see the difference between them

    # 2a. get_specified_regions_data -> Get data for those regions
    # 2b. Use predict_by_interval to predict future prices with those values

    # Have to redo compare_categories to be the same format as compare_regions

  # reg = get_regions('MLS_HPI_data_en')
  # print reg

  #reg2 = get_region_names('MLS_HPI_data_en')
  #print reg2
  #ya2 = get_growth_trend('Jan 2006', 24, 'monthly', '/Users/peter/gitProjects/HousingProjections/MLS_HPI_data_en/Victoria-Table 1.csv', 'Composite_Benchmark')
  #print ya2
  ar = get_specified_regions_data(['Victoria'], '../MLS_HPI_data_en')
  # print ar
  # print type(ar['Victoria'][0]['One_Storey_HPI'])
  ar2 = get_specified_regions_data('all', '../MLS_HPI_data_en')
  # cat_data = get_specified_category_data(['One_Storey_Benchmark'], ar2, '../MLS_HPI_data_en')
  # print cat_data
  # print type(ar2['Victoria'])
  # print ar['Victoria'][0]['One_Storey_Benchmark']
  # print ar['Victoria'][0]['Composite_HPI']
  asd = compare_regions(ar2, 'Jan 2005', 12, 'monthly', ['Composite_HPI', 'Single_Family_HPI'])
  print asd['Composite_HPI']
  # vc = compare_categories(ar2, 'Jan 2005', 12, 'monthly', ['Composite_HPI', 'Single_Family_HPI', 'One_Storey_Benchmark'])
  # print vc
  # predicted_price, coef, y_int = predict_by_interval(ar, predict_on='One_Storey_Benchmark', predict_regions='Victoria', num_months_ahead=6)
  # print predicted_price, coef, y_int
  #for key, val in vc.items():
  #  print val