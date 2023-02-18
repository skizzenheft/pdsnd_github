"""Python File used for Udacity Nano Degree in Programming for Data Science with Python"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_dict = {'chi': 'chicago.csv', 'nyc': 'new_york_city.csv', 'was':'washington.csv', '':'chicago.csv'}
month_dict = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'yea': -1, '' : -1}
day_dict = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6, 'all': -1, '': -1}

def get_filters():
    # Asks user to specify a city, month, and day to analyze.
    #Returns:
    #    (str) city - name of the city to analyze
    #    (str) month - name of the month to filter by, or "all" to apply no month filter
    #    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    print("""Hello! Let's explore some US bikeshare data! What are you interested in?
    Please, answer by using the three-letter abbrevations in square brackets to let me know!
    By hitting 'Enter', there's no filter activated and Chigaco is chosen by default.""")


    while True: 
        try:
            city = city_dict[input("Chigaco [chi], New York City [nyc] or Washington [was]? ").lower()]
            break
        except KeyError:
            print('Please use: chi, nyc or was.')

    while True:
        try:
            month= month_dict[input(
                "[jan]uary, [feb]ruary, [mar]ch, [apr]il, [may], [jun]e or the whole [yea]r? ").lower()]
            break
        except KeyError:
            print('Please use jan, feb, mar, apr, may, jun or yea.')

    while True:
        try:    
            day = day_dict[input(
                "[mon]day, [tue]sday, [wed]nesday, [thu]rsday, [fri]day, [sat]urday, [sun]day, or [all] days of the week ? ").lower()]
            break
        except KeyError:
            print('Please use mon, tue, wed, thu, fri, sat, sun or all.')

    print('-'*60)
    #print('You are to explore data from {} during {} on {}'.format(city,month,day))
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the csv file to analyze
        (int) month - index of the month to filter by, or -1 to apply no month filter
        (int) day - index of the day of week to filter by, or -1 to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    with open(city, 'r') as f:    
        df = pd.read_csv(f)
        df['month'] = pd.to_datetime(df['Start Time']).dt.month
        df['day'] = pd.to_datetime(df['Start Time']).dt.dayofweek

    if month != -1:
        df = df[df['month'] == month]         # filter by month to create the new dataframe

    # filter by day of week if applicable
    if day != -1:
        df = df[df['day'] == day]         # filter by day of week to create the new dataframe
 
    print('='*60)

    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (df) df - data frame 
       
    """
    

    print('-'*60)
    print('\nThe most popular bike-sharing...\n')
    start_time = time.time()

    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    #print(df['month'].mode())
    #print(df['day'].mode())
   
    pop_m = df['month'].mode()[0] # most common month
    pop_d = df['day'].mode()[0]  #most common day of  week
    pop_h = df['hour'].mode()[0] #most common hour


    # only necessary if not filtered into month or day:
    month_key = list(filter(lambda x: month_dict[x] == pop_m, month_dict))[0] 
    print('... month: {}'.format(month_key)) 
    day_key = list(filter(lambda x: day_dict[x] == pop_d, day_dict))[0]
    print('... day of the week: {}'.format(day_key))


    print('... hour: {}'.format(pop_h))
        
    print("\n(It took %s seconds to calculate the most frequent times of travel.)"
    % round((time.time() - start_time),4))
    print('-'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('The most popular bike-sharing...\n')
    start_time = time.time()

    pop_start = df['Start Station'].mode()[0]
    print('...start station: {}'.format(pop_start))

    pop_end = df['End Station'].mode()[0]
    print('...end station: {}'.format(pop_end))

    combi = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False)
    print('...trip: {}'.format(combi.index[0])) 

    print("\n(It took about %s seconds to calculate the most popular stations and trip.)" % round((time.time() - start_time),4))
    print('-'*60)

def trip_duration_stats(df):
#     """Displays statistics on the total and average trip duration."""

     print('\nTravel time...\n')
     start_time = time.time()

     # calculate total travel time
     df['travel_time'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.total_seconds()

     seconds =df['travel_time'].sum()
     seconds = seconds % (24 * 3600)
     hour = seconds // 3600
     seconds %= 3600
     minutes = seconds // 60
     seconds %= 60

     print("... in total: %d:%02d:%02d [h:min:sec]" % (hour, minutes, seconds))
     
     # calculate mean travel time
     df['travel_time'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).dt.total_seconds()

     seconds =df['travel_time'].mean()
    
     seconds = seconds % (24 * 3600)
     hour = seconds // 3600
     seconds %= 3600
     minutes = seconds // 60
     seconds %= 60

     print("... on average: %d:%02d:%02d [h:min:sec]" % (hour, minutes, seconds))
     
     print("\n(It took about %s seconds to calculate travel time.)" % round((time.time() - start_time),4))
     print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    start_time = time.time()

    user_types = df['User Type'].value_counts()   # display counts of user types
    print('{} of the users have been subscribers, {} have been customers.'.format(user_types[0], user_types[1]))

    # run only if with chicago or new_york_city file:
    if 'Gender' in df.columns:
        gender= df['Gender'].value_counts() # display counts of gender
        gender_perc= df['Gender'].value_counts(normalize=True) # display counts of gender 
        print('{}({}%) of the users have been male, {}({}%) have been female.'
              .format(gender[0],round(gender_perc[0]*100,2), gender[1],round(gender_perc[1]*100,2)))
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        most = df['Birth Year'].value_counts().idxmax()
        print('{} has been the earliest, {} the most recent and {} the most common year of birth'
              .format(int(oldest), int(youngest),int(most)))
    

    print("\n(It took about %s seconds to calculate the above user statistics.)" %
          round((time.time() - start_time),4))
    print('-'*60)



def raw_data_prompt(df):
    # Asks user whether or not to show raw data for csv-file chosen.
    # Args:
    #    (df) df - load dataframe to show
    # Returns: head of raw data 

    print(df.head(5))
    i = 0
    while True: 
        raw = input("Do you want to sneak peak five lines of raw data? Type [y]es or [n]o.").lower() 
        if raw == 'y':
           print(df.iloc[i:i+5])
           i += 5
        else:
           break
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_prompt(df)

        restart = input('\nWould you like to restart? Enter [y]es or [n]o.\n').lower()
        if restart != 'y':
            break

        


if __name__ == "__main__":
	main()
        
        
