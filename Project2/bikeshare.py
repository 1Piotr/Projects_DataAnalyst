
import time
import csv
from datetime import datetime, timedelta
import pprint as pp
## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'
def get_city():
    '''Asks the user for a city to be investigated and returns the csv file for that city's bike share data.
    Args:
        none.
    Returns:
         csv file
    '''
    cities = ['chicago', 'new york', 'washington']
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York, or Washington?\n')
            cities.remove(city.lower())
            break
        except ValueError:
            print('\nthat\'s not a city from the list')
     
    if city.lower() == 'chicago':
        return chicago     
    elif city.lower() == 'new york':
        return new_york_city
    else:
        return washington
 
def get_city_list(city_file):
    '''takes as an argument csv file and returns data converted into a list of
        ordered dictionaries
        Args:
            csv file
        Returns:
            list of ordered dictionaries
        '''

    with open(city_file) as csvfile:
        reader = csv.DictReader(csvfile)
        city_list =[]
        print('\nLoading data, please be patient...')
        for row in reader :
            b=      {k:v for k, v in row.items()}
            city_list.append(b)
    return city_list
def get_time_tuple():
    '''Asks the user if the data is to be filtered by month, weekday or
        no filter to be applied. Then returns a tuple with the first element
        month, day in datetime format and secondd element is a chosen month aor a day.
        If the user does not want to filter the data ('none', 'none') is returned
 
    Args:
        none.
    Returns:
         a two element tuple. First element is the type of the 
    '''
    
    months = ['january', 'february', 'march', 'april',
              'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday']
    time_periods  = ['month', 'day', 'none']
    while True:
        try:
            time_period  = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
            time_periods.remove(time_period.lower())
            break
        except ValueError:
            print('\nThat\'s not a correct fiter. Try one more time')
    if time_period.lower() == 'none':
        time_filter = 'none'
    elif time_period.lower() == 'month':
        time_period = '%B'
        while True:
            try:
                month = input('\nWhich month? January, February, March, '
                          'April, May, or June\n')
                months.remove(month.lower())
                time_filter = month.title()
                break
            except ValueError:
                print('\nThat\'s not a monthy from the list')           
    else:
        time_period = '%A'
        while True:
            try:
                day = input('\nWhich day? Monday, Tuesday, Wednesday, '
                        'Thursday, Friday, Saturday, Sunday \n')
                days.remove(day.lower())
                time_filter = day.title()
                break
            except ValueError:
                print('\nThat\'s not a day from the list')                
    time_tuple =  (time_period,time_filter)          
    return time_tuple
def get_city_data(time_tuple, city_list):
    '''takes as and aregumnet tuple and list of ordered dictionaries
        elements of the tuple correspond to the %Y-%m-%d %H:%M:%S time format.
         if the time tuple is ('none', 'none') then the filter is not applied
         and not filtered list of ordered dictionaries is returned
         

       Args:
           tuple, list of ordered dictionaries.
    Returns:
        list of ordered dictionaries filtered by month or day of the week
        '''

       
    if time_tuple[0] != 'none':
        print('\nPlease be a little bit more patient while we are preparing data...')
        city_data = list(filter(lambda row: datetime.strptime(row['Start Time'],
                        '%Y-%m-%d %H:%M:%S').strftime(time_tuple[0])== time_tuple[1], city_list))
    else:
        city_data = city_list
    return city_data
def break_down(city_data, filter_key):
    """  This function takes as an argument list of ordered dictionaries
            and filter_key. Where filter_key is a key in ordered dictionaries.
            Values associated to the key( fliter_key) in ordered dictionaries become keys in
            the new dictionary. Number how many times values (frequency)  associated to the key( fliter_key)
            apperead in ordered dictionaries become values in the new dictionary.
        
        Args:
            list of ordered dictionaries, string
        Returns:
            Dictionary
            """
    breakdown = {}
    for row in city_data:
        data_point = row[filter_key]
        if data_point in breakdown.keys():
            breakdown[data_point] +=1
        else:
            breakdown[data_point] = 1
    try:
         del breakdown['']
    except KeyError:
        pass
    return breakdown
def highest_key_value(breakdown):
    """takes an an argument dictionary and returns key taht is associates with
        the highest value
       Arguments:
               dictionary
       Return:
           dictionary key
               """
    popular = max(breakdown, key=breakdown.get)
    
    return popular
def popular_trip(city_data):
    """  This function takes as an argument list of ordered dictionaries - city_data
        
        Args:
            list of ordered dictionaries
        Returns:
            Dictionary"""
    trips={}
    for row in city_data:
        trip=row['Start Station'] + ' -To- ' +row['End Station']
        if trip in trips.keys():
            trips[trip] +=1
        else:
            trips[trip] = 1
    return trips
def popular_time(city_data, time_period):
    """  This function takes as an argument list of ordered dictionaries - city_data
        
        Args:
            list of ordered dictionaries, string
        Returns:
            Dictionary"""
    time_points = {}
    
    for row in city_data:
        dt = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
        if dt.strftime(time_period) in time_points.keys():
             time_points[dt.strftime(time_period)] +=1
        else:
             time_points[dt.strftime(time_period)] = 1
    return time_points


def highest_key_value(breakdown):
    """takes an an argument dictionary and returns key taht is associates with
        the highest value
       Arguments:
               dictionary
       Return:
           dictionary key
               """
    popular = max(breakdown, key=breakdown.get)
    
    return popular
def trip_duration(city_data):
    """The takes as an argument list of ordered dictionaries
        where the 'Trip Duration' on of the keys. returns the sum of
        values and avarage value as tuple
        Arguments:
            list of ordered dictionaries
        Returns:
            tuple"""
    total = 0
    for e in city_data:
        total += float(e['Trip Duration'])
    average_trip = total/len(city_data)
    return (total, average_trip)
def display_data(city_data):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        prints five elements from the list of ordered dictionaries
    '''
    responses = ['yes', 'no']
    i = 0
    while True:
        try:
            response = input('\nWould you like to view individual trip data?'
                        'Type \'yes\' or \'no\'.\n')
            responses.remove(response.lower())
            responses.append(response.lower())
            break
        except ValueError:
            print('Please choose  \'yes\' or \'no\'.')
        finally:
            while response.lower() == 'yes':
                pp.pprint(city_data[i: i + 5])
                i += 5
                while True:
                    try:
                        response = input('\nWould you like to view some more individual trip data?'
                            'Type \'yes\' or \'no\'.\n')
                        responses.remove(response.lower())
                        break
                    except ValueError:
                        print('Please choose  \'yes\' or \'no\'.')
                pass
        
def readable_timedelta(seconds):
    """The function's takes times in seconds and convert to
    hours, minutes and seconds
    Args:
        float
    Returns:
         string
    """
    seconds = int(round(seconds))
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    seconds = seconds % 3600 % 60
    return "{} hour(s) {} minute(s) {} second(s)".format(hours, minutes, seconds)
    
   
def restart():   
    restarts = ['yes', 'no']   
    while True:
        try:
            restart = input('\nWould you like to restart?'
                        'Type \'yes\' or \'no\'.\n')
            restarts.remove(restart.lower())
            break
        except ValueError:
            print('Please choose  \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()
    else:
        pass

def statistics():
    # Filter by city (Chicago, New York, Washington)
    city_file = get_city()
    city_list = get_city_list(city_file)
    # Filter by time period (month, day, none)
    time_tuple = get_time_tuple()
    time_period = time_tuple[0]
    city_data = get_city_data(time_tuple, city_list)
    print('\nCalculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        
        #call popular_time function and print the results
        # calling the break_down function and  providng city_data and '%B' as
        # arguments will return breakdown which is a dictionary that have 
        # each '%B' as a key, and number of times each '%B' appeared in city_data
        # as value
        breakdown = popular_time(city_data, time_period = '%B')
        # calling highest_key_value on breakdown dictionary will return the most month
        popular = highest_key_value(breakdown)
        print(breakdown)
        print('\nThe most popular month is - ' + str(popular))
                            
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == '%B':
        start_time = time.time()
 
        #call popular_time function and print the results
        # calling the break_down function and  providng city_data and '%A' as
        # arguments will return breakdown which is a dictionary that have 
        # each ''%A' as a key, and number of times each '%A' appeared in city_data
        # as value
        breakdown = popular_time(city_data, time_period = '%A')
        # calling highest_key_value on breakdown dictionary will return the most popular day of week
        popular = highest_key_value(breakdown)
        print(breakdown)
        print('\nThe most popular day is - ' + str(popular))
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular hour of day for start time?
    # calling the break_down function and  providng city_data and '%H' as
    # arguments will return breakdown which is a dictionary that have 
    # each '%H' as a key, and number of times each '%H' appeared in city_data
    # as value
    
    breakdown = popular_time(city_data, '%H')
    # calling highest_key_value on breakdown dictionary will return the most popular day of week
    popular = highest_key_value(breakdown)
    
    dt = datetime.strptime(str(popular), '%H')
    
    print('\nThe most popular hour is - ' + dt.strftime("%I %p"))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    # calling the trip_duration function with city_data as argument
    time_trip = trip_duration(city_data)
    total = time_trip[0]
    average = time_trip[1]
    print('\nThe total trip duration in the period - ' + readable_timedelta(total) +
          '\nThe average trip duration in the period - ' +  readable_timedelta(average))         
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    # calling the break_down function and  providng city_data and 'Start Station' as
    # arguments will return breakdown which is a dictionary that have 
    # each 'Start Station'r as a keys, and number of times each 'Start Station' appeared in city_data
    # as values
    breakdown_start = break_down(city_data, filter_key = 'Start Station')
    # calling the break_down function and  providng city_data and 'End Station' as
    # arguments will return breakdown which is a dictionary that have 
    # each 'End Station' as a keys, and number of times each 'End Station' appeared in city_data
    # as values
    breakdown_end = break_down(city_data, filter_key = 'End Station')
    # calling highest_key_value on  breakdown_start dictionary will return
    # the most popular start station
    popular_start =  highest_key_value(breakdown_start)
    # calling highest_key_value on  breakdown_end dictionary will return
    # the most popular end station
    popular_end = highest_key_value(breakdown_end)
    print('\nThe most popular Start Station - ' + str(popular_start) + '\nThe most popular End Station - ' + str(popular_end))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    # calling the popular_trip function and  providng city_data  as
    # argument will return breakdown which is a dictionary that have 
    # each trip route as a keys, and number of times each trip route appeared in city_data
    # as values
    breakdown = popular_trip(city_data)
    # calling highest_key_value on breakdown dictionary will return the most popular trip
    most_trip =  highest_key_value(breakdown)
    print('Most popular trip is From ' + str(most_trip))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    # calling the break_down function and  providng city_data and 'User Type' as
    # arguments will return breakdown which is a dictionary that have 
    # each 'User Type' as a keys, and number of times each 'User Type' appeared in city_data
    # as values
    breakdown = break_down(city_data,filter_key = 'User Type')
    print('\nThese are the counts for each user types:')
    pp.pprint(breakdown)
    print("That took %s seconds." % (time.time() - start_time))
    
    if city_file != washington:
    # What are the counts of gender?
    # calling the break_down function and  providng city_data and 'Gender' as
    # arguments will return breakdown which is a dictionary that have 
    # each gender as a keys, and number of times each gender appeared in city_data
    # as values
        print("\nCalculating the next statistic...")
        start_time = time.time()
        breakdown = break_down(city_data,filter_key = 'Gender')
        print('\nThese are the counts of gender:')
        print(breakdown)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
        # most popular birth years?
        # calling the break_down function and  providng city_data and 'Birth Year'
        # arguments will return breakdown which is a dictionary that have unique
        # birth years a keys and number of times each birth year appeared in city_data as values
        breakdown = break_down(city_data, filter_key = 'Birth Year')
        # calling highest_key_value on breakdown dictionary will return the most popular birth year
        most_year = highest_key_value(breakdown)
        # minimum value key from the list of keys will return the erliest birth year
        min_year = min(list(breakdown.keys()))
        # maximum value key from the list of keys will return the most recent birth year
        max_year = max(list(breakdown.keys()))
        print('\nThe most popular birth year - ' + str(most_year) + '\n'
              '\nThe youngest user - ' + str(max_year) + '\n'
              '\nThe oldest user - ' + str(min_year))
        print("That took %s seconds." % (time.time() - start_time))
    display_data(city_data)


    restart()

if __name__ == "__main__":
    statistics()

