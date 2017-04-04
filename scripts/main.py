import sys
import data_processing as dps

data_source = '../MLS_HPI_data_en'

def main():
  options_list = ['Q', 'C1', 'C2', 'D']
  print 'Hi! Welcome to Housing Projections, created to help you analyze data for the housing market in major Canadian cities.'
  city_list = dps.get_region_names(data_source)
  execute_option(city_list, options_list)

def execute_option(city_list, options_list, cont=True):

  if not cont:
    sys.exit(0)

  prompt = options_prompt().upper()
  cont = cont

  try:
    if prompt not in options_list:
      raise ValueError
    if prompt == 'Q':
      print 'Thanks for using Housing Projections!'
      cont = False
    if prompt == 'C1':
      print city_list
    if prompt == 'C2':
      print dps.get_available_categories(data_source)
    if prompt == 'D':
      city_choice = raw_input('Please select a city from the available data.\n>>> ')
      print dps.get_specified_regions_data([city_choice], data_source)
  except ValueError:
    print 'Sorry, that is not a valid option.'
  finally:
    execute_option(city_list, options_list, cont)

def options_prompt():

  prompt = raw_input('Please select a option:\
    \n[C1]: Get the list of city information available\
    \n[C2]: Get the list of data categories available for each city\
    \n[D]: Get data for a specific city\
    \n[CR]: Compare data between regions\
    \n[CC]: Compare data between categories\
    \n[Q]: Save and Quit\
    \n>>> ')

  return prompt

# Get the trend over a 2, 5, and 10 year periods of growth or decay
# Same as describe():
  # > Mean
  # > Median
  # > Greatest
  # > Lowest
# Compare two regions over the same period
	# Compare three (or more) regions over the same period
# Given a region and a time period, predict future house prices using regression
  # > Option to use a specific past time interval to predict future prices
  # > Option to predict X time intervals into the future

# Get trends for the various categories --
  # As above, same as describe
# Compare two categories over the same time period
  # Compare three (or more) over the same period

# Given a category and a time period, predict future house prices using regression
  # > Option to use a specific past time interval to predict future prices
  # > Option to predict X time intervals into the future

if __name__=='__main__':
	main()