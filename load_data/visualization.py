import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import get_test_data

from matplotlib.widgets import Button, Slider
def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)


def create_common_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS common_location AS 
        SELECT DISTINCT location from rental_price
        INTERSECT
        SELECT DISTINCT location from csi
        INTERSECT
        SELECT DISTINCT location from population
        INTERSECT
        SELECT DISTINCT location from area
        INTERSECT 
        SELECT DISTINCT location from employment_rate
    ;''')
    cursor.execute('''
        DELETE FROM common_location WHERE location in ("Chilliwack, British Columbia")
    ''')
    connection.commit()
def check_year_rp():
    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM rental_price
        WHERE location in common_location
        GROUP BY location)
        SELECT location, mi
        FROM temp_table
        ORDER BY mi DESC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)

    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM rental_price
        WHERE location in common_location
        GROUP BY location)
        SELECT location, ma
        FROM temp_table
        ORDER BY ma ASC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)

def calculate_rental_price(mi, ma):
    cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS avg_rp  AS 
        
            SELECT location, year, DGUID, AVG(price) AS "avg_price" FROM rental_price
            WHERE location in common_location
            AND TOU = "One bedroom units"
            AND year >= (?)
            AND year <= (?)
            GROUP BY location, year
    ;''', (mi, ma))
    connection.commit()

def calculate_rental_price_diff(mi, ma):
    cursor.execute(
    '''    
        CREATE TABLE IF NOT EXISTS rp_diff AS
            SELECT t1.location, t1.year, t1.DGUID, t2.avg_price - t1.avg_price  AS "price_diff"
            FROM avg_rp t1, avg_rp t2
            WHERE t1.location = t2.location
            AND t1.year = t2.year - 1
    ;''')
    connection.commit()
def check_year_csi():
    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM csi
        WHERE location in common_location
        GROUP BY location)
        SELECT location, mi
        FROM temp_table
        ORDER BY mi DESC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)

    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM csi
        WHERE location in common_location
        GROUP BY location)
        SELECT location, ma
        FROM temp_table
        ORDER BY ma ASC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)
def calculate_csi(mi, ma):
    cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS csi_common_loc AS 
            SELECT * FROM csi
            WHERE location in common_location
            AND year >= (?)
            AND year <= (?)
        
    ;''', (mi,ma)
    )
    connection.commit()

def check_year_p():
    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM population
        WHERE location in common_location
        GROUP BY location)
        SELECT location, mi
        FROM temp_table
        ORDER BY mi DESC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)

    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM population
        WHERE location in common_location
        GROUP BY location)
        SELECT location, ma
        FROM temp_table
        ORDER BY ma ASC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)
def calculate_population(mi, ma):
    cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS p_common_loc AS 
            SELECT * FROM population
            WHERE location in common_location
            AND year >= (?)
            AND year <= (?)
        
    ;''', (mi,ma)
    )
    connection.commit()

def check_year_employment_rate():
    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM employment_rate
        WHERE location in common_location
        GROUP BY location)
        SELECT location, mi
        FROM temp_table
        ORDER BY mi DESC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)

    cursor.execute(
    '''
        with temp_table (mi,ma, location) as (
        SELECT MIN(year), MAX(year), location FROM employment_rate
        WHERE location in common_location
        GROUP BY location)
        SELECT location, ma
        FROM temp_table
        ORDER BY ma ASC
    ;'''
    )
    rows = cursor.fetchall()
    print(rows)
def calculate_employment_rate(mi, ma):
    cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS er_common_loc AS 
            SELECT * FROM employment_rate
            WHERE location in common_location
            AND year >= (?)
            AND year <= (?)
    ;''', (mi, ma)
    )
    connection.commit()
def calculate_employment_rate_diff():
    cursor.execute(
    '''    
        CREATE TABLE IF NOT EXISTS er_diff AS
            SELECT t1.location, t1.year, t2.val - t1.val  AS "val_diff"
            FROM er_common_loc t1, er_common_loc t2
            WHERE t1.location = t2.location
            AND t1.year = t2.year - 1
    ;''')
    connection.commit()

def calculate_population_density():
    cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS pd AS
            SELECT p_common_loc.location, p_common_loc.year, p_common_loc.cnt/area.land_area AS "population_density"
            FROM p_common_loc, area
            WHERE p_common_loc.location = area.location;
    ''')
    connection.commit()


def get_final_data():
    # cnt is csi
    # val_diff is employment_rate change in next year
    cursor.execute( 
    '''
        CREATE TABLE IF NOT EXISTS final_data_diff AS
        SELECT rp_diff.location, rp_diff.year, price_diff, cnt, population_density, val_diff, rp_diff.DGUID
        FROM rp_diff
        LEFT JOIN csi_common_loc
        ON rp_diff.location = csi_common_loc.location AND rp_diff.year = csi_common_loc.year
        LEFT JOIN pd
        ON rp_diff.location = pd.location AND rp_diff.year = pd.year
        LEFT JOIN er_diff
        ON rp_diff.location = er_diff.location AND rp_diff.year = er_diff.year
    ;''')
    connection.commit()

def get_data_year(year):
    cursor.execute('''
        SELECT location, price_diff, cnt, population_density, val_diff FROM final_data_diff
        WHERE year = (?)
    ;''', (year,))
    return cursor.fetchall()
    
class ChangingPlot(object):
    def __init__(self, min_year, max_year):
        axes_list = []
        for item in ["rental_price", "homicide_rates", "population"]:
            for item2 in ["rental_price", "homicide_rates", "population"]:
                axes_list.append([item, item2])

        self.inc = 1
        self.fig, self.plot_list = plt.subplots(3,1)
        self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03])

        self.slider = Slider(self.sliderax, 'Year', min_year, max_year, valinit= 2006)
        self.slider.on_changed(self.update)
        self.slider.drawon = False
        initial_year = 2006
        self.get_common_location()

        self.get_data(initial_year)
        print(self.data_dict)
        x = np.arange(min_year, max_year, self.inc)
        limit = [[-200,200], [0,250], [0,10000], [-10,10]]
        self.dot_list = []
        for i in range(3):
            tmp_dict = {}
            for loc in self.common_location:
                self.dot, = self.plot_list[i].plot(self.data_dict[loc][i+1], self.data_dict[loc][0], 'bo')
                tmp_dict[loc] = self.dot
                self.plot_list[i].set_ylim(limit[0])
                self.plot_list[i].set_xlim(limit[i+1])
            self.dot_list.append(tmp_dict)
    
    def update(self, value):
        if value == int(value / self.inc) * self.inc:
            return
        value = int(value / self.inc) * self.inc
        self.get_data(value)
        for i in range(3):
            for loc in self.common_location:
                print(self.dot_list[i][loc])
                self.dot_list[i][loc].set_data(self.data_dict[loc][i+1], self.data_dict[loc][0])
        self.slider.valtext.set_text('{}'.format(value))
        self.fig.canvas.draw()

    def show(self):
        plt.show()
    def get_common_location(self):
        cursor.execute(
            '''
                SELECT * FROM common_location;
            '''
        )
        self.common_location = [x[0] for x in cursor.fetchall()]
    def get_data(self, year):
        data = get_data_year(year)
        self.data_dict = {}
        for rows in data:
            self.data_dict[rows[0]] = [rows[1], rows[2], rows[3], rows[4]]

class ChangingPlot3D(object):
    def __init__(self, min_year, max_year):
        # Twice as wide as it is tall.
        self.fig = plt.figure()
        self.inc = 1
        self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03])

        self.slider = Slider(self.sliderax, 'Year', min_year, max_year, valinit= 2006)
        self.slider.on_changed(self.update)
        self.slider.drawon = False
        initial_year = 2006
        self.get_common_location()
        self.get_data(initial_year)
        #---- First subplot
        self.plot_list = []
        limit = [[-150,150], [50,200], [0,4000], [-5,5]]
        label = ["Rental price", "CSI", "population density", "employment rate change"]
        self.dot_list = []

        for i in range (3):
            self.plot_list.append(self.fig.add_subplot(1, 3, i+1, projection='3d'))

            lst = [1,2,3]
            del lst[i]
            tmp_dict = {}
            for loc in self.common_location:
                tmp_dict[loc] = self.plot_list[i].plot(self.data_dict[loc][lst[0]], self.data_dict[loc][lst[1]], self.data_dict[loc][0], 'bo')[0]
                self.plot_list[i].set_zlim(limit[0])
                self.plot_list[i].set_xlim(limit[lst[0]])
                self.plot_list[i].set_ylim(limit[lst[1]])
                self.plot_list[i].set(xlabel=label[lst[0]], ylabel=label[lst[1]], zlabel = label[0])
            self.dot_list.append(tmp_dict)




        

    def update(self, value):
        if value == int(value / self.inc) * self.inc:
            return
        value = int(value / self.inc) * self.inc
        self.get_data(value)
        for i in range(3):
            lst = [1,2,3]
            del lst[i]
            for loc in self.common_location:
                self.dot_list[i][loc].set_data_3d([[self.data_dict[loc][lst[0]]], [self.data_dict[loc][lst[1]]], [self.data_dict[loc][0]]])
        self.slider.valtext.set_text('{}'.format(value))
        self.fig.canvas.draw()

    def show(self):
        plt.show()
    def get_common_location(self):
        cursor.execute(
            '''
                SELECT * FROM common_location;
            '''
        )
        self.common_location = [x[0] for x in cursor.fetchall()]
    def get_data(self, year):
        data = get_data_year(year)
        self.data_dict = {}
        for rows in data:
            self.data_dict[rows[0]] = [rows[1], rows[2], rows[3], rows[4]]

if __name__ == '__main__':
    connect('database.db')
    # consider only city that appear in all 4 tables
    
    
    create_common_tables()    

    # check_year_rp()   
    # all common location in rental price data is between 1987 and 2022 

    # check_year_csi()  
    # all common location in csi data is between 2001 and 2022 

    # check_year_p()    
    # all common location in population data is between 2001 and 2022

    # check_year_employment_rate()
    # all common location in employment rate data is between 2006 and 2022

    # Thus we set min and max year to the followings
    min_year = 2006
    max_year = 2022
    
    # get the average over one area (city)
    calculate_rental_price(min_year, max_year)

    # calculate the difference in a year
    calculate_rental_price_diff(min_year, max_year)

    # apply the year 
    calculate_csi(min_year, max_year)

    calculate_population(min_year, max_year)
    
    calculate_employment_rate(min_year, max_year)
    calculate_employment_rate_diff()

    calculate_population_density()
    
    
    get_final_data()

    
    # p = ChangingPlot(min_year, max_year)
    # p.show()
    # p2 = ChangingPlot3D(min_year, max_year)
    # p2.show()
    

    
    

   




