# Import required methods
import random
import os
import sys
from requests import get
from json import loads
from shutil import copyfileobj
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()

mastodon = Mastodon(
    access_token = os.getenv("token"),
    api_base_url = os.getenv("url")
)

random_number = random.randint(0,160)

set_code= open('set_codes.txt')
set_total = open('set_total_cards.txt')

set_code = [line.rstrip('\n') for line in set_code.readlines() if line.strip() != '']
set_total = [line.rstrip('\n') for line in set_total.readlines() if line.strip() != '']

cardid = (set_code[random_number])
cardtotal = (set_total[random_number])

# takes the card set total cards and randomizes the number to pick a card from that set (eg: base1-34)
cardtotal = int(cardtotal)
cardtotal = (random.randint(1,cardtotal))
cardtotal = str( cardtotal)

# Load the card data from PokemonTCGAPI

# This is the actual random card: 
card = loads(get(f"https://api.pokemontcg.io/v2/cards/"+cardid+"-"+cardtotal+"").text)

# Get the image URL
img_url = card['data']['images']['large']

# Get card title
poke_title = card['data']['name']

# Artist name
poke_artist = card['data']['artist']

# Get flavor text
poke_flavor = card['data']['flavorText']

# Save the image
with open('image.jpg', 'wb') as out_file:
    copyfileobj(get(img_url, stream = True).raw, out_file)

# Removing weird or unusable characters for hashtags
special_characters=["$","'","`","%","&","(",")",":","?","!","@","*"," "]
for i in special_characters:
    hTitle = poke_title.replace(i,"")
    hArtist = poke_artist.replace(i,"")

    hArtist = hArtist.replace('.', '')
    hArtist = hArtist.replace(',', '')
    hArtist = hArtist.replace("'", '')
    hTitle = hTitle.replace(',',"")
    hTitle = hTitle.replace('.',"")
    hTitle = hTitle.replace(':',"")
    hTitle = hTitle.replace("'","")

# Set the Mastodon post information
media = mastodon.media_post("image.jpg", description="Card Name: " + poke_title + "\n" + "Description: "  + poke_flavor + "\n" + "Artist: " + poke_artist)

# Print Text
print (poke_title)
print (img_url)
print (poke_flavor)

# Post the Toot
print(mastodon.status_post("#pokemon" + " " + "#pokemontcg" + " " + "#" + hTitle + " " + "#" + hArtist,media_ids=media))