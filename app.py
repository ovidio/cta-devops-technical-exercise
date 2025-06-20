from flask import Flask
import requests
import os
app = Flask(__name__)

# Takes in API key from github secrets
API_KEY = os.environ['GIPHY_API_KEY']
GIPHY_API_URL = "https://api.giphy.com/v1/gifs/random"

@app.route('/')
def hello_cat():
    gif_url = get_random_gif()
    html_content = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Display GIF</title>
            </head>
            <body>
                <h1>Here is your cat GIF:</h1>
                <img src="image_url" alt="Image from external source">
                <br>
                <button onClick="window.location.reload();">Refresh Page</button>
            </body>
            </html>"""
    html_content = html_content.replace("image_url", gif_url)
    return html_content

def get_random_gif():
    """Fetches a random GIF URL from Giphy API."""
    params = {
        "api_key": API_KEY,
        "tag": "cat",  # You can specify a tag like 'funny', 'cat', etc. Leave empty for random GIFs.
        "rating": "G",  # You can change rating (e.g., G, PG, PG-13, R)
    }
    response = requests.get(GIPHY_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        gif_url = data['data']['images']['original']['url']
        return gif_url
    else:
        print(f"Error: Unable to fetch GIF. Status code {response.status_code}")
        return None


if __name__ == "__main__":
    app.run(debug=True)