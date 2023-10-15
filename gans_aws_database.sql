create database gans_aws;

use gans_aws;

-- creating cities table
create table if not exists cities (
                city_id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(100),
        country VARCHAR(100),
        latitude FLOAT,
        longitude FLOAT,
        population FLOAT
    );
select * from cities;


-- creating airports table
create table if not exists airports (
                icao VARCHAR(10),
                city_id INT NOT NULL,
                PRIMARY KEY (icao),
        FOREIGN KEY (city_id) REFERENCES cities(city_id)

);
select * from airports;


-- creating flights table
create table if not exists flights (
                flight_id INT AUTO_INCREMENT PRIMARY KEY,
        icao VARCHAR(10),
        departure_airport VARCHAR(100),
        local_arrival_time datetime,
        arrival_terminal VARCHAR(10),
        airline VARCHAR(100),
        flight_number VARCHAR(50),
        flight_status VARCHAR(100),
        FOREIGN KEY (icao) REFERENCES airports(icao)
);
select * from flights;


-- creating weather table
create table if not exists weather (
                weather_id INT AUTO_INCREMENT PRIMARY KEY,
                city_id INT NOT NULL,
        `time` datetime,
        temp_min FLOAT,
        temp_max FLOAT,
        pop FLOAT,
        wind_speed FLOAT,
        description VARCHAR(100),
        humidity INT,
        FOREIGN KEY (city_id) REFERENCES cities(city_id)

);
select * from weather;

