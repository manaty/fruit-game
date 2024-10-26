import os
import csv
from openai import OpenAI
import requests

# Fetch the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_SECRET_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_SECRET_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Directory to save images
output_dir = './photorealistic'
os.makedirs(output_dir, exist_ok=True)

# CSV file path
csv_file = '../2_files_preparation/1.2_fruit_properties.csv'

# Function to generate an image from OpenAI using DALL-E 3
def generate_image(fruit_name):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A photorealistic vertical image of a mate not wrinkled {fruit_name}",
            size="1024x1792",  # Using the 1024x1792 size as requested
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url 
        return image_url
    except Exception as e:
        print(f"Error generating image for {fruit_name}: {e}")
        return None

# Function to download and save the image
def download_image(image_url, fruit_name):
    image_path = os.path.join(output_dir, f"{fruit_name}.png")
    if os.path.exists(image_path):
        print(f"Image for {fruit_name} already exists, skipping...")
        return
    
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded and saved image for {fruit_name}")
        else:
            print(f"Failed to download image for {fruit_name}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image for {fruit_name}: {e}")

# Main function to process the CSV file and generate images
def process_fruits_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line (header)

        for row in reader:
            if row:  # Ensure row is not empty
                fruit_name = row[0].strip()  # Don't convert to lowercase
                image_path = os.path.join(output_dir, f"{fruit_name}.png")
                
                # Skip if the image already exists
                if os.path.exists(image_path):
                    print(f"Image for {fruit_name} already exists, skipping...")
                    continue
                
                # Generate the image URL
                image_url = generate_image(fruit_name)
                
                if image_url:
                    download_image(image_url, fruit_name)
                else:
                    print(f"Could not generate an image for {fruit_name}")

# Run the script
if __name__ == '__main__':
    process_fruits_csv(csv_file)
