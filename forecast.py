import requests
import os
from datetime import date, datetime, time
from country_codes import codes
import calendar


key = os.environ.get('WEATHER_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/forecast'


def main():
    location = get_location()
    weather_data, error = get_forecast(location, key)

    if error:
        print('Sorry, could not get weather')
    else:
        list_of_forecasts = weather_data['list']

        for forecast in list_of_forecasts:
            get_forecast_info = get_forecast_details(forecast)
            # print(f'{location}\n{get_forecast_info}')
            print(get_forecast_info)


def get_location():
    city, country_code = '', ''
    while len(city) == 0 or not city.isalpha():
        city = input('Enter the city name: ').strip()

    country_name = ''
    while len(country_name) <= 4 or not country_name.isalpha():
        country_name = input('Enter country name: ')
        print(country_name)
    print(country_name)

    for country in codes:
        if country['Name'].lower == country_name.lower():
            country_code = country['Code']
            print(country_code)

    print(country_code)
    location = f'{city},{country_code}'
    return location


def get_forecast(location, key):

    try:
        units = 'imperial'
        query = {'q': location, 'units': units, 'appid': key}

        response = requests.get(base_url, params=query)
        response.raise_for_status()
        data = response.json()
        return data, None

    except Exception as ex:
        print(ex)
        print(response.text)  # added for debugging
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

        # return temp, timestamp, forecast_date
        return f'{day} at {forecast_date.time()}: Expect {description}.\nTemperature will be {temp}F with winds speed of {wind_speed} miles/hour\n'
    except Exception as ex:
        print(ex)
        return ex


if __name__ == '__main__':
    main()
