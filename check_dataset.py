import pandas as pd

df = pd.read_csv("data/tickets.csv")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nCategories:")
print(df["category"].value_counts())