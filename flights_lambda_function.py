import json
import pandas as pd
import requests
import sqlalchemy
from datetime import datetime, date, timedelta
from pytz import timezone
from keys import gans_aws_key as awskey
from keys import my_api_key as wkey
from keys import rapidApi_key as fkey

def get_flights(airports_df):
    schema = "gans_aws"
    host = "wbs-project5-db.csv6puy3yaat.eu-north-1.rds.amazonaws.com"
    user = "admin"
    password = awskey
    port = 3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

    airports_df = pd.read_sql('airports', con=con)
    icao_list = airports_df['icao'].to_list()

    today = datetime.now().astimezone(timezone('Europe/Berlin')).date()
    tomorrow = (today + timedelta(days=1))

    times = [["00:00", "11:59"], ["12:00", "23:59"]]

    querystring = {
        "withLeg": "true",
        "direction": "Arrival",
        "withCancelled": "false",
        "withCodeshared": "false",
        "withCargo": "false",
        "withPrivate": "false",
        "withLocation": "true"
    }
    headers = {
        "X-RapidAPI-Key": fkey,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    flights_dict = {
        'icao': [],
        'departure_airport': [],
        'local_arrival_time': [],
        'arrival_terminal': [],
        'airline': [],
        'flight_number': [],
        'flight_status': []
    }

    for time in times:
        for icao in icao_list[0:2]:
            flight_url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{tomorrow}T{time[0]}/{tomorrow}T{time[1]}"
            response = requests.request("GET", flight_url, headers=headers, params=querystring)
            print(response.text)

            if response.status_code == 200:
                try:
                    flight_json = response.json()

                    for flight in flight_json['arrivals']:
                        flights_dict['icao'].append(icao)
                        flights_dict['departure_airport'].append(flight['departure']['airport']['name'])

                        flights_dict['airline'].append(flight['airline']['name'])
                        flights_dict['flight_number'].append(flight['number'])
                        flights_dict['flight_status'].append(flight['status'])

                        try:
                            flights_dict['arrival_terminal'].append(flight['arrival']['terminal'])
                        except:
                            flights_dict['arrival_terminal'].append('unknown')
                        try:
                            flights_dict['local_arrival_time'].append(flight['departure']['scheduledTime']['local'])
                        except:
                            flights_dict['local_arrival_time'].append(pd.NaT)
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON for icao {icao} and time {time}")
            else:
                print(f"Request failed for icao {icao} and time {time} with status code: {response.status_code}")

    flights_df = pd.DataFrame(flights_dict)
    flights_df['local_arrival_time'] = pd.to_datetime(flights_df['local_arrival_time'])
    print(flights_df)
    return flights_df

def lambda_handler(event, context):
    schema = "gans_aws"
    host = "wbs-project5-db.csv6puy3yaat.eu-north-1.rds.amazonaws.com"
    user = "admin"
    password = awskey
    port = 3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

    airports_df = pd.read_sql('airports', con=con)
    flights_df = get_flights(airports_df)
    # flights_df['local_arrival_time'] = pd.to_datetime(flights_df['time'])
    # print(flights_df)
    flights_df.to_sql('flights', con=con, if_exists='append', index=False)
    # weather_forecast_df.to_sql

    # TODO
    return {
        'statusCode': 200
        # 'body': json.dumps('Hello from Lambda!')
    }
