from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your actual Discogs API consumer key and secret
CONSUMER_KEY = 'frcYGScctkLNtFtkRMOA'
CONSUMER_SECRET = 'QFKIGJCbdlMhHDdGNOOtgaLEYVpTRBrh'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_links', methods=['POST'])
def fetch_links():
    data = request.get_json()
    barcodes = data.get('barcodes', [])
    links = []

    for barcode in barcodes:
        # Discogs API URL for searching by barcode
        url = f"https://api.discogs.com/database/search?barcode={barcode}&key={CONSUMER_KEY}&secret={CONSUMER_SECRET}"
        response = requests.get(url)
        
        if response.status_code == 200:
            results = response.json()
            if results.get('results'):
                # Extract the URI and cover image URL
                album_info = results['results'][0]
                album_link = f"https://www.discogs.com{album_info['uri']}"
                cover_image = album_info.get('cover_image', None)
                title = album_info.get('title', 'Unknown Title')
                artist = album_info.get('artist', 'Unknown Artist')
                links.append({'link': album_link, 'image': cover_image, 'title': title, 'artist': artist})
            else:
                links.append({'link': f"No results found for barcode: {barcode}", 'image': None, 'title': None, 'artist': None})
        else:
            links.append({'link': f"Error fetching data for barcode {barcode}: {response.status_code} {response.text}", 'image': None, 'title': None, 'artist': None})

    return jsonify({'links': links})

if __name__ == '__main__':
    app.run(debug=True)