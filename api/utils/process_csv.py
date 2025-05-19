import csv
from ..utils.db_config import create_db_and_tables, get_session
from ..models.db_models import *
from ..utils.string_utils import *
import os
# Processes the community area CSV and crime rates CSV
def process_community_area(): 
   print(os.getcwd())
   with open("api/utils/data/community_areas.csv", "r") as file: 
      reader = csv.reader(file)
      next(reader)
      for row in reader: 
         insert_community_area(row)
         break

def process_crime_rates():
   with open("api/utils/data/crime_rates.csv", "r") as file: 
      reader = csv.reader(file)
      print(next(reader))
      for row in reader: 
         insert_crime(row)
         break

def insert_community_area(data: list):
   # the_geom,AREA_NUMBE,COMMUNITY,AREA_NUM_1,SHAPE_AREA,SHAPE_LEN
   community_area = CommunityAreas(area_id=int(data[1]), name=data[2])
   with get_session as session:
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
# process_community_area()
# create_db_and_tables()
# process_crime_rates()