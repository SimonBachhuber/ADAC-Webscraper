import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# Output File
output_filename = 'data/all_cars.json'

# The URL to scrape
base_url = "https://www.adac.de/rund-ums-fahrzeug/autokatalog/marken-modelle/?sort=SORTING_DESC"

# Send a GET request to the base page
response = requests.get(base_url)
response.raise_for_status()

# Parse the HTML content of the base page
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize the dictionary to hold data
all_cars = {}

# Find all main divs with the specified class
main_divs = soup.find_all('div', class_="sc-12b7852f-2 sc-2395b325-0 sc-12b7852f-3 sc-7440936f-2 iOSpch hyHcmC kczXcM")

# Loop through the divs to find each <a> element and the nested <p> element
for div in main_divs:
    # Find the <a> tag that is directly above the <p> tag
    maker_tags = div.find_all('a')

    if maker_tags:
        for maker_tag in maker_tags:
        
            # Get the link from the <a> tag
            href = maker_tag.get('href')
            
            # Form the full URL (handle relative URLs)
            full_url = urljoin(base_url, href)
            
            # Find the <p> element in the base page div with the specified class
            maker_p_element = maker_tag.find('p')
            
            if maker_p_element:
                # Get the text content of the <p> element to use as the dictionary key
                maker_name = maker_p_element.get_text(strip=True).capitalize()
                maker_name = "Mercedes" if maker_name == "Mercedes-Benz" else maker_name
                print(maker_name)
                
                # Visit the linked page
                models_response = requests.get(full_url)
                models_response.raise_for_status()
                
                # Parse the linked page content
                models_soup = BeautifulSoup(models_response.content, 'html.parser')
                
                # Find the target div on the linked page
                models_divs = models_soup.find_all('div', class_="sc-acbf8e00-0 ilVHcr")
                
                # Initialize a list to hold the text from <p> elements on the linked page
                linked_p_texts = []
                
                # Loop through the target divs and extract text from <p> elements with the specified class
                for model in models_divs:
                    model_name = model.find_all('p', class_="dMEK_RYMXzHdo4LnYdUq")
                    for p in model_name:
                        linked_p_texts.append(p.get_text(strip=True))
                        print(p.get_text(strip=True))
                
                # Add to dictionary: key is the base <p> text, value is the list of texts from linked page
                all_cars[maker_name] = linked_p_texts

# Output the constructed dictionary
for key, value in all_cars.items():
    print(f"Base text: {key}")
    print(f"Linked texts: {value}\n")


# Save the dictionary to a JSON file
with open(output_filename, 'w', encoding='utf-8') as json_file:
    json.dump(all_cars, json_file, ensure_ascii=False, indent=4)

print(f"Dictionary saved to {output_filename}")


with open(output_filename, 'r', encoding='utf-8') as json_file:
    loaded_dict = json.load(json_file)

print("Loaded dictionary:")
print(loaded_dict)
