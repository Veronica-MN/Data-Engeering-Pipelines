# Data-Engeering-Pipeliness

![data-pipeline](aaron-jones-IJbfutoo7_U-unsplash.jpg)

## Gans e-Scooter
### Objective
You have been hired by Gans a startup developing e-scooter sharing system. The company aspires to operate in the most populous cities in the world. Gans has seen that its operational success depends on something more mundane: having its scooters parked where users need them. The company wants to anticipate as much as possible scooter movements. Predictive modelling is certainly on the roadmap, but the first step is to collect more data, transform it and store it appropriately.

### Problem
In an ideal world, scooters would rearranged organically by having certain users moving from point A to point B, and then an even number of users moving from point B to point A however this is not the case. Scooter movement looks to be asymmetries with some of the elements that contribute to this being: 

* In hilly cities, users tend to use scooters to go uphill and then walk downhill.
* In the morning, there is a general movement from residential neighbourhoods towards the city centre.
* Whenever it starts raining, e-scooter usage decreases drastically.
* Young tourists travelling with cheap flights are a big potential group of users, but they need to find scooters downtown or nearby touristic landmarks.

## Desigining Data Pipelines
The final goal is to have an automated data pipeline on the cloud which will provide seamless flow of data, data which is up to date and consistent. In order to make this possible, the first step is to gather data, transform it and store it the right way. 

#### Collecting Data 
There are various ways data has been collected in this project
* Through Web Scraping with Python and BeautifulSoup
* Using Apis - RapidAPI and OpenWeatherMap API
* exporting DataFrames into .csv files which can be downloaded as additional sources of data

