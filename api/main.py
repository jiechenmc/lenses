from fastapi import FastAPI, HTTPException
from models.insights import Insights
from fastapi.middleware.cors import CORSMiddleware

description = """
Lenses API makes real estate search easier! 
"""
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app = FastAPI(
    title="Lenses API",
    description=description,
    summary="Lenses: Real Estate's Best Friend",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World Latest"}


@app.get("/api/get_insight")
async def get_insight():
    # Takes in an address
    return {"message": "Hello World"}


# Given an address, compute the safety score
@app.get("/api/get_safety_score/")
async def get_safety_score(address: str):
    community, community_id = Insights.get_community_area(address)
    if not community_id:
        raise HTTPException(
            status_code=404, detail="Invalid address or community area not found."
        )
    safety_score = Insights.get_crime_percentile(community_id)
    return {
        "address": address,
        "community_area": community,
        "safety_score": safety_score,
    }


@app.get("/api/get_commute/")
async def get_commute(origin: str, destination: str, mode: str = "drive"):
    print(f"Origin: {origin}, Destination: {destination}")
    modes = ["drive", "walk", "bicycle", "transit"]
    if mode not in modes:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode of transportation. Choose from: drive, walk, bicycle, transit.",
        )
    # Calculate commute time and distance
    commute_info = Insights.get_commute(origin, destination, mode)
    if not commute_info:
        raise HTTPException(
            status_code=500, detail="Failed to compute commute information."
        )
    return {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "distance_meters": commute_info["distanceMeters"],
        "duration": commute_info["duration"],
    }


@app.get("/api/get_schools")
async def get_schools():
    return {"message": "Schools Route"}


@app.get("/api/get_convenience_stores")
async def get_convenience_stores():
    return {"message": "Convenience Stores Route"}
