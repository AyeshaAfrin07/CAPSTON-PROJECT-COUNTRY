import requests
import pandas as pd

API_URL="http://127.0.0.1:8000/countries"

def fetch_countries():
    try:
        response=requests.get(API_URL,timeout=10)
        response.raise_for_status()

        countries=response.json()

        df=pd.DataFrame(countries)

        print("\n country Data:")
        print(df.to_string(index=False))

        df.to_csv("exported_countries.csv", index=False)

        print("\nData exported successfully to 'exported_countries.csv'\n")

    except requests.exceptions.RequestException as error:
        print("API request failed:",error)


if __name__ == "__main__":
    fetch_countries()