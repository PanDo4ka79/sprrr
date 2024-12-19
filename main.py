from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from db_manager import DBManager
from pass_data import PassData

class PassData(BaseModel):
    name: str
    description: str
app = FastAPI()

db_manager = DBManager()

@app.post("/submitData")
def submit_data(pass_data: PassData):
    try:
        query = """
        INSERT INTO passes (name, location, height, status)
        VALUES (%s, %s, %s, 'new') RETURNING id;
        """
        params = (pass_data.name, pass_data.location, pass_data.height)
        db_manager.execute_query(query, params)
        return {"message": "Pass added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/submitData/{id}")
async def get_pass_by_id(id: int):
    pass_data = db_manager.get_pass_by_id(id)
    if pass_data:
        return pass_data
    return {"message": "Pass not found"}, 404

@app.patch("/submitData/{id}")
async def update_pass(id: int, pass_data: PassData):
    existing_pass = db_manager.get_pass_by_id(id)
    if not existing_pass:
        return {"state": 0, "message": "Pass not found"}

    if existing_pass["status"] != "new":
        return {"state": 0, "message": "Only passes with status 'new' can be updated"}

    success = db_manager.update_pass(id, pass_data)
    if success:
        return {"state": 1, "message": "Pass updated successfully"}
    return {"state": 0, "message": "Failed to update pass"}


@app.get("/submitData/")
async def get_passes_by_email(user__email: str):
    passes = db_manager.get_passes_by_email(user__email)
    return passes
