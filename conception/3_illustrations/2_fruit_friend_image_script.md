I already have pictures of the main fruits, but please create a python script that read the csv file and for each fruit friend use google to find an image of the fruit. download it, convert it to png and copy it in a ./friend_images directory the name of the image is the name of the fruit (no lowercased) and the ".png" extension : <fruitName>.png
if such a file <fruitName>.png already exist we skip to the next fruit friend.
If in the ./friend_images directory  there is a file <fruitName>_1.png present it means that we need to select the second image returned by google, if there is a file <fruitName>_2.png it means we must select the third image, etc




chatGPT model o1-preview anwser:

Here is a Python script that reads the CSV file and downloads images for each fruit friend using the Bing Image Search API. The script saves the images as PNG files in the `./friend_images` directory, following your specified naming conventions.

**Note:** You'll need to obtain an API key for the Bing Image Search API from [Microsoft Azure](https://azure.microsoft.com/en-us/services/cognitive-services/bing-image-search-api/) to run this script.

---

### **Steps to Set Up the Script**

1. **Install Required Libraries:**

   You'll need to install the following Python libraries if they aren't already installed:

   ```bash
   pip install requests pillow pandas
   ```

2. **Obtain a Bing Image Search API Key:**

   - Sign up for a free account on [Azure Portal](https://portal.azure.com/).
   - Create a new **Bing Search v7** resource.
   - After creation, navigate to the resource and find your **Access Key** under the "Keys and Endpoint" section.

3. **Save the API Key:**

   - Replace `'YOUR_BING_IMAGE_SEARCH_API_KEY'` in the script with your actual API key.

4. **Create the `friend_images` Directory:**

   - Ensure a directory named `friend_images` exists in the same location as the script. You can create it manually or let the script create it for you.

5. **Save the CSV File:**

   - Save the CSV data provided earlier into a file named `fruits.csv` in the same directory as the script.

---

### **Python Script**

```python
import os
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

# Replace with your actual Bing Image Search API key
API_KEY = 'YOUR_BING_IMAGE_SEARCH_API_KEY'
SEARCH_URL = "https://api.bing.microsoft.com/v7.0/images/search"

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
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params  = {"q": fruit_name, "license": "public", "imageType": "photo", "count": 10}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Handle case where there are fewer results than desired index
    if len(search_results.get("value", [])) <= image_index:
        print(f"Not enough images found for {fruit_name}. Skipping.")
        return

    image_url = search_results["value"][image_index]["contentUrl"]
    try:
        image_response = requests.get(image_url, timeout=5)
        image_response.raise_for_status()
        image = Image.open(BytesIO(image_response.content)).convert('RGB')
        save_image(fruit_name, image)
    except Exception as e:
        print(f"Failed to download image for {fruit_name}: {e}")

def save_image(fruit_name, image):
    """Saves the image to the specified directory with the correct naming."""
    base_name = os.path.join(IMAGE_DIR, fruit_name)
    if not os.path.isfile(f"{base_name}.png"):
        image.save(f"{base_name}.png")
        print(f"Saved image as {base_name}.png")
    else:
        count = get_existing_image_count(fruit_name)
        image.save(f"{base_name}_{count+1}.png")
        print(f"Saved image as {base_name}_{count+1}.png")

def main():
    # Read the CSV file
    df = pd.read_csv('fruits.csv')
    fruit_friends = df[['Fruit Friend 1', 'Fruit Friend 2', 'Fruit Friend 3']].values.flatten()
    fruit_friends = [str(fruit).strip() for fruit in fruit_friends if pd.notnull(fruit)]

    for fruit_name in fruit_friends:
        fruit_name_clean = fruit_name.replace(" ", "_")
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
```

---

### **Explanation**

- **API Key and Endpoint:**
  - Replace `'YOUR_BING_IMAGE_SEARCH_API_KEY'` with your actual API key.
  - The script uses the Bing Image Search API to search for images.

- **Functions:**
  - `get_existing_image_count(fruit_name)`: Checks how many images already exist for a fruit.
  - `search_and_download_image(fruit_name, image_index)`: Searches for the image and downloads it.
  - `save_image(fruit_name, image)`: Saves the image with the correct naming convention.

- **Main Logic:**
  - Reads the CSV file and extracts all fruit friends.
  - Iterates over each fruit friend and checks if an image already exists.
    - If it exists, it skips to the next fruit.
    - If not, it determines which image index to download based on existing images.
  - Downloads and saves the image accordingly.

- **Image Naming Convention:**
  - If no image exists for a fruit, it saves as `<fruitName>.png`.
  - If images like `<fruitName>_1.png`, `<fruitName>_2.png` exist, it selects the next image index.

- **Image Conversion:**
  - The script converts all images to PNG format using the Pillow library.

---

### **Important Notes**

- **Error Handling:**
  - The script includes basic error handling for network requests and missing images.
  - If the Bing Image Search API doesn't return enough images, the script will skip that fruit.

- **Image Usage Rights:**
  - The script filters images by the "public" license, but you should still verify that you have the rights to use the downloaded images, especially for commercial purposes.

- **API Limits:**
  - The free tier of the Bing Image Search API has limitations on the number of requests per second and per month. Ensure you stay within these limits or consider upgrading your plan.

- **Compliance:**
  - Make sure to comply with the [Microsoft Azure Cognitive Services Terms](https://azure.microsoft.com/en-us/support/legal/) when using the Bing Image Search API.

---

### **Sample CSV File (`fruits.csv`)**

Ensure your `fruits.csv` file contains the data provided earlier. Here's a brief example of how it should look:

```csv
Fruit Name,Family Rank,Fruit Friend 1,Fruit Friend 2,Fruit Friend 3
Citron,Grandfather,Yuzu,Bergamot,Buddha's Hand
Kumquat,Grandmother,Calamansi,Limequat,Finger Lime
...
```

---

Let me know if you need further assistance or modifications to the script!