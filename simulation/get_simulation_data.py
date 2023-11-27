import geopy
import json
import math
import random
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD


# get simulation data using intiial data generated
class Simulation:
    def __init__(self):
        # a, b, c are the coefficients for the functions f,g and h
        self.a1 = 8.38253314e-04
        self.a2 = 3.83305840e-02
        self.a3 = 2.47086759e+01
        self.b1 = 500
        self.b2 = 0.75
        self.c1 = 0.00304379
        self.c2 = 0.99879705
        self.c3 = 0.00779231
        #self.initial_states = initial_states 
        #self.city_list = city_list
        
    def load_initial_data(self, json_path):
        #get initial csi, population density, employment rate of the needed city
        f = open(json_path)
        #Store initial data in a dictionary self.data
        self.data = json.load(f)

    
    def get_initial_state(self):
        self.initial_state = {}
        #get 0,-1, or 1 for each cities
        for city in self.data.keys():
            self.initial_state[city] = self.get_initial_state_city(self.data[city])

        #print(self.initial_state)
            
        #pass

    def get_initial_state_city(self, parameter):
        #calculate values of functions f,g and h
        g = self.a1 * parameter['population'] + self.a2 * parameter['csi'] + self.a3
        h = self.b1*(1/(1 + math.exp(-self.b2 * parameter['employment'])) - 1/2)
        f = self.c1*g + self.c2*h + self.c3
        #return intial state of city depending on value of f
        if f > 150:
            return 1
        elif f > 50:
            return 0
        else:
            return -1

        
    def get_city_coordinates(self):
        #Create dictionary to store location of each city
        self.coordinates = {}
        geolocator = Nominatim(user_agent="MyApp")
        for city in self.data.keys():
            location = geolocator.geocode(city[:-10])
            self.coordinates[city] = [location.latitude,location.longitude]

    
    def get_city_distance(self):
        self.distance_dict = {}
        for city in self.data.keys():
            self.distance_dict[city] = dict()
            for neighbor in self.data.keys():
                if neighbor == city :
                    continue
                distance = GD(self.coordinates[city], self.coordinates[neighbor]).km
                dist_weight = 1/(0.002*distance - 1) + 2
                self.distance_dict[city][neighbor] = dist_weight
    def get_city_state(self, city, year):
        dist_list = []
        #get current city states
        for neighbor in self.data.keys():
            if neighbor == city :
                continue
            dist_list.append([self.distance_dict[city][neighbor], self.simulation_data[year-1][neighbor]])

        if self.simulation_data[year - 1][city] == 1:
            #rate of change from state 1 to state 0
            prob = 1/sum([x[0] for x in dist_list]) * sum([min(1-x[1], 1) * x[0] for x in dist_list])
            if prob < np.random.uniform() :
                return 1
            else:
                return 0
        elif self.simulation_data[year-1][city] == -1:
            #rate of change from state -1 to state 0
            prob = 1/sum([x[0] for x in dist_list]) * sum([min(1+x[1], 1) * x[0] for x in dist_list])
            if prob < np.random.uniform() :
                return -1
            else:
                return 0
        else:
            #if current state is 0, we can go to any state k from state 0
            sum1 = 0
            summ1 = 0
            sum_all = 0
            for x in dist_list:
                sum_all += x[0]
                if x[1] == 1:
                    sum1 += x[0]
                elif x[1] == -1:
                    summ1 += x[0]
            rates1 = sum1/sum_all
            ratesm1 = summ1/sum_all
            if rates1 + ratesm1 >= 1:
                print("----------")
            random = np.random.uniform()
            if random < rates1:
                return 1
            elif random < rates1 + ratesm1:
                return -1
            else: 
                return 0
                

    def run(self):
        #return a list of year containing cities and the states
        self.simulation_data = {}
        self.simulation_data[2015] = self.initial_state
        for year in range(2016, 2100):
            self.simulation_data[year] = dict()
            for city in self.data.keys():
                self.simulation_data[year][city] = self.get_city_state(city, year)
        with open('us_states_by_year.json', 'w') as fp:
            json.dump(self.simulation_data, fp)

                    
            

def main():
    simulation = Simulation()
    #f = open('data.json')
    simulation.load_initial_data("us_state_initial_data.json")
    simulation.get_initial_state()
    simulation.get_city_coordinates()
    simulation.get_city_distance()
    simulation.run()


main()
