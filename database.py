import sqlite3

class CountryDatabaseManager:
    def __init__(self, db_name="countries.db"):
        self.db_name=db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
            ''')

    def create_country(self,country):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
            ''', (
                country["country_name"], 
                country["capital"], 
                country["population"], 
                country["area"]))

        return {"message":"Country created successfully."}

    def create_countries(self, countries):
        with sqlite3.connect(self.db_name) as conn:
            conn.executemany('''
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
            ''', [
                (
                    country["country_name"], 
                    country["capital"], 
                    country["population"], 
                    country["area"]
                ) for country in countries
            ])

        return {"message":f'{len(countries)} countries inserted successfully.'}

    def read_all_countries(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            rows=conn.execute('SELECT * FROM countries ORDER BY country_name').fetchall()
        return [dict(row) for row in rows]

    def read_country(self, country_name):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute('SELECT * FROM countries WHERE country_name = ?', (country_name,)).fetchone()
        return dict(row) if row else None

    def update_country(self,country_name,capital,population,area):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.execute('''
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE country_name = ?
            ''', (capital, population, area, country_name))

            updated=cursor.rowcount>0

        if updated:
            return {"message":"Country updated successfully."}
        else:
            return {"message":"Country not found."}

    def delete_country(self, country_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute('''DELETE FROM countries WHERE country_name = ?''', (country_name,))
            deleted = cursor.rowcount > 0

        if deleted:
            return {"message":"Country deleted successfully."}
        else:
            return {"message":"Country not found."}


if __name__ == "__main__":
    db = CountryDatabaseManager()
    print("Database created successfully.")