import csv
import os
import requests
import wikipedia

images_dir = './images'
os.makedirs(images_dir, exist_ok=True)

csv_file = '1.2_fruit_properties.csv'

exclude_terms = [
    'icon', 'logo', 'symbol', 'map', 'location', 'coat of arms', 'flag',
    'diagram', 'chart', 'emblem', 'heraldry', 'crest', 'insignia',
    'anatomy', 'taxonomy'
]

headers = {'User-Agent': 'fruit-image-downloader/1.0 (https://example.com)'}

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        fruit_name = row['Name']
        fruit_page_title = fruit_name + ' fruit'
        print(f"\nProcessing fruit: {fruit_name}")
        try:
            page = wikipedia.page(fruit_page_title)
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error for {fruit_page_title}: {e.options}")
            page = None
            for option in e.options:
                if 'fruit' in option.lower() or option.lower() == fruit_name.lower():
                    try:
                        page = wikipedia.page(option)
                        break
                    except Exception:
                        continue
            if page is None:
                print(f"Could not resolve disambiguation for {fruit_page_title}")
                continue
        except wikipedia.exceptions.PageError:
            print(f"Page not found for {fruit_page_title}, trying alternative")
            alt_page_title = fruit_name + ' (fruit)'
            try:
                page = wikipedia.page(alt_page_title)
            except Exception as e:
                print(f"Could not find page for {alt_page_title}: {e}")
                continue

        images = page.images
        print(f"Found {len(images)} images for {page.title}")
        for image_url in images:
            if any(image_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                if any(term in image_url.lower() for term in exclude_terms):
                    continue
                image_filename = os.path.basename(image_url)
                image_filename = fruit_name.replace(' ', '_') + '_' + image_filename
                image_path = os.path.join(images_dir, image_filename)
                if os.path.exists(image_path):
                    print(f"Image {image_filename} already exists, skipping.")
                    continue
                print(f"Downloading image: {image_url}")
                response = requests.get(image_url, headers=headers, stream=True)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                else:
                    print(f"Failed to download image: {image_url}")
