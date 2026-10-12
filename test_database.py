from database import CountryDatabaseManager
db=CountryDatabaseManager("test_countries.db")
country={
    "country_name": "Testland",
    "capital":"Test City",
    "population":100000,
    "area":2500.5
}
print(db.create_country(country ))

print("\nAll countries:")
print(db.read_all_countries())

print("\n Single Country:")
print(db.read_country("Testland"))

print("\nupdating country:")
print(
    db.update_country("Testland", "New Test City", 120000, 2600.5)
)

print("\n Deleting country:")
print(db.delete_country("Testland"))

print(db.read_country("Testland"))