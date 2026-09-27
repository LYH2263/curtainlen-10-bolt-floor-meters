from pydantic import BaseModel

class FabricUpdateRequest(BaseModel):
    min_order_m: float
