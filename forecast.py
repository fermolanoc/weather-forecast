import requests
import os
from datetime import datetime
from country_codes import codes
import calendar
import logging


# basic config for logging messages
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')


# get api key from local system
key = os.environ.get('WEATHER_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/forecast'


def main():
    location = get_location()
    # get forecast for specific location
    weather_data, error = get_forecast(location, key)

    if error:
        print(
            '\nSorry, could not get weather\nPlease verify city and country name are correct')
    else:
        get_results(location, weather_data)


def get_location():
    city, country_code = '', ''
    city_txt = 'h'

    # ask user city to look for
    while len(city) == 0 or not city_txt.isalpha():
        city = input('Enter the city name: ')
        # removes blank spaces on city name like 'New York' without modifying the name that will be returned
        city_txt = city.replace(" ", "")

    # user country name provided by user to find 2-letter codes list
    country_code = get_country_code()

    location = f'{city},{country_code}'
    return location


def get_country_code():
    code = ''
    country_name = ''
    # get country name from user
    while len(country_name) < 4 or len(code) == 0:
        country_name = input('Enter country name: ')

        for country in codes:
            if country['Name'] == country_name.title():
                code = country['Code']

    return code


def get_forecast(location, key):
    try:
        # generate a personalized query to combina with base url
        units = 'imperial'
        query = {'q': location, 'units': units, 'appid': key}

        response = requests.get(base_url, params=query)
        response.raise_for_status()
        data = response.json()
        return data, None

    except Exception as ex:
        # print(ex)
        logging.error(response.text)  # added for debugging
        return None, ex


def get_forecast_details(forecast):
    try:
        # temp details
        temp = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        wind_speed = forecast['wind']['speed']

        # time details
        timestamp = forecast['dt']
        forecast_date = datetime.fromtimestamp(timestamp)
        date_txt = forecast_date.date()
        day = calendar.day_name[date_txt.weekday()]

        return f'{day} at {forecast_date.time()}\nExpect {description}.\nTemperature will be {temp}F with winds speed of {wind_speed} miles/hour\n', None
    except Exception as error:
        return None, error


def get_results(location, weather_data):
    print(f'\n{location.upper()} next 5 days forecast (3-hour interval)\n')
    # get the list of 5-day forecast which contains 3-hour interval data
    list_of_forecasts = weather_data['list']

    for forecast in list_of_forecasts:
        # for each interval, get specific data to show details to user
        get_forecast_info, error = get_forecast_details(forecast)

        if error:
            logging.critical(
                f'Error: {error} when trying to access data from forecast list')
            print('There was an error when trying to access the data. Try again later\n')
        else:
            print(get_forecast_info)


if __name__ == '__main__':
    main()
