from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from database import CountryDatabaseManager

app=FastAPI(title="country Data API")

db = CountryDatabaseManager("countries.db")

class Country(BaseModel):
    country_name: str = Field(min_length=1)
    capital: str
    population: int = Field(ge=0)
    area: float = Field(ge=0)

@app.get("/") 
def home():
    return {"message": "Welcome to the Country Data API"}
    
@app.get("/countries")
def get_countries():
    return db.read_all_countries()

@app.get("/countries/{country_name}")
def get_country(country_name: str):
    country = db.read_country(country_name)

    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country  

@app.post("/countries",status_code=201)
def create_country(country: Country):
    existing_country = db.read_country(country.country_name)
    if existing_country is not None:
        raise HTTPException(status_code=409, detail="Country already exists")

    country_data=country.model_dump()
    db.create_country(country_data)
    return{
        "message": "Country created successfully",
        "country": country_data
    }

@app.put("/countries/{country_name}")
def update_country(country_name: str, country: Country):
    existing_country = db.read_country(country_name)
    if existing_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    if country.country_name != country_name:
        raise HTTPException(status_code=400, detail="Country name in the body must match the URL")

    updated=db.update_country(
        country_name,
        country.capital,
        country.population,
        country.area
    )

    if not updated:
        raise HTTPException(status_code=404, detail="country not found")

    return {
        "message": "Country updated successfully",
        "country": db.read_country(country_name)
    }

@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    if not db.delete_country(country_name):
        raise HTTPException(status_code=404, detail="Country not found")

    return {
        "message": "Country deleted successfully",
        
    }