from fastapi import FastAPI
import uvicorn
from db.database import engine
from db.models import Base
from routers import items

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(items.router_meals)
app.include_router(items.router_orders)
app.include_router(items.router_user)

@app.get("/data")
def get_data():
    return {"message": "Hello"}
    
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
