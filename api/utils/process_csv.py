import csv
# Processes the community area CSV and crime rates CSV
def process_community_area(): 
   with open("data/community_areas.csv", "r") as file: 
      reader = csv.reader(file)
      next(reader)
      for row in reader: 
         if row[1] != row[3]:
            print(f"{row[1]}, {row[2]}, {row[3]}")

def process_crime_rates():
   with open("data/crime_rates.csv", "r") as file: 
      reader = csv.reader(file)
      print(next(reader))
      for row in reader: 
         for i in range(22):
            print(f"{row[i]}, type: {type(row[i])}")
         break
         
# process_community_area()
process_crime_rates()