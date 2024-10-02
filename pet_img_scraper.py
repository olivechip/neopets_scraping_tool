import os
import requests
from bs4 import BeautifulSoup

moods = ["Happy", "Sad", "Angry", "Sick"]
genders = ["male", "female"]
colors = ["Red", "Blue", "Green", "Yellow"]

# Commented out species are currently inactive on Neopets
species = [
    # "Acara", "Aisha", "Blumaroo", "Bori", "Bruce", "Buzz", "Chia", 
    # "Chomby", "Cybunny", "Draik", 
    # "Elephante", "Eyrie", "Flotsam", "Gelert", "Gnorbu", "Grarrl", 
    #"Grundo", "Hissi", 
    "Ixi", 
    # "Jetsam", 
    # "Jubjub", "Kacheek", "Kau", 
    # "Kiko", "Koi", 
    # "Korbat", "Kougra", 
    # "Krawk", 
    # "Kyrii", "Lenny", "Lupe", 
    # "Lutari", 
    # "Meerca", "Moehog", 
    # "Mynci", "Nimmo", "Ogrin", "Peophin", 
    # "Poogle", 
    # "Pteri", "Quiggle", 
    # "Ruki", 
    # "Scorchio", "Shoyru", "Skeith", "Techo", 
    # "Tonu", 
    # "Tuskaninny", "Uni", "Usul", 
    # "Vandagyre", "Wocky", "Xweetok", "Yurble", "Zafara"
]

# Create the 'imgs' and 'urls' folders if they don't exist
if not os.path.exists("imgs"):
    os.makedirs("imgs")
if not os.path.exists("urls"):
    os.makedirs("urls")

# Construct headers with cookies (replace placeholders with your actual cookies)
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.sunnyneo.com/",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Iterate over each species
for specie in species:
    # Create a file to store the image URLs for the current species
    with open(os.path.join("urls", f"{specie.lower()}.txt"), "w") as url_file:
        # Create a folder for the images of the current species
        specie_folder = os.path.join("imgs", specie.lower())
        if not os.path.exists(specie_folder):
            os.makedirs(specie_folder)

        # Iterate in the order: mood, gender, color
        for mood in moods:
            for gender in genders:
                for color in colors:
                    # Construct the URL (mood in lowercase)
                    url = f"https://www.sunnyneo.com/rainbowpool.php?species={specie.lower()}&colour={color.lower()}#{gender}-{mood.lower()}"

                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Find the img tag
                    img_tag = soup.find("img", title=f"{mood} {gender} {color} {specie}")

                    if img_tag:
                        img_src = img_tag["src"]
                        img_url = "https://pets.neopets.com" + img_src.split("pets.neopets.com")[-1].split("?")[0]
                        img_url = img_url.rsplit("/", 1)[0] + "/4.png"

                        # Write the URL to the file
                        url_file.write(f"{specie.lower()}_{color.lower()}_{mood.lower()}_{gender}\n")
                        url_file.write(f"{img_url}\n\n")

                        # Send request with headers to download the image
                        response = requests.get(img_url, headers=headers)

                        if response.status_code == 200:
                            # Extract filename from the URL
                            filename = f"{mood.lower()}_{gender}_{color.lower()}_{specie.lower()}.png"
                            file_path = os.path.join(specie_folder, filename)

                            # Save the image
                            with open(file_path, "wb") as img_file:
                                img_file.write(response.content)

                            print(f"Downloaded {filename}")
                        else:
                            print(f"Failed to download image: {response.status_code} - {img_url}")
                    else:
                        print(f"No image found for {mood} {gender} {color} {specie}")

print("Done!")