from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root(): 
    return {"message": "Hello World"}

@app.get("/api/get_insight")
async def get_insight():
    # Takes in an address 
    return {"message": "Hello World"}

# Given an address, compute the safety score
@app.get("/api/get_safety_score")
async def get_safety_score():
    return {"message": "Safety Score Route"}

@app.get("/api/get_commute")
async def get_commute():
    return {"message": "Commute Route"}

@app.get("/api/get_schools")
async def get_schools():
    return {"message": "Schools Route"}

@app.get("/api/get_convenience_stores")
async def get_convenience_stores():
    return {"message": "Convenience Stores Route"}