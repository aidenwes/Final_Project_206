from dotenv import load_dotenv
import os
import requests
import base64
from requests import post, get
import json
import sqlite3

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_billboard_100(token):
    url = "https://api.spotify.com/v1/playlists/6UeSakyzhiEt4NB3UAd6NQ"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

def get_daily_chart(token):
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

def add_position_to_json(json):
    for i in range(len(json["tracks"]["items"])):
        json["tracks"]["items"][i]["position"] = i + 1
    return json

# # #create billboaard table with id, song_name, artist, album, release_date, and popularity
# def setup_billboard_table():
#     conn = sqlite3.connect("spotify.db")
#     cursor = conn.cursor()
#     cursor.execute("CREATE TABLE IF NOT EXISTS billboard_100 (id INTEGER, song_name TEXT, artist TEXT, album TEXT, release_date TEXT, popularity INTEGER)")
#     conn.commit()
#     conn.close()

# def insert_data(conn, cursor, table):
#     conn = sqlite3.connect("spotify.db")
#     cursor = conn.cursor()
#     length_table = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
#     print(length_table)
#     conn.commit()
#     conn.close()

def setup_billboard_table():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS billboard_100 (id INTEGER, song_name TEXT, artist TEXT, album TEXT, release_date TEXT, popularity INTEGER)")
    conn.commit()
    conn.close()

def setup_daily_chart_table():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS daily_chart (id INTEGER, song_name TEXT, artist TEXT, album TEXT, release_date TEXT, popularity INTEGER)")
    conn.commit()
    conn.close()

# def insert_data(conn, cursor, table):
#     length_table = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
#     #insert a song into the table
#     data = add_position_to_json(get_billboard_100(get_token()))
#     for i in range(len(data["tracks"]["items"])):
#         song = data["tracks"]["items"][i]["track"]
#         song_id = data["tracks"]["items"][i]["position"]
#         print(song_id)
#         song_name = song["name"]
#         artist = song["artists"][0]["name"]
#         album = song["album"]["name"]
#         release_date = song["album"]["release_date"]
#         popularity = song["popularity"]
#         cursor.execute(f"INSERT INTO {table} (id, song_name, artist, album, release_date, popularity) VALUES (?, ?, ?, ?, ?, ?)", (song_id, song_name, artist, album, release_date, popularity))
#         conn.commit()

def insert_25_tracks(conn, cursor):
    length_BB = cursor.execute(f"SELECT COUNT(*) FROM billboard_100").fetchone()[0]
    data_BB = add_position_to_json(get_billboard_100(get_token()))
    length_DC = cursor.execute(f"SELECT COUNT(*) FROM daily_chart").fetchone()[0]
    data_DC = add_position_to_json(get_daily_chart(get_token()))
    for i in range(25):
        if length_BB != 100:
            for song in data_BB["tracks"]["items"]:
                if song['position'] not in [x[0] for x in cursor.execute(f"SELECT id FROM billboard_100").fetchall()]:
                    song_id = song["position"]
                    song_name = song["track"]["name"]
                    artist = song["track"]["artists"][0]["name"]
                    album = song["track"]["album"]["name"]
                    release_date = song["track"]["album"]["release_date"]
                    popularity = song["track"]["popularity"]
                    cursor.execute(f"INSERT INTO billboard_100 (id, song_name, artist, album, release_date, popularity) VALUES (?, ?, ?, ?, ?, ?)", (song_id, song_name, artist, album, release_date, popularity))
                    conn.commit()
                    break
        elif length_DC != 50 and length_BB == 100:
            for song in data_DC["tracks"]["items"]:
                if song['position'] not in [x[0] for x in cursor.execute(f"SELECT id FROM daily_chart").fetchall()]:
                    song_id = song["position"]
                    song_name = song["track"]["name"]
                    artist = song["track"]["artists"][0]["name"]
                    album = song["track"]["album"]["name"]
                    release_date = song["track"]["album"]["release_date"]
                    popularity = song["track"]["popularity"]
                    cursor.execute(f"INSERT INTO daily_chart (id, song_name, artist, album, release_date, popularity) VALUES (?, ?, ?, ?, ?, ?)", (song_id, song_name, artist, album, release_date, popularity))
                    conn.commit()
                    break


def main():
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()
    setup_billboard_table()
    setup_daily_chart_table()
    insert_25_tracks(conn, cursor)

if __name__ == "__main__":
    main()



# def setup_daily_chart_table():
#     conn = sqlite3.connect("spotify.db")
#     cursor = conn.cursor()
#     cursor.execute("CREATE TABLE IF NOT EXISTS daily_chart (id INTEGER, song_name TEXT, artist TEXT, album TEXT, release_date TEXT, popularity INTEGER)")
#     conn.commit()
#     conn.close()

# def insert_database(conn, cursor, table, data):
