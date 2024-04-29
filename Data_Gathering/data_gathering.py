import sqlite3

def count_song_releases():
    # Connect to the SQLite database
    conn = sqlite3.connect("spotify.db")
    cursor = conn.cursor()

    # Execute the SQL query to count song releases based on picture of the day date
    query = """
    SELECT np.date, COUNT(*) AS song_count
    FROM nasa_pictures np
    LEFT JOIN billboard_100 bb ON np.date = bb.release_date
    LEFT JOIN daily_chart dc ON np.date = dc.release_date
    GROUP BY np.date
    ORDER BY song_count DESC;
    """
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    return results

def main():
    # Get the counts of song releases
    song_counts = count_song_releases()

    # Display the results
    for date, count in song_counts:
        print(f"Date: {date}, Song Count: {count}")

if __name__ == "__main__":
    main()