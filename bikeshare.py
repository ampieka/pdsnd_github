import time
import pandas as pd
import numpy as np
import datetime
'''making a change because i have to'''
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['Chicago', 'New York City', 'Washington']
    city = input("Please enter the city data you would like to search (available cities are {0}, {1}, or {2}): ".format(
        valid_cities[0], valid_cities[1], valid_cities[2]))
    # loops till valid information is inputted
    while city.title() not in valid_cities:
        city = input(
            'ERROR! Invalid city entered.  Please enter valid city, either {0}, {1}, or {2}: '.format(valid_cities[0],
                                                                                                      valid_cities[1],
                                                                                                      valid_cities[2]))

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    month = input(
        "Please enter the month data you would like to search (available months are from {0} to {1}, or all): ".format(
            valid_months[0], valid_months[-2]))
    while month.title() not in valid_months:
        month = input(
            'ERROR! Invalid month entered.  Please enter valid month, valid months are from {0} to {1}, or all): '.format(
                valid_months[0], valid_months[-2]))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    day = input("Please enter the day of week data you would like to search (available days are {0}, or all): ".format(
        valid_days[0:-2]))
    while day.title() not in valid_days:
        day = input(
            'ERROR! Invalid day of week entered.  Please enter valid day of week, valid days of week are {0}, or all): '.format(
                valid_days[0:-2]))

    print('\nNow Displaying data for {0}, with a month filter of {1}, and a day filter of {2}!'.format(city.title(),
                                                                                                       month.title(),
                                                                                                       day.title()))
    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    # use the index of the months list to get the corresponding int
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_convert = [1, 2, 3, 4, 5, 6]
    df['month'] = df["month"].replace(month_convert, months)
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_count = value_count(df, 'month')
    print('The most common month for rentals is {0} with {1} rentals.'.format(month_count.idxmax(), month_count.max()))

    # TO DO: display the most common day of week
    day_count = value_count(df, 'day_of_week')
    print('The most common day of the week for rentals is {0} with {1} rentals.'.format(day_count.idxmax(),
                                                                                        day_count.max()))

    # TO DO: display the most common start hour
    hour_count = df['Start Time'].dt.hour.value_counts()
    print(
        'The most common start hour for rentals is {0} with {1} rentals.'.format(hour_count.idxmax(), hour_count.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_count = value_count(df, 'Start Station')
    print(
        'The most commonly used start station for rentals is {0} with {1} rentals.'.format(start_station_count.idxmax(),
                                                                                           start_station_count.max()))

    # TO DO: display most commonly used end station
    end_station_count = value_count(df, 'End Station')
    print('The most commonly used end station for rentals is {0} with {1} rentals.'.format(end_station_count.idxmax(),
                                                                                           end_station_count.max()))

    # TO DO: display most frequent combination of start station and end station trip
    combo_station_count = df['Start Station'] + ' to ' + df['End Station']
    combo_station_count = combo_station_count.value_counts()
    print(
        'The most frequent combination of start station and end station trip for rentals is {0} with {1} rentals.'.format(
            combo_station_count.idxmax(), combo_station_count.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def time_convert(seconds):
    '''
    converts the time from seconds to days, hours, minutes,seconds,milliseconds
    asks for the time in seconds
    returns the time in days, hours, minutes,seconds,milliseconds formate
    '''
    # converts seconds to a float as some of the csv files have the duration and ints
    seconds = float(seconds)
    # converts time to more user-friendly format
    time = datetime.timedelta(seconds=seconds)

    return time


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = time_convert(total_travel_time)
    print('The total travel time for all selected rentals is {0}.'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = time_convert(mean_travel_time)
    print('The mean travel time for all selected rentals is {0}.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def value_count(df, value):
    '''
    gets tha value count of the column provided
    asks for the dataframe, and column name
    returns the count of vaules
    '''
    count = df[value].value_counts()

    return count


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = value_count(df, 'User Type')
    print('The most common user type is: \n{0}'.format(user_type_count.to_string()))
    print('\n')

    # TO DO: Display counts of gender
    # tries to get gender but some files dont have gender so if it doesnt it will fail
    try:
        gender_count = value_count(df, 'Gender')
        print(gender_count.to_string())
    except:
        print('No gender information to display')
    print()
    # TO DO: Display earliest, most recent, and most common year of birth
    # tries to get birth year but some files dont have birth year so if it doesnt it will fail
    try:
        birth_year_count = value_count(df, 'Birth Year')
        print(
            'the earliest birth year is {0}, the most recent birth year is {1}, and the most common birth year is {2} with a count of {3}'.
            format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(birth_year_count.idxmax()),
                   birth_year_count.max()))
    except:
        print('No Birth Year infomation to display')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    '''returns 5 rows of data at a time'''
    line_count = 0
    while True:
        print(df.iloc[line_count:line_count + 5])
        see_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
        if see_data.lower() not in ['yes', 'y']:
            break
        else:
            line_count += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if see_data.lower() in ['yes', 'y']:
            show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
    main()
