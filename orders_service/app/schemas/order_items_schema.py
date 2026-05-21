import enum
from typing import Optional
from pydantic import BaseModel, Field

class GuitarType(str, enum.Enum):
    ELECTRIC = "электрогитара"
    ACOUSTIC = "акустическая гитара"
    CLASSICAL = "классическая гитара"
    BASS = "бас гитара"

class PickupConfig(str, enum.Enum):
    SSS = "SSS"
    HH = "HH"
    HSS = "HSS"
    HSH = "HSH"
    SS = "SS"
    P90 = "P90"
    PIEZO = "piezo"
    NONE = "none"

class OrderItemCreate(BaseModel):
    product_id: int
    sku: str
    title: str
    brand: str
    price: float
    quantity: int = Field(1, ge=1)

    type: GuitarType
    body_wood: str
    neck_wood: str
    fretboard_wood: str
    fret_count: int
    scale_length: float
    pickup_config: PickupConfig
    image_url: Optional[str] = None

class OrderItem(OrderItemCreate):
    id: int
    model_config = {"from_attributes": True}