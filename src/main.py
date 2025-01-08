from fastapi import FastAPI
from db.database import engine
from db.models import Base
from routers import items
import httpx

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(items.router)

#Connect to RaspberryPi
@app.get("/fetch-data")
def fetch_data():
    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:8000/data")
        return {"response": response.json()}