import time
import pandas as pd
import numpy as np

CITY_DATA = {"1" : "chicago.csv", "2" : "new_york_city.csv", "3" : "washington.csv"}

def get_filters():
        print('Hello! Let\'s explore some US bikeshare data!')
        
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city_selection = input("To view the available bikshare data , pls select one of those:\n (1)Chicago \n (2)New York City \n (3)Washington \n Choice: ").lower()
        while city_selection not in ("1" , "2" , "3"):
            print("\nThat's an invalid choice , please select one of the cities\n")
            city_selection = input("To view the available bikshare data , pls select one of those:\n (1)Chicago \n (2)New York City \n (3)Washington \n Choice: ").lower()
        else:
            print("Nice Choice! \n NOTE: if you want to change the selected choice , please restart the program")
            
            
    # get user input for month (all, january, february, ... , june)
        months = ['january' , 'february' , 'march' , 'april' , 'may', 'june', 'all']
        month = input("\n Please type one of the first six months or all: ").lower()
        while month not in months:        
            print("That's an invalid choice , please type a valid month")
            month = input("\n Please type one of the first six months or all: ").lower()
        else:
            print("Nice Choice! \n NOTE: if you want to change the selected choice , please restart the program")
            
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
        days = ['monday' , 'tuesday' , 'wednesday' , 'thursday' , 'friday', 'saturday' , 'sunday' , 'all']
        day = input("\n Please type one of seven days of the week or all: ").lower()
        while day not in days:   
            print("That's an invalid choice , please type a valid day")
            day = input("\n Please type one of seven days of the week or all: ").lower()
        else:
            print("Great Job! , You finished filtering")
        return(city_selection , month , day)
    

print('-'*40)

def load_data(city_selection, month, day):
    #Loading the data of the file into a dataframe
    df = pd.read_csv(CITY_DATA[city_selection])

    #Converting the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extarcting the month and day of the week to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    #Filtering by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        #Creating it into a dataframe 
        df = df[df['month'] == month]

    #Filtering by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df): # Popular times of travel
    print('\nCalculating Popular times of travel..\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0] # .value_counts().idxmax()
    print('Most popular month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most popular starting hour:', common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0] # .value_counts().idxmax()
    print('Most popular start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0] # .value_counts().idxmax()
    print('Most popular end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df["rout"] = df["Start Station"] + "-" + df["End Station"]
    common_station = df["rout"].mode()[0]
    print('Most popular station:', common_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time:', total_time/86400 , "Days")
    # TO DO: display mean travel time
    average_time = df['Trip Duration'].mean()
    print('Average travel time:' , average_time , "minutes")    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_count = df['User Type'].value_counts()
    print("Users Type:\n" , user_count)
    
    try:
    #Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("Gender of bike riders:\n" , gender_count)
    #Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print("Earliest birth year:" , earliest_year)
        recent_year = df['Birth Year'].max()
        print("Recent birth year:" , recent_year)
        common_year = df['Birth Year'].value_counts().idxmax()
        print("Most common year:" , common_year)
    except KeyError:
        #Fixing the issue with Washington
        print("This is data is not available for Washington")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#Displaying raw data if the user wanted
def display_raw_data(city_selection):
    print('\n Raw data is available to display... \n')
    display_raw = input("Do you want to have a look on the raw data?  Type (yes) or(no)").lower()
    
    while display_raw not in ['yes' , 'no']:
        print("Please type (yes) or (no)")
    
    while display_raw == "yes":
        try:
            for chunk in pd.read_csv(CITY_DATA[city_selection] , chunksize=5):
                print(chunk)
                display_raw = input("Do you want to have a look on more raw data?  Type (yes) or (no)").lower()
                if display_raw != "yes":
                    print("Thank You :), have a nice day")
                break
            break 
        except KeyboardInterrupt:
            print("Thank You :) Have a nice day ;)")
            

def main():
    while True:
        city_selection , month, day = get_filters()
        df = load_data(city_selection, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city_selection)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
