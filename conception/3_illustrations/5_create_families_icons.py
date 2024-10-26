from openai import OpenAI
import os
import requests

# Fetch the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_SECRET_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_SECRET_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Create folder for icons
output_dir = './families_icons'
os.makedirs(output_dir, exist_ok=True)

# Define family names and file names
families = {
    "Citrus Family": "Citrus.png",
    "Berry Family": "Berries.png",
    "Stone Fruit Family": "Stones.png",
    "Tropical Fruit Family": "Tropical.png",
    "Pome Fruit Family": "Pomes.png",
    "Melon Family": "Melons.png",
    "Exotic Fruit Family": "Exotic.png"
}

# Define the common prompt style
prompt_style = "a minimalist icon representing a representative fruit of {family} with a black foreground and white background. Ensure the design is simple, geometric."

# Function to generate and save the image
def generate_icon(family, filename):
    image_path = os.path.join(output_dir, f"{filename}")
    if os.path.exists(image_path):
        print(f"Image for {family} already exists, skipping...")
        return
    prompt = prompt_style.format(family=family)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",  # Using the 1024x1792 size as requested
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url 
    
    # Download the image
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded and saved image for {family}")
        else:
            print(f"Failed to download image for {family}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image for {family}: {e}")

# Loop through the families and generate images
for family, filename in families.items():
    print(f"Generating icon for {family}...")
    generate_icon(family, filename)

print("Icons generated and saved in 'families_icons' folder.")
