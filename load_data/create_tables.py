import sqlite3

def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)


def create_rp_tables():
    q = '''CREATE TABLE IF NOT EXISTS rental_price (
        year INTEGER,
        location TEXT NOT NULL,
        DGUID text NOT NULL,
        TOS text NOT NULL,
        TOU text NOT NULL,
        price REAL);'''
    cursor.execute(q)
    connection.commit()

def create_csi_tables():
    q = '''CREATE TABLE IF NOT EXISTS csi (
        year INTEGER,
        location TEXT NOT NULL,
        DGUID text NOT NULL,
        cnt REAL);'''
    cursor.execute(q)
    connection.commit()
    
def create_population_tables():
    q = '''CREATE TABLE IF NOT EXISTS population (
        year INTEGER,
        location TEXT NOT NULL,
        DGUID text NOT NULL,
        cnt REAL);'''
    cursor.execute(q)
    connection.commit()

def create_er_tables():
    q = '''CREATE TABLE IF NOT EXISTS employment_rate (
        year INTEGER,
        location TEXT NOT NULL,
        val REAL);'''
    cursor.execute(q)
    connection.commit()

def create_area_tables():
    q = '''CREATE TABLE IF NOT EXISTS area (
        location TEXT NOT NULL,
        land_area REAL);'''
    cursor.execute(q)
    connection.commit()
    
if __name__ == '__main__':
    connect("database.db")
    create_rp_tables()
    create_csi_tables()
    create_population_tables()
    create_er_tables()
    create_area_tables()
