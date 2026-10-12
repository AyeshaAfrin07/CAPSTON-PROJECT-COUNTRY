import requests
import csv
import os
from bs4 import BeautifulSoup
class CountryScraper:
    URL = 'https://www.scrapethissite.com/pages/simple/'

    def scrape_countries(self,limit=20):
        response=requests.get(
            self.URL,
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0'}

        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        country_elements=soup.select('div.country')
        print("country cards found:",len(country_elements))
        countries=[]
        
        for element in country_elements:
            if len(countries)>=limit:
                break
            
            name_element=element.select_one(".country-name")
            capital_element=element.select_one(".country-capital")
            population_element=element.select_one(".country-population")
            area_element=element.select_one(".country-area")

            if not all([
                name_element,capital_element,population_element,area_element
            ]):
                print("skipping card withmisiing fields")
                continue

            try:
                name=name_element.get_text(strip=True)
                capital=capital_element.get_text(strip=True)
                population=population_element.get_text(strip=True)
                area=area_element.get_text(strip=True)

                population=int(population.replace(',', ''))
                area=float(area.replace(',', ''))

                country = {
                    'name': name,
                    'capital': capital,
                    'population': population,
                    'area': area
                }
                countries.append(country)
            except (ValueError,TypeError) as error:
                print(f"skipping invalid record:{error}")
                continue

        return countries


if __name__ == "__main__":
    scraper=CountryScraper()
    Country_data=scraper.scrape_countries(limit=20)
    print(f'total countries scraped:{len(Country_data)}')

    csv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"exported_countries.csv")
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['name', 'capital', 'population', 'area']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Country_data)
        
print(f"Exported successfully:{csv_path}")