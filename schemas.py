from pydantic import BaseModel, field_validator, ConfigDict, conint, constr
from typing import Optional

class VehicleBase(BaseModel):
    manufacturer: constr(min_length=1)
    description: Optional[str] = None
    horse_power: conint(ge=0)
    model_name: constr(min_length=1)
    model_year: conint(ge=1886)
    purchase_price: float
    fuel_type: constr(min_length=1)

    model_config = ConfigDict(from_attributes=True)

    @field_validator('purchase_price')
    @classmethod
    def price_non_negative(cls, v):
        if v < 0:
            raise ValueError('purchase_price must be non-negative')
        return v

class VehicleCreate(VehicleBase):
    vin: constr(min_length=1)

class VehicleUpdate(BaseModel):
    manufacturer: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    horse_power: Optional[conint(ge=0)] = None
    model_name: Optional[constr(min_length=1)] = None
    model_year: Optional[conint(ge=1886)] = None
    purchase_price: Optional[float] = None
    fuel_type: Optional[constr(min_length=1)] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('purchase_price')
    @classmethod
    def price_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('purchase_price must be non-negative')
        return v

class VehicleResponse(VehicleBase):
    vin: str
