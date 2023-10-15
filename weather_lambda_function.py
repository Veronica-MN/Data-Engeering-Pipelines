import json
import pandas as pd
import requests
import sqlalchemy
from keys import gans_aws_key as awskey
from keys import my_api_key as wkey

def get_weather(cities_df, wkey):
  
  city_conditions_dict = {
            'city_id': [],
            'time' : [],
            'temp_min': [],
            'temp_max': [],
            'pop': [],
            'wind_speed': [],
            'description': [],
            'humidity': []}



  for i, city in enumerate(cities_df['city_id']):
      #city_name = cities_df.iloc[i]['city']
      forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={cities_df.iloc[i]['city']}&appid={wkey}&units=metric"
      response = requests.get(forecast_url)
      weather_json = response.json()
    
      for j in weather_json['list']:       
          city_conditions_dict['city_id'].append(city)
          city_conditions_dict['time'].append(j['dt_txt'])
          city_conditions_dict['temp_min'].append(j['main']['temp_min'])
          city_conditions_dict['temp_max'].append(j['main']['temp_max'])
          city_conditions_dict['wind_speed'].append(j['wind']['speed'])
          city_conditions_dict['humidity'].append(j['main']['humidity'])
          city_conditions_dict['pop'].append(j['pop'])
          city_conditions_dict['description'].append(j['weather'][0]['description'])

  weather_forecast_df = pd.DataFrame(city_conditions_dict)
  return weather_forecast_df




# database connection to mysql aws
def lambda_handler(event, context):
  schema="gans_aws"
  host="wbs-project5-db.csv6puy3yaat.eu-north-1.rds.amazonaws.com"
  user="admin"
  password= awskey
  port=3306
  con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

  cities_df = pd.read_sql('cities', con=con)
  weather_forecast_df = get_weather(cities_df, wkey)
  weather_forecast_df['time'] = pd.to_datetime(weather_forecast_df['time'])
  weather_forecast_df.to_sql('weather',con=con,if_exists='append',index=False)
  #weather_forecast_df.to_sql
  
#weather table data types
  
    # export the 'weather_forecast' into the 'weather'' table in aws mysql
  #weather_forecast_df.to_sql('weather', con=con, dtype=data_types, if_exists='append', index=False)
  #print(f'The weather table has been updated with {weather_forecast_df.shape[0]} records.')


#TODO 
  return {
    'statusCode': 200}
    #'body': json.dumps('Hello from Lambda!')}