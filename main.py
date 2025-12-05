from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List
from database import get_db, init_db
from schemas import VehicleCreate, VehicleResponse, VehicleUpdate

init_db()  # ensure DB exists

app = FastAPI(title="Vehicle Service (SQLite)")

# ---------------- Exception Handlers ----------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# ---------------- CRUD Endpoints ----------------
@app.get("/vehicle", response_model=List[VehicleResponse])
def list_vehicles(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("""
        SELECT vin, manufacturer, description, horse_power, model_name, model_year, purchase_price, fuel_type 
        FROM vehicles
    """)
    rows = cur.fetchall()
    return [
        {
            "vin": r[0],
            "manufacturer": r[1],
            "description": r[2],
            "horse_power": r[3],
            "model_name": r[4],
            "model_year": r[5],
            "purchase_price": r[6],
            "fuel_type": r[7],
        } for r in rows
    ]

@app.post("/vehicle", status_code=201, response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db=Depends(get_db)):
    cur = db.cursor()
    vin_upper = vehicle.vin.upper()
    cur.execute("SELECT vin FROM vehicles WHERE UPPER(vin)=?", (vin_upper,))
    if cur.fetchone():
        raise HTTPException(status_code=422, detail="VIN already exists")
    
    cur.execute("""
        INSERT INTO vehicles (vin, manufacturer, description, horse_power, model_name, model_year, purchase_price, fuel_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (vin_upper, vehicle.manufacturer, vehicle.description, vehicle.horse_power,
          vehicle.model_name, vehicle.model_year, vehicle.purchase_price, vehicle.fuel_type))
    db.commit()
    
    return {**vehicle.model_dump(), "vin": vin_upper}

@app.get("/vehicle/{vin}", response_model=VehicleResponse)
def get_vehicle(vin: str, db=Depends(get_db)):
    cur = db.cursor()
    vin_upper = vin.upper()
    cur.execute("""
        SELECT vin, manufacturer, description, horse_power, model_name, model_year, purchase_price, fuel_type 
        FROM vehicles WHERE UPPER(vin)=?
    """, (vin_upper,))
    r = cur.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {
        "vin": r[0],
        "manufacturer": r[1],
        "description": r[2],
        "horse_power": r[3],
        "model_name": r[4],
        "model_year": r[5],
        "purchase_price": r[6],
        "fuel_type": r[7],
    }

@app.put("/vehicle/{vin}", response_model=VehicleResponse)
def update_vehicle(vin: str, vehicle: VehicleUpdate, db=Depends(get_db)):
    cur = db.cursor()
    vin_upper = vin.upper()
    
    cur.execute("SELECT vin FROM vehicles WHERE UPPER(vin)=?", (vin_upper,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    data = vehicle.model_dump(exclude_unset=True)
    if not data:
        return get_vehicle(vin_upper, db)
    
    columns = ", ".join(f"{k}=?" for k in data.keys())
    values = tuple(data.values()) + (vin_upper,)
    
    cur.execute(f"UPDATE vehicles SET {columns} WHERE UPPER(vin)=?", values)
    db.commit()
    
    return get_vehicle(vin_upper, db)

@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db=Depends(get_db)):
    cur = db.cursor()
    vin_upper = vin.upper()
    
    cur.execute("SELECT vin FROM vehicles WHERE UPPER(vin)=?", (vin_upper,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    cur.execute("DELETE FROM vehicles WHERE UPPER(vin)=?", (vin_upper,))
    db.commit()
    
    return JSONResponse(status_code=204, content=None)
