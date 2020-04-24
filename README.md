# carris-analysis

## Project Goal
This project aims to provide the means to analyse data of the Lisbon Public Bus Transport Network [Carris](http://www.carris.pt/).

It was used the public Carris API in order to obtain the data. The API is refferenced here: https://carris.tecmic.com/index.html 

## Dependencies
Install the following in your machine
* docker version 19.03.8
* docker-compose version 1.25.4

## Run
To spin up this project simple execute the following steps in a machine with docker installed:

* Clone the project with `git clone https://github.com/ricardojdferreira/carris-analysis.git`
* Define new current directory with `cd carris-analysis`
* Copy the *.env-template* file with the command `cp .env-template .env`. Having your `.env` file, specify:
    * Host where the stack lives
    * Database's password
    * Number of days for analysis - You can start with the 7 previous days
* Spin up the docker service by typing `docker-compose -f docker-compose.yml up`
* Access the interface on http://localhost:3000
    * Within the Metabase interface, create a local account and add the data so you can start exploring - more information here: https://www.metabase.com/docs/v0.35.3/setting-up-metabase.html

## Stack
The stack for this project is compose by:
* A Postgres database https://www.postgresql.org/
* A Metabase instance https://www.metabase.com/
* A custom Extractor with the following setup:
    * `extractor.py`, that allows the interaction with Carris API, exposing a `GTFS()` class with download and extraction functions on top of the data
    * `dbutils.py`, which interfaces the `Extractor` application with the Postgres DB
    * `main.py`, managing the ETL, **E**xtracting Carris data, **T**ransforming it for analysis and **L**oading the result into the Postgres database  