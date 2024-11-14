import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr')
    
    data = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:
            school_name = columns[2].text.strip()
            if school_name == "II LICEUM OGÓLNOKSZTAŁCĄCE IM. PŁK. LEOPOLDA LISA-KULI":
                row_data = [col.text.strip() for col in columns]
                data.append(row_data)
    
    return data

base_url = "https://sigg.gpw.pl/ranking/by-voivodeship/PODKARPACKIE?size=10&page="

all_data = []

for page in range(101):
    url = base_url + str(page) + "&sort="
    page_data = scrape_page(url)
    all_data.extend(page_data)

with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Zapisanie nagłówków
    csvwriter.writerow(['Rank', 'Investor', 'School Name', 'City', 'Amount', 'Change 1 Amount', 'Change 1 Percentage', 'Change 2 Amount', 'Change 2 Percentage', 'Unknown 1', 'Unknown 2'])
    # Zapisanie danych
    for row in all_data:
        change_1_amount, change_1_percentage = row[5].split('\n')[0], row[5].split('\n')[1]
        change_2_amount, change_2_percentage = row[6].split('\n')[0], row[6].split('\n')[1]
        csvwriter.writerow([row[0], row[1], row[2], row[3], row[4], change_1_amount, change_1_percentage, change_2_amount, change_2_percentage, row[7], row[8]])

print("Git jest")
