
import os
import requests
import base64
from requests import post, get
import json
import sqlite3


CLIENT_ID = "eeee49cf4d3e434988195059e514534b"
CLIENT_SECRET = "2975c2b65cbb4f7e9ab02e378093f959"

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
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

