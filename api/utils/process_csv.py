import csv
from ..utils.db_config import create_db_and_tables, get_session, get_db_url
from ..models.db_models import *
from ..utils.string_utils import *
import tempfile
import psycopg2
import os
import time
import requests
import pandas as pd
from shapely.wkt import loads as load_wkt
from geoalchemy2.shape import from_shape
# List of violent crimes
VIOLENT_CRIMES = [
    "ASSAULT",
    "BATTERY",
    "CRIMINAL SEXUAL ASSAULT",
    "HOMICIDE",
    "HUMAN TRAFFICKING",
    "INTIMIDATION",
    "KIDNAPPING",
    "OFFENSE INVOLVING CHILDREN",
    "ROBBERY",
    "SEX OFFENSE",
    "STALKING"
]

NONVIOLENT_CRIMES = [
    "ARSON",
    "BURGLARY",
    "CONCEALED CARRY LICENSE VIOLATION",
    "CRIMINAL DAMAGE",
    "CRIMINAL TRESPASS",
    "DECEPTIVE PRACTICE",
    "GAMBLING",
    "INTERFERENCE WITH PUBLIC OFFICER",
    "LIQUOR LAW VIOLATION",
    "MOTOR VEHICLE THEFT",
    "NARCOTICS",
    "NON-CRIMINAL",
    "OBSCENITY",
    "OTHER NARCOTIC VIOLATION",
    "OTHER OFFENSE",
    "PROSTITUTION",
    "PUBLIC INDECENCY",
    "PUBLIC PEACE VIOLATION",
    "RITUALISM",
    "THEFT",
    "WEAPONS VIOLATION"
]

def get_row_count(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        return cur.fetchone()[0]
    
# Processes the community area CSV and crime rates CSV
def process_community_area(): 
   print(os.getcwd())
   # Load data with total population per community area
   response = requests.get("https://data.cityofchicago.org/resource/t68z-cikk.json")
   if response.status_code==200: 
      data = response.json()
      total_pop_data = {}
      for point in data:
         community_area = point['community_area']
         total_pop_data[community_area] = {k: v for k, v in point.items() if k != "community_area"}
   community_areas=pd.read_csv("api/utils/data/community_areas.csv")
   community_areas['total_population']=0
   # print(community_areas.head())
   for index, row in community_areas.iterrows():
      # print(total_pop_data[row["COMMUNITY"]])
      community_areas.at[index, "total_population"] = int(float(total_pop_data[row["COMMUNITY"]]["total_population"]))
   
   merged_data = compute_crime_per_capita(community_areas)
   for index, row in merged_data.iterrows():
      row = [
         row["the_geom"],
         row["AREA_NUMBE"],
         row["COMMUNITY"],
         row["total_violent_crimes"],
         row["total_nonviolent_crimes"],
         row["total_population"],
         row["total_crimes"],
         row["violent_crime_rate"],
         row["nonviolent_crime_rate"],
         row["crime_rate"],
         row["crime_percentile"]
         
      ]
      insert_community_area(row)
      
   print(community_areas.head())
   return community_areas

def process_crime_rates():
   with tempfile.NamedTemporaryFile(mode="w", delete=False, newline='') as tmp_file:
      writer=csv.writer(tmp_file)
      with open("api/utils/data/crime_rates.csv", "r") as file: 
         reader = csv.reader(file)
         header=next(reader)
         # Write a new header that matches table columns
         writer.writerow([
             "crime_id", "case_number", "date", "block", "iucr", "primary_type",
             "description", "location_description", "arrest", "domestic",
             "beat", "district", "ward", "community_area", "fbi_code",
             "x_coordinate", "y_coordinate", "year", "updated_on",
             "latitude", "longitude", "location"
         ])
         
         for row in reader:
            cleaned_row = [
                parse_int(row[0]), # Crime ID
                row[1] or None, # Case Number
                parse_datetime(row[2]), # Date
               #  row[3] or None, # Block 
                row[4] or None, # IUCR 
                row[5] or None, # Primary Type
               #  row[6] or None, # Description
               #  row[7] or None, # Location Description
                parse_bool(row[8]), # Arrest
                parse_bool(row[9]), # Domestic
               #  parse_int(row[10]), # Beat
               #  parse_int(row[11]), # District
               #  parse_int(row[12]), # Ward
                parse_int(row[13]), # Community Area
                row[14] or None, # FBI Code
               #  parse_float(row[15]), # X-Coordinate
               #  parse_float(row[16]), # Y-Coordinate
                parse_int(row[17]), # Year
               #  parse_datetime(row[18]), # Updated On
                parse_float(row[19]), # Latitude
                parse_float(row[20]), # Longitude 
               #  row[21] or None # Location
            ]
            writer.writerow(cleaned_row)
            # print(cleaned_row)
            # break
   db_url = get_db_url()
   conn = psycopg2.connect(db_url)
   cur = conn.cursor()
   start = time.perf_counter()
   with open(tmp_file.name, 'r') as f: 
      cur.copy_expert(
         f"""COPY crimerates (
    crime_id, case_number, date, iucr, primary_type, arrest, 
    domestic, community_area, fbi_code, year, latitude, longitude
) FROM STDIN WITH CSV HEADER;""",
         f
      )
   conn.commit()
   end = time.perf_counter()

   after_count = get_row_count(conn, "crimerates")
   print(f'INSERTED {after_count} into crimerates in {(end-start):.2f} seconds.')
   cur.close()
   conn.close()


         # for row in reader: 
         #    insert_crime(row)
            # break
def compute_crime_per_capita(community_areas):
   crimes = pd.read_csv("api/utils/data/crime_rates.csv")
   print(crimes.head())
   # Drop rows without a community area
   crimes = crimes[crimes['Community Area'].notna()]
   crimes['Community Area'] = crimes['Community Area'].astype(int)
   
   # Violent Crimes 
   violent_counts = (
      crimes[crimes["Primary Type"].isin(VIOLENT_CRIMES)]
      .groupby("Community Area")
      .size()
      .reset_index(name="total_violent_crimes")
   )

   # Non-Violent Crimes
   nonviolent_counts = (
      crimes[crimes["Primary Type"].isin(NONVIOLENT_CRIMES)]
      .groupby("Community Area")
      .size()
      .reset_index(name="total_nonviolent_crimes")
   )

   # Group by community area
   crime_counts = (
      crimes.groupby('Community Area')
      .size()
      .reset_index(name="total_crimes")
   )
   # Merge crime counts with violent and nonviolent crime counts
   all_counts = pd.merge(crime_counts, violent_counts, on="Community Area", how="left")
   all_counts = pd.merge(all_counts, nonviolent_counts, on="Community Area", how="left")
   # Merge with community areas table with the total population information
   all_counts = all_counts.rename(columns={"Community Area": "AREA_NUMBE"})
   merged = all_counts.merge(community_areas, on="AREA_NUMBE")
   # Calculate Crime Rate per 100000
   merged["crime_rate"] = merged["total_crimes"] / merged["total_population"] * 100000
   # Calculate Violent Crime Rate per 100000
   merged["violent_crime_rate"] = merged["total_violent_crimes"] / merged["total_population"] * 100000
   # Calculate Non-violent Crime Rate per 100000
   merged["nonviolent_crime_rate"] = merged["total_nonviolent_crimes"] / merged["total_population"] * 100000

   # The lower the percentile, the safer the neighborhood is compared to its peers
   merged["crime_percentile"] = merged["crime_rate"].rank(pct=True)
   print(merged.head())   
   return merged

def insert_community_area(data: list):
   # the_geom,AREA_NUMBE,COMMUNITY,AREA_NUM_1,SHAPE_AREA,SHAPE_LEN
   community_area = CommunityAreas(
      area_id=int(data[1]), 
      the_geom=from_shape(load_wkt(data[0]), srid=4326),
      name=data[2], 
      total_violent_crimes=int(data[3]),
      total_nonviolent_crimes=float(data[4]),
      total_population=data[5],
      total_crimes=data[6],
      crime_rate=data[7],
      violent_crime_rate=data[8],
      nonviolent_crime_rate=data[9],
      crime_percentile=data[10]
      )
   with get_session() as session:
      session.add(community_area)
      session.commit()
      session.refresh(community_area)
      print(f"Community {community_area.name} added with ID: {community_area.id}")
   pass

def insert_crime(data: list):
   crime = CrimeRates(
      crime_id=parse_int(data[0]),
      case_number=data[1] or None, 
      date=parse_datetime(data[2]),
      # block=data[3] or None,
      iucr=data[4] or None,
      primary_type=data[5] or None,
      # description=data[6] or None,
      # location_description=data[7] or None,
      arrest=parse_bool(data[8]),
      domestic=parse_bool(data[9]),
      # beat=parse_int(data[10]),
      # district=parse_int(data[11]),
      # ward=parse_int(data[12]),
      community_area=parse_int(data[13]),
      fbi_code=data[14] or None,
      x_coordinate=parse_float(data[15]),
      y_coordinate=parse_float(data[16]),
      year=parse_int(data[17]),
      latitude=parse_float(data[19]),
      longitude=parse_float(data[20]),
      # location=data[21] or None,
      # updated_on=parse_datetime(data[18])
   )

   with get_session() as session:
       session.add(crime)
       session.commit()
       session.refresh(crime)
       print(f"Inserted Crime ID: {crime.id}")
   pass
create_db_and_tables()
process_community_area()
process_crime_rates()