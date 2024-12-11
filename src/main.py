from fastapi import FastAPI
from src.db.database import engine
from src.db.models import Base
from src.routers import items
import uvicorn

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)