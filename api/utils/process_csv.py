import csv
from ..utils.db_config import create_db_and_tables, get_session, get_db_url
from ..models.db_models import *
from ..utils.string_utils import *
import tempfile
import psycopg2
import os
import time

def get_row_count(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        return cur.fetchone()[0]
    
# Processes the community area CSV and crime rates CSV
def process_community_area(): 
   print(os.getcwd())
   with open("api/utils/data/community_areas.csv", "r") as file: 
      reader = csv.reader(file)
      next(reader)
      for row in reader: 
         insert_community_area(row)
         # break

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
                parse_int(row[0]),
                row[1] or None,
                parse_datetime(row[2]),
                row[3] or None,
                row[4] or None,
                row[5] or None,
                row[6] or None,
                row[7] or None,
                parse_bool(row[8]),
                parse_bool(row[9]),
                parse_int(row[10]),
                parse_int(row[11]),
                parse_int(row[12]),
                parse_int(row[13]),
                row[14] or None,
                parse_float(row[15]),
                parse_float(row[16]),
                parse_int(row[17]),
                parse_datetime(row[18]),
                parse_float(row[19]),
                parse_float(row[20]),
                row[21] or None
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
    crime_id, case_number, date, block, iucr, primary_type,
    description, location_description, arrest, domestic,
    beat, district, ward, community_area, fbi_code,
    x_coordinate, y_coordinate, year, updated_on,
    latitude, longitude, location
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

def insert_community_area(data: list):
   # the_geom,AREA_NUMBE,COMMUNITY,AREA_NUM_1,SHAPE_AREA,SHAPE_LEN
   community_area = CommunityAreas(area_id=int(data[1]), name=data[2])
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
      block=data[3] or None,
      iucr=data[4] or None,
      primary_type=data[5] or None,
      description=data[6] or None,
      location_description=data[7] or None,
      arrest=parse_bool(data[8]),
      domestic=parse_bool(data[9]),
      beat=parse_int(data[10]),
      district=parse_int(data[11]),
      ward=parse_int(data[12]),
      community_area=parse_int(data[13]),
      fbi_code=data[14] or None,
      x_coordinate=parse_float(data[15]),
      y_coordinate=parse_float(data[16]),
      year=parse_int(data[17]),
      latitude=parse_float(data[19]),
      longitude=parse_float(data[20]),
      location=data[21] or None,
      updated_on=parse_datetime(data[18])
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