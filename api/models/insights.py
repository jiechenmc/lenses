from ..utils.db_config import get_session
from ..models.db_models import CrimeRates, CommunityAreas
from collections import defaultdict
from sqlalchemy import text
from geopy.geocoders import Nominatim
from geoalchemy2.shape import to_shape


import requests
import time

def geocode_address(address:str):
    """Use Nominatim to geocode the address."""
    geolocator = Nominatim(user_agent="chicago_mapper")
    location = geolocator.geocode(address)
    print(f"LOCATION: {location}, Longitude: {location.longitude}, Latitude: {location.latitude}")
    return location
# Temporary Location for this function - might be relocated later
def get_geojson(community_area): 
    stmt = text("""
        SELECT ST_AsGeoJSON(the_geom) AS geojson
        FROM communityareas
        WHERE name = :name
    """)    

    with get_session() as session:
        result = session.exec(stmt.bindparams(name=community_area)).first()
        if result:
            geojson_str = result.geojson  # This is a GeoJSON string
            print(geojson_str)
            return geojson_str
    return None

class Insights: 
    def __init__(self, address:str):
        self.address = address
        self.community_area, self.community_id = Insights.get_community_area(address)
        self.crime_percentile = Insights.get_crime_percentile(self.community_id)
        self.commute = self.get_commute()
        self.schools = self.get_schools() 
        self.convenient_stores = self.get_convenient_stores()
        pass
    def get_crime_percentile(community_area):
        # Returns a safety score of the requested community area. The lower the score, the less safe an area is. 
        start = time.perf_counter()
        with get_session() as session:
            community=session.exec(text(f"SELECT * FROM communityareas WHERE communityareas.area_id={community_area}")).first()
        end = time.perf_counter()
        print(f"Total time to execute query: {end-start} seconds.")
        print(community.crime_percentile)
        return community.crime_percentile
    
    def get_community_area(addr:str): 
        location = geocode_address(addr)
        print(f"Longitude: {location.longitude}, Latitude: {location.latitude}")
        query = text("""
        SELECT name, area_id
        FROM communityareas
        WHERE ST_Contains(
            the_geom,
            ST_SetSRID(ST_Point(:lon, :lat), 4326)
        )
        LIMIT 1;
        """)
        with get_session() as session:
            result = session.exec(query.bindparams(lon = location.longitude, lat = location.latitude)).first()
            if result:
                print(f"Location {location} is in {result}")
        return result
    
    def get_commute(self): 
        pass
    def get_schools(self):
        pass
    def get_convenient_stores(self): 
        pass

    def to_dict(self): 
        return {
            "address": self.address, 
            "crime_rate": self.crime_rate,
            "commute": self.commute, 
            "schools": self.schools, 
            "convenient_stores": self.convenient_stores
        }
    
# insights = Insights("")
Insights.get_community_area("1715 S Ruble St, Chicago, IL 60616")