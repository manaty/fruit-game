import os
import csv
from PIL import Image, ImageDraw, ImageFont

# Set paths relative to the execution directory (conception/5_card_back/)
fruit_properties_path = "../2_files_preparation/1.2_fruit_properties.csv"
friends_csv_path = "../1_content/3_Friends.csv"
icons_dir = "../3_illustrations/families_icons/"
font_path = "../3_illustrations/fonts/DejaVuSans.ttf"
output_dir = "card_back_images"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load font
font_size = 20
font = ImageFont.truetype(font_path, font_size)

# Read fruit properties
fruit_data_list = []
with open(fruit_properties_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader):
        fruit_data = {
            'index': idx + 1,
            'Name': row['Name'].replace(' ', ''),
            'OriginalName': row['Name'],
            'Family': row['Family'],
            'Family_scientific': row['Family_scientific'],
            'Color(s)': row['Color(s)'],
            'Place of Origin': row['Place of Origin'],
            'Countries Where It Grows': row['Countries Where It Grows'],
            'Importance in Industry': row['Importance in Industry'],
            'Historical Significance': row['Historical Significance'],
            'Nutritional Benefits': row['Nutritional Benefits'],
            'Medicinal Uses': row['Medicinal Uses'],
            'Interesting Chemicals': row['Interesting Chemicals'],
        }
        fruit_data_list.append(fruit_data)

# Read friends data
friends_dict = {}
with open(friends_csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fruit_name = row['Fruit Name'].replace(' ', '')
        friends = [
            row['Fruit Friend 1'].replace(' ', ''),
            row['Fruit Friend 2'].replace(' ', ''),
            row['Fruit Friend 3'].replace(' ', '')
        ]
        friends_dict[fruit_name] = friends

# Merge friends into fruit data
for fruit_data in fruit_data_list:
    fruit_name = fruit_data['Name']
    fruit_data['Friends'] = friends_dict.get(fruit_name, [])

# Load and resize icons
icon_filenames = [
    f for f in os.listdir(icons_dir) if f.endswith('.png')
]
icon_images = []
for filename in icon_filenames:
    icon = Image.open(os.path.join(icons_dir, filename)).convert('RGBA')
    icon = icon.resize((60, 60), resample=Image.Resampling.LANCZOS)
    icon_images.append(icon)

# Create background image
def create_background_image():
    img = Image.new('RGBA', (820, 1120), 'white')
    draw = ImageDraw.Draw(img)
    border_color = (128, 128, 128)
    draw.rectangle([0, 0, 819, 1119], outline=border_color, width=80)

    central_area = (80, 80, 740, 1040)
    icon_opacity = int(255 * 0.2)
    icon_index = 0
    icons_per_row = (660 // 60) + 1
    icons_per_column = (960 // 60) + 1

    for y in range(icons_per_column):
        for x in range(icons_per_row):
            icon = icon_images[icon_index % len(icon_images)].copy()
            icon_index += 1
            alpha = icon.split()[3]
            alpha = alpha.point(lambda p: icon_opacity)
            icon.putalpha(alpha)
            pos_x = 80 + x * 60
            pos_y = 80 + y * 60
            if pos_x > 680 or pos_y > 980:
                continue
            img.paste(icon, (pos_x, pos_y), icon)
    return img

background_img = create_background_image()

# Function to wrap text
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    i = 0
    while i < len(words):
        line = ''
        while i < len(words):
            test_line = line + words[i] + ' '
            text_width = font.getbbox(test_line)[2]
            if text_width <= max_width:
                line = test_line
                i += 1
            else:
                break
        lines.append(line.strip())
    return lines

# Generate card backs
for fruit_data in fruit_data_list:
    img = background_img.copy()
    draw = ImageDraw.Draw(img)
    text_color = (64, 64, 64)
    line_spacing = 4
    block_margin = 10
    text_start_x = 90
    current_y = 90
    max_text_width = 640

    blocks = [
        ('Scientific Family', fruit_data['Family_scientific']),
        ('Color(s)', fruit_data['Color(s)']),
        ('Place of Origin', fruit_data['Place of Origin']),
        ('Countries Where It Grows', fruit_data['Countries Where It Grows']),
        ('Name', fruit_data['OriginalName']),
        ('Family', fruit_data['Family']),
        ('Importance in Industry', fruit_data['Importance in Industry']),
        ('Historical Significance', fruit_data['Historical Significance']),
        ('Nutritional Benefits', fruit_data['Nutritional Benefits']),
        ('Medicinal Uses', fruit_data['Medicinal Uses']),
        ('Interesting Chemicals', fruit_data['Interesting Chemicals']),
        ('Friends', "Left to right: " + ', '.join(fruit_data['Friends']))
    ]

    for title, content in blocks:
        title_text = title + ":"
        title_height = font.getbbox(title_text)[3]
        draw.text((text_start_x, current_y), title_text, font=font, fill=text_color)
        current_y += title_height + line_spacing

        content_lines = wrap_text(content, font, max_text_width)
        for line in content_lines:
            line_height = font.getbbox(line)[3]
            draw.text((text_start_x, current_y), line, font=font, fill=text_color)
            current_y += line_height + line_spacing

        current_y += block_margin
        if current_y > 1030:
            print(f"Warning: Text exceeds the central area for fruit {fruit_data['OriginalName']}")
            break

    output_filename = f"{fruit_data['index']}_{fruit_data['Name']}_back.png"
    print(f"Saving {output_filename}")
    output_path = os.path.join(output_dir, output_filename)
    img.save(output_path)
