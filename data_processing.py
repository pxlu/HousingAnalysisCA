import pandas as pd
import numpy as np
import glob
import os

import hp_classes as hpc

def get_regions(data_dir):

  # Get all the regions that have data available
  # For all .csv files in data_dir, get the names of all the tables and return it in a list
  # Return all names in lowercase
  csv_files = glob.glob(os.getcwd() + "/" + data_dir + "/*.csv")
  return csv_files

def region_files_to_names(region_list):

  return [csv_file.split("/")[-1].split("-")[:-1][0].capitalize() for csv_file in region_list]

def read_region_data(csv_file_path):

  data = pd.read_csv(csv_file_path)
  return (data, data.columns.values)

def get_specified_regions_data(specified_regions, data_dir):

  all_regions = get_regions(data_dir)
  req_table_regions = []

  for region in all_regions:
    csv_file = region.split("/")[-1]
    if len(csv_file.split("_")) > 1 and " ".join(map(str.capitalize, csv_file.split("_"))).split("-")[0] in specified_regions:
        req_table_regions.append(region)
    elif csv_file.split("-")[:-1][0].capitalize() in specified_regions:
      req_table_regions.append(region)

  return {region.split("/")[-1].split("-")[:-1][0] : read_region_data(region) for region in req_table_regions}

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

  # Attributes is categories in this case

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
        # Need to merge all the series of a specific category into a single dataframe indexed by date to compare
        # Make a new dataframe comprised of all the individual Series, indexed by date
      out_df = pd.concat(out_data, axis=1, keys=[k for k in to_compare_dict.keys()])
      out_df['Date'] = dates
      start_index, time_interval_multi = compute_region_time(out_df, start_date, time_interval, interval_type)
      all_data[category] = out_df[start_index:start_index+time_interval*time_interval_multi:time_interval_multi]

    return all_data
  except Exception, e:
    raise e

def compare_categories(time_interval, attributes=[]):

  # Attributes is regions in this case

  pass

def predict_by_interval(predict_on=None, num_months_prior=24, num_months_ahead=12):

  pass

if __name__ == '__main__':
  #ya2 = get_growth_trend('Jan 2006', 24, 'monthly', '/Users/peter/gitProjects/HousingProjections/MLS_HPI_data_en/Victoria-Table 1.csv', 'Composite_Benchmark')
  #print ya2
  ar = get_specified_regions_data(['Victoria', 'Regina', 'Greater Toronto'], 'MLS_HPI_data_en')
  asd = compare_regions(ar, 'Jan 2005', 12, 'monthly', ['Composite_HPI', 'Single_Family_HPI'])
  print asd['Composite_HPI']