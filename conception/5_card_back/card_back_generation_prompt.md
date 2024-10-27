I need a python script conception/5_card_back/card_back_generation.py that will create for each fruit a back image of a playing card containing the fruit name, and information ina way that is readable for the owner of the card but difficult to read from other player as the back of the card should not allow other player to reveal them the fruit displayed on the front of the cards or the 3 friends of the fruit.

from the file conception/2_files_preparation/1.2_fruit_properties.csv

that starts like
```
Name,Family,Family_scientific,Color(s),Place of Origin,Countries Where It Grows,Importance in Industry,Historical Significance,Nutritional Benefits,Medicinal Uses,Interesting Chemicals
Citron,Citrus,Rutaceae (Citrus family),Bright yellow when ripe,Southeast Asia (India or nearby regions),"India, China, Japan, Mediterranean countries like Italy and Greece","Used for candied peels, flavorings, essential oils in perfumes and aromatherapy; significant in religious rituals",One of the oldest citrus fruits; used in Jewish rituals during the festival of Sukkot as the Etrog,"Rich in vitamin C, dietary fiber, and antioxidants","Traditionally used to treat digestive issues, nausea, and skin conditions","Contains limonene, citral, and bioflavonoids"
Kumquat,Citrus,Rutaceae (Citrus family),Bright orange to yellow-orange,China,"China, Japan, Southeast Asia, the United States (Florida, California)","Consumed fresh, used in marmalades, jellies, candies, and liqueurs",Cultivated for centuries in China; symbolizes good luck and prosperity,"High in vitamin C, fiber, and antioxidants",Used in traditional Chinese medicine for coughs and sore throats,Rich in essential oils like limonene and pinene
Orange,Citrus,Rutaceae (Citrus family),Bright orange,Southeast Asia (possibly southern China),"Brazil, United States, India, China, Spain, Mexico","Widely consumed fresh and as juice; used in marmalades, candies, and flavorings; essential oils used in cosmetics and cleaning products",Introduced to Europe via trade routes; became a symbol of luxury and health,"Excellent source of vitamin C, fiber, folate, and antioxidants",Supports immune function; used in aromatherapy for its uplifting scent,"Contains hesperidin, limonene, and flavonoids"
...
```
You get the following <fruit_name>,Family,Family_scientific,Color(s),Place of Origin,Countries Where It Grows,Importance in Industry,Historical Significance,Nutritional Benefits,Medicinal Uses,Interesting Chemicals


from the file conception/1_content/3_Friends.csv

that starts like
```
Fruit Name,Family Rank,Fruit Friend 1,Fruit Friend 2,Fruit Friend 3
Citron,Grandfather,Yuzu,Bergamot,Buddha's Hand
Kumquat,Grandmother,Calamansi,Limequat,Finger Lime
Orange,Father,Tangerine,Clementine,Mandarin Orange
Lemon,Mother,Meyer Lemon,Eureka Lemon,Sweet Lemon
Lime,Son,Key Lime,Kaffir Lime,Desert Lime
...
```
The <fruit_name> is in the first column (remove spaces in the name for the filename), the <family_rank> is in the second column and the three <fruit_friend_name> are form the third, fourth and fifth columns after removing the spaces in their name.

The output should be a vertical pmg image file for each fruit should be conception/5_card_back/card_back_images/<index>_<fruit_name>_back.png  where the index is the index of the fruit in the 1.2_fruit_properties.csv file.
The image should have dimension 820*1120px

The back image of the card should be a white background with a grey border of 80px.
the center area must be filled with 60*60px grey png icons present in conception/3_illustrations/families_icons/ using 20% opacity (use all icons successively , all cards must have same backgroud)

The fruit information should be placed left aligned in darker grey text.
The font file is in conception/3_illustrations/fonts/DejaVuSans.ttf
The name and family should not be blocks written after Color(s),Place of Origin,Countries Where It Grows.
'Family_scientific' should be written in "Scientific Family".
The last information block is "Friends fruits from left to right: <fruit_friend_1>, <fruit_friend_2>, <fruit_friend_3>"

Each type of information form a block 
Those blocks have 10px margin.
Make sure all blocks fit in the central area card.

Note that 'FreeTypeFont' object has no attribute 'getsize'
Note that Image.ANTIALIAS is deprecated and should be replaced by Image.Resampling.LANCZOS.
Note that the python file will be executed from conception/5_card_back/

