# import sqlite3

# def setup_combined_data_table(conn, cursor):
#     conn = sqlite3.connect("combined.db")
#     conn.execute("CREATE TABLE IF NOT EXISTS combined_data (date TEXT, url TEXT, position INTEGER, title TEXT, artist TEXT, release_date TEXT, rank INTEGER, streams INTEGER)")

# # def select_all(conn, cursor):
# #     conn2 = sqlite3.connect("spotify.db")
# #     # conn.cursor.execute("CREATE TABLE combined_data AS \
# #     #                 SELECT * FROM nasa_pictures \
# #     #                 JOIN billboard_100 ON nasa_pictures.date = billboard_100.release_date \
# #     #                 JOIN daily_50 ON nasa_pictures.date = daily_50.release_date;")
# #     cursor.execute("CREATE TABLE combined_data AS \
# #                     SELECT * FROM nasa_pictures;")
# #     # cursor.execute("SELECT * FROM billboard_100")
# #     # cursor.execute("SELECT * FROM daily_50")
# #     return cursor.fetchall()

# def main():
#     conn = sqlite3.connect("nasa.db")
#     cursor = conn.cursor()
#     select_all(conn, cursor)
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     main()

# # import sqlite3

# # def select_all(conn, cursor):
# #     # Connect to the second database (spotify.db)
# #     conn_spotify = sqlite3.connect("spotify.db")
# #     cursor_spotify = conn_spotify.cursor()

# #     # Perform the JOIN operation between tables from nasa.db and spotify.db

    
# #     cursor_spotify.execute("""
# #         CREATE TABLE combined_data AS
# #         SELECT *
# #         FROM nasa_pictures
# #         JOIN billboard_100 ON nasa_pictures.date = billboard_100.release_date
# #         JOIN daily_chart ON nasa_pictures.date = daily_chart.release_date
# #     """)

# #     # Close the connection to spotify.db
# #     conn_spotify.close()

# # def main():
# #     # Connect to the first database (nasa.db)
# #     conn = sqlite3.connect("nasa.db")
# #     cursor = conn.cursor()

# #     # Call the select_all function to perform the operations
# #     select_all(conn, cursor)

# #     # Commit changes and close the connection to nasa.db
# #     conn.commit()
# #     conn.close()

# # if __name__ == "__main__":
# #     main()

# import sqlite3

# def create_combined_database():
#     # Connect to the existing databases
#     nasa_conn = sqlite3.connect("nasa.db")
#     spotify_conn = sqlite3.connect("spotify.db")

#     # Retrieve data from nasa.db
#     nasa_cursor = nasa_conn.cursor()
#     nasa_cursor.execute("SELECT date FROM nasa_pictures")
#     nasa_data = nasa_cursor.fetchall()

#     # Retrieve release dates from spotify.db (billboard_100 and daily_50)
#     spotify_cursor = spotify_conn.cursor()
#     spotify_cursor.execute("SELECT release_date FROM billboard_100")
#     billboard_release_dates = spotify_cursor.fetchall()
#     spotify_cursor.execute("SELECT release_date FROM daily_chart")
#     daily_50_release_dates = spotify_cursor.fetchall()

#     # Create a new SQLite database
#     combined_conn = sqlite3.connect("combined.db")
#     combined_cursor = combined_conn.cursor()

#     # Create tables in the new database
#     combined_cursor.execute("CREATE TABLE IF NOT EXISTS billboard_100_dates (date TEXT)")
#     combined_cursor.execute("CREATE TABLE IF NOT EXISTS daily_50_dates (date TEXT)")

#     # Insert data into tables
#     combined_cursor.executemany("INSERT INTO billboard_100_dates VALUES (?)", billboard_release_dates)
#     combined_cursor.executemany("INSERT INTO daily_50_dates VALUES (?)", daily_50_release_dates)

#     # Commit changes and close connections
#     combined_conn.commit()
#     combined_conn.close()
#     nasa_conn.close()
#     spotify_conn.close()

# def main():
#     create_combined_database()

# if __name__ == "__main__":
#     main()

import sqlite3
from collections import Counter

def calculate_top_ten_recurring_dates():
    # Connect to the existing databases
    combined_conn = sqlite3.connect("combined.db")
    nasa_conn = sqlite3.connect("nasa.db")
    spotify_conn = sqlite3.connect("spotify.db")

    # Create a cursor for each database
    combined_cursor = combined_conn.cursor()
    nasa_cursor = nasa_conn.cursor()
    spotify_cursor = spotify_conn.cursor()

    # Create tables for top ten recurring dates for billboard_100 and daily_50
    combined_cursor.execute("CREATE TABLE IF NOT EXISTS top_ten_billboard_dates (release_date TEXT, occurrences INTEGER)")
    combined_cursor.execute("CREATE TABLE IF NOT EXISTS top_ten_daily_50_dates (release_date TEXT, occurrences INTEGER)")

    # Retrieve data from nasa.db for dates in 2024
    nasa_cursor.execute("SELECT date FROM nasa_pictures WHERE date LIKE '2024-%'")
    nasa_dates = nasa_cursor.fetchall()

    # Retrieve release dates from spotify.db (billboard_100 and daily_50) for dates in 2024
    spotify_cursor.execute("SELECT release_date FROM billboard_100 WHERE release_date LIKE '2024-%'")
    billboard_dates = spotify_cursor.fetchall()
    spotify_cursor.execute("SELECT release_date FROM daily_chart WHERE release_date LIKE '2024-%'")
    daily_50_dates = spotify_cursor.fetchall()

    # Calculate the top ten recurring dates for billboard_100 in 2024
    billboard_counter = Counter([date[0] for date in billboard_dates])
    top_ten_billboard = billboard_counter.most_common(10)

    # Calculate the top ten recurring dates for daily_50 in 2024
    daily_50_counter = Counter([date[0] for date in daily_50_dates])
    top_ten_daily_50 = daily_50_counter.most_common(10)

    # Insert top ten recurring dates for billboard_100 into the table
    combined_cursor.executemany("INSERT INTO top_ten_billboard_dates VALUES (?, ?)", top_ten_billboard)

    # Insert top ten recurring dates for daily_50 into the table
    combined_cursor.executemany("INSERT INTO top_ten_daily_50_dates VALUES (?, ?)", top_ten_daily_50)

    # Commit changes and close connections
    combined_conn.commit()
    combined_conn.close()
    nasa_conn.close()
    spotify_conn.close()

def add_nasa_pictures_to_combined():
    # Connect to the databases
    nasa_conn = sqlite3.connect("nasa.db")
    combined_conn = sqlite3.connect("combined.db")

    # Create cursors for each database
    nasa_cursor = nasa_conn.cursor()
    combined_cursor = combined_conn.cursor()

    # Retrieve data from nasa_pictures in nasa.db
    nasa_cursor.execute("SELECT * FROM nasa_pictures")
    rows = nasa_cursor.fetchall()

    # Create nasa_pictures table in combined.db if not exists
    combined_cursor.execute("CREATE TABLE IF NOT EXISTS nasa_pictures (position INTEGER, date TEXT, url TEXT)")

    # CREATE TABLE table_name (
    #     column1 datatype,
    #     column2 datatype,
    #     column3 datatype,
    # ....
    # );

    # Insert data into nasa_pictures table in combined.db
    combined_cursor.executemany("INSERT INTO nasa_pictures VALUES (?, ?, ?)", rows)


    # Commit changes and close connections
    combined_conn.commit()
    nasa_conn.close()
    combined_conn.close()


def join_tables_BB():
    conn = sqlite3.connect("combined.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS joined_billboard (date TEXT, occurrences INTEGER, url TEXT)")

    cursor.execute("""SELECT top_ten_billboard_dates.release_date, top_ten_billboard_dates.occurrences, url
                   FROM top_ten_billboard_dates
                   JOIN nasa_pictures
                   ON nasa_pictures.date = top_ten_billboard_dates.release_date"""
                     )
    
    joined = cursor.fetchall()

    # Create nasa_pictures table in combined.db if not exists
    

    cursor.executemany("INSERT INTO joined_billboard VALUES (?, ?, ?)", joined)


    conn.commit()
    conn.close()

def join_tables_DC():
    conn = sqlite3.connect("combined.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS daily_50_joined (date TEXT, occurrences INTEGER, url TEXT)")

    cursor.execute("""SELECT top_ten_daily_50_dates.release_date, top_ten_daily_50_dates.occurrences, url
                   FROM top_ten_daily_50_dates
                   JOIN nasa_pictures
                   ON nasa_pictures.date = top_ten_daily_50_dates.release_date"""
                     )
    
    joined = cursor.fetchall()

    # Create nasa_pictures table in combined.db if not exists
    

    cursor.executemany("INSERT INTO daily_50_joined VALUES (?, ?, ?)", joined)

    conn.commit()
    conn.close()


def main():
    calculate_top_ten_recurring_dates()
    add_nasa_pictures_to_combined()
    join_tables_BB()
    join_tables_DC()

if __name__ == "__main__":
    main()