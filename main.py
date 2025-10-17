from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
import uvicorn
import os
import json

load_dotenv()


app = FastAPI()


data = [
    {"name": "sam larry", "age": 20, "track": "AI Developer"},
    {"name": "Boladele", "age": 50, "track": "AI Developer"},
    {"name": "sam Loco", "age": 70, "track": "AI Engineer"}
]
class Item(BaseModel):  # Example Pydantic model
    name: str = Field(..., example="Ayyub Raji")
    age: int = Field(..., example=25)
    track: str = Field(..., example="AI Engineer")


# Optional data  for patch request
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    track: Optional[str] = None
    

@app.get("/")
def root():
    return {"Message": "Welcome to my FastAPI Application"}



# Example POST endpoint using the Pydantic model
@app.post("/create-data/")
def create_data(req: Item):
    data.append(req.model_dump())
    return {"message": "Item created", "item": data}



@app.put("/update-data/{id}")
def create_data(id: int, req: Item):
    data[id] = req.model_dump()

    return {"message": "Item created", "item": data}


@app.patch("/patch-data/{id}")
def create_data(id: int, req: ItemUpdate):
    data[id].update(req.model_dump(exclude_unset=True))
    return {"message": "Item created", "item": data}


@app.delete("/delete-data/{id}")
def create_data(id: int):
    data.remove(data[id])
    
    return {"message": "Item created", "item": data}



if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=os.getenv("HOST"), 
        port=int(os.getenv("PORT"))   
    )