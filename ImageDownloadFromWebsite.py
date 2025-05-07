
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Import urljoin to handle relative URLs

# URL of the page with images
url = 'https://www.metmuseum.org/art/collection/search/38025'  # Replace with the actual URL of the page

# Set up a session
session = requests.Session()

# Get the webpage content
response = session.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags
images = soup.find_all('img')

# Create a folder to save images
folder_name = 'downloaded_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Loop through all images and download them
for img in images:
    img_url = img.get('src')
    if img_url:
        # Use urljoin to handle relative URLs and create the full URL
        full_img_url = urljoin(url, img_url)

        try:
            # Get the image content
            img_data = requests.get(full_img_url).content
            # Get the image filename
            img_name = os.path.join(folder_name, full_img_url.split('/')[-1])
            # Write the image to the folder
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded {img_name}")
        except Exception as e:
            print(f"Failed to download {full_img_url}: {e}")
