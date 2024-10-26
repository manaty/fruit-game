import os
import requests
import pandas as pd
from PIL import Image
from io import BytesIO


# Replace with your actual Bing Image Search API key
API_KEY =  os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID =os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Directory to save images
IMAGE_DIR = './friend_images'

# Ensure the image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_existing_image_count(fruit_name):
    """Returns the number of existing images for a given fruit."""
    base_name = os.path.join(IMAGE_DIR, fruit_name)
    count = 0
    if os.path.isfile(f"{base_name}.png"):
        return 1
    while os.path.isfile(f"{base_name}_{count+1}.png"):
        count += 1
    return count

def search_and_download_image(fruit_name, image_index):
    """Searches for an image and downloads it."""
    search_url = 'https://customsearch.googleapis.com/customsearch/v1'
    params = {
        'q':  f"{fruit_name} fruit",
        'cx': SEARCH_ENGINE_ID,
        'key': API_KEY,
        'searchType': 'image',
        'fileType': 'png,jpg',
        'imgType': 'photo',
        'num': 10,
        'safe': 'off',
        'rights': 'cc_publicdomain',
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Handle case where there are fewer results than desired index
    items = search_results.get('items', [])
    if len(items) <= image_index:
        print(f"Not enough images found for {fruit_name}. Skipping.")
        return

    image_url = items[image_index]['link']
    try:
        headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
        image_response = requests.get(image_url,headers=headers, timeout=10)
        image_response.raise_for_status()
        image = Image.open(BytesIO(image_response.content)).convert('RGB')
        save_image(fruit_name, image)
    except Exception as e:
        print(f"Failed to download image for {fruit_name}: {e}")

def save_image(fruit_name, image):
    """Saves the image to the specified directory with the correct naming."""
    fruit_name_clean = fruit_name.replace(" ", "")
    base_name = os.path.join(IMAGE_DIR, fruit_name_clean)
    if not os.path.isfile(f"{base_name}.png"):
        image.save(f"{base_name}.png")
        print(f"Saved image as {base_name}.png")
    else:
        count = get_existing_image_count(fruit_name_clean)
        image.save(f"{base_name}_{count+1}.png")
        print(f"Saved image as {base_name}_{count+1}.png")

def main():
    # Read the CSV file
    df = pd.read_csv('../1_content/3_Friends.csv')
    fruit_friends = df[['Fruit Friend 1', 'Fruit Friend 2', 'Fruit Friend 3']].values.flatten()
    fruit_friends = [str(fruit).strip() for fruit in fruit_friends if pd.notnull(fruit)]

    for fruit_name in fruit_friends:
        fruit_name_clean = fruit_name.replace(" ", "")
        base_name = os.path.join(IMAGE_DIR, fruit_name_clean)

        # Check if the main image exists
        if os.path.isfile(f"{base_name}.png"):
            print(f"Image for {fruit_name} already exists. Skipping.")
            continue

        # Check for existing numbered images
        image_count = get_existing_image_count(fruit_name_clean)
        image_index = image_count  # Zero-based index for search results

        print(f"Downloading image {image_index + 1} for {fruit_name}")
        search_and_download_image(fruit_name, image_index)

if __name__ == "__main__":
    main()