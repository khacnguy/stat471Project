
# Rental Price Simulation Project

## Introduction
We wanted to investigate how economic, social and environmental factors affect rent prices using mathematical techniques and Markov models.

Firstly, we used maximum likelihood estimation and gradient descent to estimate the parameters of our model. From this, we got initial data to put into our voter model.

Then, we used a three-state voter model on this initial data to simulate rental price changes over multiple years.

## Installation
Clone the repository through the following commands:
```
git clone https://github.com/khacnguy/stat471Project.git
```
or
```
git clone git@github.com:khacnguy/stat471Project.git
```
Library

## Usage
Method 1: Using Makefile
- Go to the directory with the `Makefile` and type in command line the following:
```
make get_data
```
```
make get_parameters
```
```
make simul
```

Method 2: Manual
- Run the following commands:
```
rm -f database.db
touch database.db
python3 load_data/create_tables.py
python3 load_data/load_data.py
python3 load_data/visualization.py
python3 load_data/MLE.py
python3 load_data/simulation.py
rm -f *.json
python3 simulation/generate_initial_data.py
python3 simulation/get_simulation_data.py
python3 simulation/us_map.py
```

## Data
- `us_states_name.csv`: Data of the US states (only using names) \
- `area.csv`: Data of the Canadian cities' land areas \
- `csi,pd.csv`: Data for Crime Severity Index and population density of each city \
- `employment_rate.csv`: Data for employment rates in each city \
- `homicide_rates.csv`: Data for homicide rates in each city \
- `population.csv`: Data for population in each city \
- `rental_price.csv`: Data of rental prices in each city \


## Structure and Components
Calculate parameters for linear models using maximum likelihood estimation

- `create_tables.py`: Create tables for database 
- `load_data.py`: Load data for simulation 
- `visualization.py`: Clean data and visualize 
- `MLE.py`: Calculate parameters for linear models using maximum likelihood estimation 
- `simulation.py`: Simulate employment rate change based on rental price and put in database 
- `gradient_descent.py`: Apply gradient descent with synthetic data to find parameters for simulation 
We are not using this file because the data is generated, hence we know the parameters already.

- `canadian_covid_map.py`: Canadian map 
- `generate_initial_data.py`: user interface for generating initial data 
- `get_simulation_data.py`: get simulation data using intiial data generated 
- `us_map.py`: draw US map based on generated geojson data 

## Acknowledgments
- Markov Mavericks contributing team members: Khac Nguyen Nguyen, Bao Nguyen, John He, Adhiguna Pande