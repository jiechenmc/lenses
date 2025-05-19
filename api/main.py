from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root(): 
    return {"message": "Hello World"}

@app.get("/api/get_insight")
async def get_insight():
    # Takes in an address 
    return {"message": "Hello World"}