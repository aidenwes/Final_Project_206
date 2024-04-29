import requests
import sqlite3 
from datetime import datetime, timedelta
import json
import time

# Define the base URL for the NASA APOD API
base_url = 'https://api.nasa.gov/planetary/apod'

# Define your NASA API key
api_key = "J6J1q12I6Opn5qdtk1XqPkqa84t0jqHk8b06fxGy"

def get_pictures():
    start_date = datetime(2024, 1, 1)
    end_date = datetime.today()
    current_date = start_date
    pictures = {}
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        params = {
            'api_key': api_key,
            'date': date_str
        }
        response = requests.get(base_url, params=params)
        print(response)
        time.sleep(1)
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                pictures[date_str] = data['url']
            else:
                print(f"No image URL found for date: {date_str}")
        else:
            print(f"Failed to fetch image for date: {date_str}. Status code: {response.status_code}")
        current_date += timedelta(days=1)
    return pictures

def add_position_to_json(pictures):
    for i, (date, url) in enumerate(pictures.items()):
        pictures[date] = {'date': date, 'url': url, 'position': i + 1}
    return pictures

def set_up_date_table():
    conn = sqlite3.connect("nasa.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS nasa_pictures (position INTEGER, date TEXT, url TEXT)")
    conn.commit()
    conn.close()

def insert_pictures_25(conn, cursor):
    data_pictures = add_position_to_json(get_pictures())
    length_pictures = cursor.execute(f"SELECT COUNT(*) FROM nasa_pictures").fetchone()[0]
    current_year = datetime.now().year
    
    # Calculate the number of days that have passed in the current year
    today = datetime.now()
    start_of_year = datetime(today.year, 1, 1)
    days_passed = (today - start_of_year).days

    for i in range(25):
        if length_pictures != days_passed:
            for picture in data_pictures.values():
                if picture['position'] not in [x[0] for x in cursor.execute("SELECT position FROM nasa_pictures").fetchall()]:
                    date = picture["date"]
                    url = picture["url"]
                    position = picture["position"]
                    cursor.execute(f"INSERT INTO nasa_pictures (position, date, url) VALUES (?, ?, ?)", (position ,date, url))
                    conn.commit()
                    break

def main():
    conn = sqlite3.connect("nasa.db")
    cursor = conn.cursor()
    set_up_date_table()
    insert_pictures_25(conn, cursor)
    conn.close()

if __name__ == "__main__":
    main()