import requests
from datetime import datetime, timedelta

# Define the base URL for the NASA APOD API
base_url = 'https://api.nasa.gov/planetary/apod'

# Define your NASA API key
api_key = "J6J1q12I6Opn5qdtk1XqPkqa84t0jqHk8b06fxGy"

# Specify the start date (January 1st of the desired year)
start_date = datetime(2024, 1, 1)

# Get today's date
end_date = datetime.today()

# Iterate through dates from start_date to end_date
current_date = start_date
while current_date <= end_date:
    # Format the current date as YYYY-MM-DD
    date_str = current_date.strftime('%Y-%m-%d')

    # Construct the API request URL for the current date
    request_url = f"{base_url}?date={date_str}&api_key={api_key}"

    # Make the API request
    response = requests.get(request_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        apod_data = response.json()
        
        # Extract and print relevant information (e.g., title, explanation)
        print(f"Date: {date_str}")
        print(f"Title: {apod_data['title']}")
        print(f"Explanation: {apod_data['explanation']}")
        print(f"URL: {apod_data['url']}")
        print()
    else:
        print(f"Failed to retrieve APOD for date: {date_str}")

    # Move to the next date
    current_date += timedelta(days=1)