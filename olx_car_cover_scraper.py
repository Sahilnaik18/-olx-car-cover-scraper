import requests
from bs4 import BeautifulSoup
import csv

# Base URL for searching "Car Cover"
BASE_URL = "https://www.olx.in/items/q-car-cover"

# Headers to simulate a browser visit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def get_olx_listings(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = []

    # Find all ad containers
    ads = soup.select('li[data-aut-id="itemBox"]')

    for ad in ads:
        try:
            title = ad.select_one('span[data-aut-id="itemTitle"]').text.strip()
            price = ad.select_one('span[data-aut-id="itemPrice"]').text.strip()
            location = ad.select_one('span[data-aut-id="item-location"]').text.strip()
            listings.append({
                'Title': title,
                'Price': price,
                'Location': location
            })
        except AttributeError:
            continue  # Skip if any field is missing

    return listings

def save_to_csv(data, filename="olx_car_covers.csv"):
    keys = data[0].keys() if data else ['Title', 'Price', 'Location']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    print("🔍 Scraping OLX India for Car Covers...")
    url = BASE_URL
    data = get_olx_listings(url)
    
    if data:
        save_to_csv(data)
        print(f"✅ Done! {len(data)} listings saved to 'olx_car_covers.csv'")
    else:
        print("⚠️ No listings found or structure has changed.")

if __name__ == "__main__":
    main()
