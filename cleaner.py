import pandas as pd
print ("loading messy excel file...")

# 1. Read the dirty Excel file
df = pd.read_excel ("dirty_data.xlsx")

print ("cleaning data...")

# 2. Clean the text First(This turns both SHEILA and SheILA into Sheila)
df ["Client Name"] = df["Client Name"].str.strip().str.capitalize()

# 3. Remove completely duplicate rows
df = df.drop_duplicates()

#3. Fix names: Capitalize just the first letter (Changes "SHEILA" to "Sheila")
#this one is used to handle literal duplicates
#df ["Client Name"] = df['Client Name'].str.strip().str.capitalize()

# 4. Fill in the missing names with a placeholder
#df["Client Name"] = df["Client Name"].fillna(0)

# 4. Handle missing names with a placeholder
df["Client Name"] = df["Client Name"].fillna("Unknown Client")

#5. Handle missing revenue by replacing blank spots with 0
df["Revenue"] = df["Revenue"].fillna(0)

# 6. Replace non-date text mistakes with a standard format
df["Joint Date"] = pd.to_datetime(df["Joint Date"], errors='coerce')

print("saving clean file...")

# 7. Export the polished data back to a brand new Excel sheet
df.to_excel("clean_data.xlsx", index=False)

print("Success! Your clean file \'clean_data.xlsx\' is ready!")