I need a python script conception/4_card_front/card_front_generation.py that will create for each fruit a front image of a playing card containing the fruit image, an icon representing its family (Citrus, Berries, Stones, Tropical, Pomes,Melons,Exotic) , an icon representing its family rank (Grandfather, Grandmother, Father, Mother, Son), and the images of its three fruit friends.

from the file conception/2_files_preparation/1.2_fruit_properties.csv

that starts like
```
Name,Family,Family_scientific,Color(s),Place of Origin,Countries Where It Grows,Importance in Industry,Historical Significance,Nutritional Benefits,Medicinal Uses,Interesting Chemicals
Citron,Citrus,Rutaceae (Citrus family),Bright yellow when ripe,Southeast Asia (India or nearby regions),"India, China, Japan, Mediterranean countries like Italy and Greece","Used for candied peels, flavorings, essential oils in perfumes and aromatherapy; significant in religious rituals",One of the oldest citrus fruits; used in Jewish rituals during the festival of Sukkot as the Etrog,"Rich in vitamin C, dietary fiber, and antioxidants","Traditionally used to treat digestive issues, nausea, and skin conditions","Contains limonene, citral, and bioflavonoids"
Kumquat,Citrus,Rutaceae (Citrus family),Bright orange to yellow-orange,China,"China, Japan, Southeast Asia, the United States (Florida, California)","Consumed fresh, used in marmalades, jellies, candies, and liqueurs",Cultivated for centuries in China; symbolizes good luck and prosperity,"High in vitamin C, fiber, and antioxidants",Used in traditional Chinese medicine for coughs and sore throats,Rich in essential oils like limonene and pinene
Orange,Citrus,Rutaceae (Citrus family),Bright orange,Southeast Asia (possibly southern China),"Brazil, United States, India, China, Spain, Mexico","Widely consumed fresh and as juice; used in marmalades, candies, and flavorings; essential oils used in cosmetics and cleaning products",Introduced to Europe via trade routes; became a symbol of luxury and health,"Excellent source of vitamin C, fiber, folate, and antioxidants",Supports immune function; used in aromatherapy for its uplifting scent,"Contains hesperidin, limonene, and flavonoids"
...
```
You get the <fruit_name> from the first column and the <fruit_family_name> from the second column.
The png image file of the fruit is in conception/3_illustrations/photorealistic/<fruit_name>.png
the png image of the family is in conception/3_illustrations/families_icons/<fruit_family_name>.png


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
The <fruit_name> is in the first column (do not remove spaces in the name), the <family_rank> is in the second column and the three <fruit_friend_name> are form the third, fourth and fifth columns after removing the spaces in their name.
the png image file of the family rank is in conception/3_illustrations/family_rank_icons/<family_rank>.png
The png image file of the fruit friend is in conception/3_illustrations/friend_images/<fruit_friend_name>.png

The output should be a vertical pmg image file  or each fruit should be conception/4_card_front/card_front_images/<index>_<fruit_name>.png  where the index is the index of the fruit in the 1.2_fruit_properties.csv file.
The image should have dimension 820*1120px
The fruit image should be placed at the center of the image, and serves as background, do not change aspect ratio, but resize it to fit the image witdh 820px and translate the image 200px up (150px only for 'Lime', 'Gooseberry', 'Strawberry', 'Blueberry' and 'Galia Melon' and 300px for 'Date', 'Olive', 'Peach','Cherry', 'Plum', 'Jackfruit', 'Pineapple', 'Quince', 'Pear', 'Bitter Melon', 'Mangosteen').
The family icon should be placed at the top left corner of the image, width 200px and height 200px and left and top margin od 72px.
The faimly rank icon should be placed at the top right corner of the image, width 200px and height 200px and right and top margin of 72px.
The 3 fruit friends should be placed at the bottom of the image, width 273px and height 273px, and should be horizontally aligned, use with 274px for the middle image to avoid gaps.

Note that Image.ANTIALIAS is deprecated and should be replaced by Image.Resampling.LANCZOS.
Note that friend fruits images dont have an alpha channel 
Note that the python file will be executed from conception/4_card_front/
