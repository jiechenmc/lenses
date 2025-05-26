from ..utils.db_config import get_session
from ..models.db_models import CrimeRates, CommunityAreas
from collections import defaultdict
from sqlalchemy import text
import time

# List of violent crimes
VIOLENT_CRIMES = {
    "ARSON", 
    "ASSAULT", 
    "BATTERY", 
    "CRIMINAL SEXUAL ASSAULT", 
    "CRIMINAL TRESPASS", 
    "HOMICIDE", 
    "HUMAN TRAFFICKING", 
    "INTIMIDATION", 
    "KIDNAPPING", 
    "MOTOR VEHICLE THEFT", 
    "ROBBERY", 
    "SEX OFFENSE", 
    "STALKING", 
    "THEFT", 
    "WEAPONS VIOLATION"
}

# List of non-violent crimes
NON_VIOLENT_CRIMES = {
    "CONCEALED CARRY LICENSE VIOLATION", 
    "DECEPTIVE PRACTICE", 
    "GAMBLING", 
    "LIQUOR LAW VIOLATION", 
    "NARCOTICS", 
    "NON-CRIMINAL", 
    "OBSCENITY", 
    "OFFENSE INVOLVING CHILDREN", 
    "OTHER NARCOTIC VIOLATION", 
    "OTHER OFFENSE", 
    "PROSTITUTION", 
    "PUBLIC INDECENCY", 
    "PUBLIC PEACE VIOLATION", 
    "RITUALISM"
}

class Insights: 
    def __init__(self, address:str):
        self.address = address
        self.crime_rate = self.compute_crime_rate_per_capita(9)
        self.commute = self.get_commute()
        self.schools = self.get_schools() 
        self.convenient_stores = self.get_convenient_stores()
        pass
    def compute_crime_rate_per_capita(self, community_area):
        # Returns a safety score of the requested community area. The lower the score, the less safe an area is. 
        start = time.perf_counter()
        with get_session() as session:
            crimes=session.exec(text(f"SELECT * FROM crimerates WHERE crimerates.community_area={community_area}"))
            community=session.exec(text(f"SELECT * FROM communityareas WHERE communityareas.area_id={community_area}"))
        end = time.perf_counter()

        print(f"Time to execute query for crimerates: {(end-start)} seconds")
        for point in community: 
            total_pop = point.total_population
        print(f"Total Population: {total_pop}")
        stats = defaultdict(lambda: {
            "violent": 0, 
            "non_violent": 0, 
            "arrests": 0,
            "total": 0
        })

        for crime in crimes: 
            area = crime.community_area
            if not area: 
                continue
            is_violent = crime.primary_type in VIOLENT_CRIMES
            stats[area]["total"]+=1
            if is_violent: 
                stats[area]["violent"]+=1
            else: 
                stats[area]["non_violent"]+=1
            stats[area]["arrests"]+= (1 if crime.arrest else 0)
        print(stats)

        for area, counts in stats.items(): 
            crime_rate = counts['total'] / total_pop * 100000 # Crime Rate per capilta
            # score = (
            #     100
            #     - 0.02 * violent_rate
            #     - 0.005 * non_violent_rate
            #     + 25 * arrest_rate
            # )
            print(f"Crime Rate per Capita for {community_area} is {crime_rate}")

            # score = max(0, min(100, score))
            # print(f"Score for {community_area} out of 100 is {score}")
            return crime_rate

        pass
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
    
insights = Insights("")