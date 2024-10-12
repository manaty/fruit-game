taking example on this program :

```
import csv
import re
import requests
import wikipedia
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))

csv_file = '../files/country_landmarks.csv'
imagesPath = "../files/images/"

def download_image(url, country_name, landmark_name):
    headers = {
        'User-Agent': 'game-country/1.0 (https://github.com/manaty/country-game)'
    }

    # Construct the relative path
    relative_path = os.path.join(imagesPath,f"{country_name+'_'+landmark_name.replace(' ', '_')}.jpg")
    
    if os.path.exists(relative_path):
        print(f"file {relative_path} already exists, skip the image download")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(relative_path), exist_ok=True)

    # Download and save the image
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(relative_path, 'wb') as file:
            print(f"Size of content: {len(response.content)} bytes")
            file.write(response.content)

def askChatGPT(country,landmark):
    # Crafting the prompt to ask for landmarks of the countries in input
    prompt_user = f"Please provide the url of an image of the famous landmark `{landmark}` of the country `{country}`."
    print(prompt_user)

    completion = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "user", "content": prompt_user},
    ],
    max_tokens=2000,  # Increased to accommodate longer response
    n=1,
    stop=None,
    temperature=0)

    # Extracting the response content
    response_text = completion.choices[0].message.content
    print(response_text)

    return response_text


def download_landmarks_images(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        countryIndex = 0
        for row in reader:
            countryIndex+=1
            country = row[0]
            landmarks = row[1:]
            index=0

            for landmark in landmarks:
                index+=1
                landmark_name = landmark.split(',')[0].strip()
                # if there is already an image for this landmark, skip it
                imageFilename = f"{countryIndex}_{country}_{index}_{landmark_name.replace(' ', '_')}.jpg"
                if os.path.exists(os.path.join(imagesPath,imageFilename)):
                    print(f"file {imageFilename} already exists, skip the image download")
                    continue
                print(f"Searching for {landmark_name} using wikipedia")
                try:
                    page = wikipedia.page(f"{landmark_name}, {country}")
                    if page.images:
                        print(f"Found {len(page.images)} images in wikipedia for {landmark_name}")
                        # Print all the page.images URLs
                        for image_url in page.images:
                            print(f"image url: {image_url}")
                            if image_url.lower().endswith('.jpg') and 'location_map' not in image_url:
                                print(f"Downloading image for {landmark_name} and url {image_url}")
                                download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                                # continue with the next landmark
                                continue
                    else:
                        print(f"No images found for {landmark_name}")
                except wikipedia.exceptions.PageError:
                    print(f"No Wikipedia page found for {landmark_name}")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"Disambiguation error for {landmark_name}, possible options: {e.options}")
                    page = wikipedia.page(landmark_name + ' ' + country)
                    try:
                        page = wikipedia.page(landmark_name)
                        if page.images:
                            # Print all the page.images URLs
                            for image_url in page.images:
                                if image_url.lower().endswith('.jpg') and 'location_map' not in image_url:
                                    print(f"Downloading image for {landmark_name} and url {image_url}")
                                    download_image(image_url, str(countryIndex)+'_'+country, str(index)+'_'+landmark_name)
                                    # continue with the next landmark
                                    continue
                        else:
                            print(f"No images found for {landmark_name}")
                    except wikipedia.exceptions.PageError:
                        print(f"No Wikipedia page found for {landmark_name}")
                    except wikipedia.exceptions.DisambiguationError as e:
                        print(f"Disambiguation error for {landmark_name}, possible options: {e.options}")
                    

if __name__ == "__main__":
    download_landmarks_images(csv_file)
```

please create a python program '2.1_fruit_img_download.py' that will use the csv file '1.2_fruit_properties.csv' to download in ./images an image of each fruit

th csv file is like this:
```
Name,Family,Color(s),Place of Origin,Countries Where It Grows,Importance in Industry,Historical Significance,Nutritional Benefits,Medicinal Uses,Interesting Chemicals
Citron,Rutaceae (Citrus family),Bright yellow when ripe,Southeast Asia (India or nearby regions),"India, China, Japan, Mediterranean countries like Italy and Greece","Used for candied peels, flavorings, essential oils in perfumes and aromatherapy; significant in religious rituals",One of the oldest citrus fruits; used in Jewish rituals during the festival of Sukkot as the Etrog,"Rich in vitamin C, dietary fiber, and antioxidants","Traditionally used to treat digestive issues, nausea, and skin conditions","Contains limonene, citral, and bioflavonoids"
Kumquat,Rutaceae (Citrus family),Bright orange to yellow-orange,China,"China, Japan, Southeast Asia, the United States (Florida, California)","Consumed fresh, used in marmalades, jellies, candies, and liqueurs",Cultivated for centuries in China; symbolizes good luck and prosperity,"High in vitamin C, fiber, and antioxidants",Used in traditional Chinese medicine for coughs and sore throats,Rich in essential oils like limonene and pinene
Orange,Rutaceae (Citrus family),Bright orange,Southeast Asia (possibly southern China),"Brazil, United States, India, China, Spain, Mexico","Widely consumed fresh and as juice; used in marmalades, candies, and flavorings; essential oils used in cosmetics and cleaning products",Introduced to Europe via trade routes; became a symbol of luxury and health,"Excellent source of vitamin C, fiber, folate, and antioxidants",Supports immune function; used in aromatherapy for its uplifting scent,"Contains hesperidin, limonene, and flavonoids"
Lemon,Rutaceae (Citrus family),Bright yellow,Northeast India or China,"India, Mexico, Argentina, Spain, United States","Used in beverages (lemonade), cooking, baking, cleaning products, cosmetics, and aromatherapy",Used by sailors to prevent scurvy; symbol of cleanliness and freshness,"High in vitamin C, flavonoids, and potassium","Aids digestion, boosts immunity, used in traditional remedies for sore throats","Contains citric acid, limonene, and ascorbic acid"
```

When looking for wikipedia page do not using only the fruit name, append " fruit" to it, for instance instead of "Apple" lookup the page "Apple fruit".

Download all the images of the page in the ./images directory.
