import time
import pandas as pd
import numpy as np

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
    city = input("Please enter City name: ").lower()

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Sorry, looks like that city is invalid, enter either chicago,"
                     "new york city, or washington.")

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter month: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day: ").lower()

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
    df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df["month"] = df["Start Time"].dt.month
    df["week_day"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df["week_day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(str(df["month"].mode().values)))

    # display the most common day of week
    print("The most common day is: {}".format(str(df["week_day"].mode().values[0])))

    # display the most common start hour
    common_start_hour = df["Start Time"].dt.weekday_name.value_counts().idxmax()
    print("The most common hour is: {}".format(str(common_start_hour)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode().values[0]
    print("The most common start station is: {}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df["End Station"].mode().values[0]
    print("The most common end station is: {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df["combo_routes"] = df["Start Station"].astype(str) + " " + df["End Station"].astype(str)
    print("The most common trip is: {}".format(df["combo_routes"].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["Time_duration"] = df["End Time"] - df["Start Time"]

    # display total travel time
    print("Total travel time is: {}".format(str(df["Time_duration"].sum())))

    # display mean travel time
    print("The mean travel is: {}".format(str(df["Time_duration"].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of user types: {} ".format(df["User Type"].value_counts()))

    # Display counts of gender
    if "Gender" in df:
        male_gender = df["Gender"].astype(str).count("Male").sum()
        female_gender = df["Gender"].astype(str).count("Male").sum()
        print("The male count is: {}".format(int(male_gender)))
        print("The female count is: {}".format(int(female_gender)))

    # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is: {} ".format(
            str(int(df['Birth Year'].min())))
        )

        print("The most recent year of birth is:".format(
            str(int(df["Birth Year"].max()))))

        print("The most common year of birth is: {}".format(int(df["Birth Year"].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """ This displays contents of the csv files if the users request them."""
    start_loc = 0
    end_loc = 5

    display_file = input("Would you like to see the raw data?: ").lower()

    if display_file == "yes":
        while end_loc <= df.shape[0] - 1:
            print(df.iloc[start_loc:end_loc])
            start_loc += 5
            end_loc += 5
            # continue to ask if user wants data and stop when the user says no
            display_continue = input("Do you wish to continue?:").lower()
            if display_continue == "no":
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
