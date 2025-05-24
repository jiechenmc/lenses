class Insights: 
    def __init__(self, address:str):
        self.address = address
        self.crime_rate = self.get_crime_rate()
        self.commute = self.get_commute()
        self.schools = self.get_schools() 
        self.convenient_stores = self.get_convenient_stores()
        pass
    def get_crime_rate(self): 
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