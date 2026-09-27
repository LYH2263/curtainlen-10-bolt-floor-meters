from fastapi import APIRouter, HTTPException
from app.repositories import fabrics as repo
from app.schemas.fabric import FabricUpdateRequest
router = APIRouter()
@router.get("/fabrics")
def list_fabrics(): return {"items": repo.list_fabrics()}
@router.get("/fabrics/{fid}")
def get_fabric(fid: int):
    r = repo.get_fabric(fid)
    if not r: raise HTTPException(404)
    return r
@router.patch("/fabrics/{fid}")
def update_fabric(fid: int, body: FabricUpdateRequest):
    if body.min_order_m <= 0:
        raise HTTPException(422, "min_order_m must be positive")
    if not repo.update_min_order(fid, body.min_order_m):
        raise HTTPException(404)
    return repo.get_fabric(fid)
