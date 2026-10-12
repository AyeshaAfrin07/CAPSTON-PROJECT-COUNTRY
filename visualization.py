import pandas as pd
import matplotlib.pyplot as plt

csv_file="exported_countries.csv"
def create_plot():
    df=pd.read_csv(csv_file)
    df["population"]=pd.to_numeric(df["population"], errors="coerce")
    df['area']=pd.to_numeric(df['area'], errors="coerce")
    df=df.dropna(subset=["population", "area"])
    plt.figure(figsize=(10, 6))
    plt.scatter(df["area"], df["population"],alpha=0.75)
    plt.title("Population vs Area")
    plt.xlabel("population")
    plt.ylabel("area")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("population_vs_area.png",dpi=300)

    plt.close()
    print('plot created')
    plt.show()
if __name__ == "__main__":
    create_plot()