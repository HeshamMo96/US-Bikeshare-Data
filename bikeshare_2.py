# References Used
# 1- https://pandas.pydata.org/docs/reference/series.html
# 2- https://dataindependent.com/pandas/pandas-to-datetime-string-to-date-pd-to_datetime/
# 3- https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output-of-dataframe-or-series

import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Please Choose City (Chicago, New York or Washington): ')) # City user Input
        except ValueError:
            print('\nPlease Enter a Valid String Value') # if the value is not str
            
        if city.lower() not in CITY_DATA: # if the user input value out of the three cities
            print('\nInvalid Input')
        else:
            break
                

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Please Choose Month (All, Jan, Feb, Mar, Apr, May or Jun): ')) # Month user Input
        if month.lower() != 'all':
            if month.lower() not in months: # if the user input value out of the three cities
                print('\nInvalid Input')
            else:
                break
        else:
            break
    


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Please Choose Day (All, Sat, Sun, Mon, Tue, Wed, Thu, Fri): ')) # Day user Input


    print('-'*40)
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
    print('Loading Data...')
    df = pd.read_csv(CITY_DATA[city])
    print('Loaded')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columnons
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.strftime("%a")
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The Most Common Month is: {}'.format(months[df['month'].mode()[0]-1]))

    # display the most common day of week
    print('The Most Common Day is: {}'.format(df['day'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The Most Common Hour (0 to 23) is: {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The Most Commonly Used Start Station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The Most Commonly Used End Station: {}'.format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + " => " + df['End Station']).mode()[0] # to get the mode of the combination
    print("The Most Frequent Combination is: {}".format(frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travil Time: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean Travil Time: {}'.format(df['Trip Duration'].mean()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts Of User Types: {}'.format(df['User Type'].value_counts().to_string())) # to.string to remove name and dtype

    # If Check Because Washington Don't Have Gender and Birth Year Columns
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        # Display counts of gender
        print('\nCounts Of Genders: {}'.format(df['Gender'].value_counts().to_string())) # to.string to remove name and dtype

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest Year of Birth: {}'.format(int(df['Birth Year'].min()))) #int() to delete float point 
        print('Most Recent Year of Birth: {}'.format(int(df['Birth Year'].max()))) #int() to delete float point 
        print('Most Common Year of Birth: {}'.format(int(df['Birth Year'].mode()[0]))) #int() to delete float point 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rows(df):
    """Displays Raw Data If User Want."""
    
    print(df.head()) # to Display First 5 Rows
    
    next = 0
    while True:
        raw_data = input('\nWould You Want To See Next 5 Rows? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5]) # Display The Next 5 Rows
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        while True:
            raw_data = input('\nWould You Want To See First 5 Rows? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break
            display_rows(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
