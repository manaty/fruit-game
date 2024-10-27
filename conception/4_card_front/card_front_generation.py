import pandas as pd
from PIL import Image
import os

# Constants
OUTPUT_WIDTH = 820
OUTPUT_HEIGHT = 1120

# Paths
fruit_properties_csv = '../2_files_preparation/1.2_fruit_properties.csv'
friends_csv = '../1_content/3_Friends.csv'
fruit_images_dir = '../3_illustrations/photorealistic/'
family_icons_dir = '../3_illustrations/families_icons/'
family_rank_icons_dir = '../3_illustrations/family_rank_icons/'
friend_images_dir = '../3_illustrations/friend_images/'
output_images_dir = 'card_front_images/'

# Create output directory if it doesn't exist
if not os.path.exists(output_images_dir):
    os.makedirs(output_images_dir)

# Read CSV files
fruit_properties = pd.read_csv(fruit_properties_csv)
friends = pd.read_csv(friends_csv)

# Lists for special vertical translations
translate_150_fruits = ['Lime', 'Gooseberry', 'Strawberry', 'Blueberry', 'Galia Melon']
translate_300_fruits = ['Date', 'Olive', 'Peach', 'Cherry', 'Plum', 'Jackfruit', 'Pineapple', 'Quince', 'Pear', 'Bitter Melon', 'Mangosteen']
translate_400_fruits = ['Pineapple']
# Loop over fruits
for index, row in fruit_properties.iterrows():
    fruit_name = row['Name']
    fruit_family_name = row['Family']

    # Get the family rank and friends from friends CSV
    friends_row = friends[friends['Fruit Name'] == fruit_name]
    if friends_row.empty:
        print(f"No friends found for {fruit_name}")
        continue
    family_rank = friends_row['Family Rank'].values[0]
    fruit_friend_1 = friends_row['Fruit Friend 1'].values[0].replace(' ', '')
    fruit_friend_2 = friends_row['Fruit Friend 2'].values[0].replace(' ', '')
    fruit_friend_3 = friends_row['Fruit Friend 3'].values[0].replace(' ', '')

    # Paths to images
    fruit_image_path = os.path.join(fruit_images_dir, f"{fruit_name}.png")
    family_icon_path = os.path.join(family_icons_dir, f"{fruit_family_name}.png")
    family_rank_icon_path = os.path.join(family_rank_icons_dir, f"{family_rank}.png")
    friend_image_paths = [
        os.path.join(friend_images_dir, f"{fruit_friend_1}.png"),
        os.path.join(friend_images_dir, f"{fruit_friend_2}.png"),
        os.path.join(friend_images_dir, f"{fruit_friend_3}.png")
    ]

    # Check if all image files exist
    if not os.path.isfile(fruit_image_path):
        print(f"Fruit image not found for {fruit_name}")
        continue
    if not os.path.isfile(family_icon_path):
        print(f"Family icon not found for {fruit_family_name}")
        continue
    if not os.path.isfile(family_rank_icon_path):
        print(f"Family rank icon not found for {family_rank}")
        continue
    missing_friend_images = [path for path in friend_image_paths if not os.path.isfile(path)]
    if missing_friend_images:
        print(f"Friend images not found for {fruit_name}: {missing_friend_images}")
        continue

    # Open images
    fruit_image = Image.open(fruit_image_path).convert('RGBA')
    family_icon = Image.open(family_icon_path).convert('RGBA')
    family_rank_icon = Image.open(family_rank_icon_path).convert('RGBA')
    friend_images = [Image.open(path).convert('RGBA') for path in friend_image_paths]

    # Create new image
    card_image = Image.new('RGBA', (OUTPUT_WIDTH, OUTPUT_HEIGHT), (255, 255, 255, 0))

    # Resize and position the fruit image
    fruit_image_aspect_ratio = fruit_image.width / fruit_image.height
    new_fruit_height = int(OUTPUT_WIDTH / fruit_image_aspect_ratio)
    fruit_image_resized = fruit_image.resize((OUTPUT_WIDTH, new_fruit_height), Image.Resampling.LANCZOS)

    # Determine vertical translation
    if fruit_name in translate_150_fruits:
        translate_y = -150
    elif fruit_name in translate_300_fruits:
        translate_y = -300
    elif fruit_name in translate_400_fruits:
        translate_y = -400
    else:
        translate_y = -200

    # Paste fruit image onto card
    card_image.paste(fruit_image_resized, (0, translate_y), fruit_image_resized)

    # Resize and position family icon
    family_icon_resized = family_icon.resize((200, 200), Image.Resampling.LANCZOS)
    card_image.paste(family_icon_resized, (72, 72), family_icon_resized)

    # Resize and position family rank icon
    family_rank_icon_resized = family_rank_icon.resize((200, 200), Image.Resampling.LANCZOS)
    x_position = OUTPUT_WIDTH - 200 - 72
    card_image.paste(family_rank_icon_resized, (x_position, 72), family_rank_icon_resized)

    # Resize and position friend images
    friend_image_sizes = [(273, 273), (274, 273), (273, 273)]
    x_positions = [0, 273, 547]
    y_position = OUTPUT_HEIGHT - 273

    for i, friend_image in enumerate(friend_images):
        friend_image_resized = friend_image.resize(friend_image_sizes[i], Image.Resampling.LANCZOS)
        if friend_image_resized.mode != 'RGBA':
            friend_image_resized = friend_image_resized.convert('RGBA')
        card_image.paste(friend_image_resized, (x_positions[i], y_position))

    # Save the image
    output_image_name = f"{index+1}_{fruit_name.replace(' ', '')}.png"
    output_image_path = os.path.join(output_images_dir, output_image_name)
    card_image.save(output_image_path)

    print(f"Generated card for {fruit_name} at {output_image_path}")
