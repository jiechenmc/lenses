from fastapi import FastAPI, HTTPException
from models.insights import Insights

app = FastAPI()


@app.get("/")
async def root(): 
    return {"message": "Hello World"}

@app.get("/api/get_insight")
async def get_insight():
    # Takes in an address 
    return {"message": "Hello World"}

# Given an address, compute the safety score
@app.get("/api/get_safety_score/")
async def get_safety_score(address: str):
    community, community_id = Insights.get_community_area(address)
    if not community_id:
        raise HTTPException(status_code=404, detail="Invalid address or community area not found.")
    safety_score = Insights.get_crime_percentile(community_id)
    return {
        "address": address,
        "community_area": community,
        "safety_score": safety_score
    }

@app.get("/api/get_commute")
async def get_commute():
    return {"message": "Commute Route"}

@app.get("/api/get_schools")
async def get_schools():
    return {"message": "Schools Route"}

@app.get("/api/get_convenience_stores")
async def get_convenience_stores():
    return {"message": "Convenience Stores Route"}