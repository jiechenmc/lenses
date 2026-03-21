from utils.db_config import get_session
from models.db_models import CrimeRates, CommunityAreas
from collections import defaultdict
from sqlalchemy import text
from geopy.geocoders import Nominatim
from geoalchemy2.shape import to_shape
from dotenv import load_dotenv
import os
import requests
import time
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
def geocode_address(address:str):
    # """Use Nominatim to geocode the address."""
    # geolocator = Nominatim(user_agent="chicago_mapper")
    # location = geolocator.geocode(address)
    """Calls the Google Geocoding API to get the latitude and longitude of an address.

    Args:
        address (str): Specified address to geocode.

    Returns:
        _type_: _description_
    """
    # Urlify the address for API request
    urlify_address = quote_plus(address)
    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={urlify_address}&key={google_api_key}")
    if response.status_code != 200: 
        return None
    data = response.json()
    if not data or "results" not in data or len(data["results"]) == 0: 
        return None
    location = data['results'][0]['geometry']['location']
    print(f"LOCATION: {location}, Longitude: {location['lng']}, Latitude: {location['lat']}")
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
        print(f"Longitude: {location['lng']}, Latitude: {location['lat']}")
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
            result = session.exec(query.bindparams(lon = location["lng"], lat = location["lat"])).first()
            if result:
                print(f"Location {location} is in {result}")
        return result
    
    def get_commute(origin: str, destination: str, mode: str):
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": google_api_key,
            "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
        }
        body = {
            "origin": {
                "address": origin
            }, 
            "destination": {
                "address": destination
            },
            "travelMode": mode.upper()
        }
        print(f"BODY: {body}")
        response = requests.post("https://routes.googleapis.com/directions/v2:computeRoutes", headers=headers, json=body)
        if response.status_code != 200:
            return None
        data = response.json()
        print(f"TEST: {data}")
        if "routes" not in data or len(data["routes"]) == 0:
            return None
        return data["routes"][0]
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
# Insights.get_community_area("1715 S Ruble St, Chicago, IL 60616")
# Insights.get_commute("1715 S Ruble St, Chicago, IL 60616", "1000 W 35th St, Chicago, IL 60609", "drive")