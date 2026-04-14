from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.park_service import ParkService
from app.schemas.park import ParkResponse, ParkCreate, ParkUpdate
from app.db import get_db

router = APIRouter()

@router.get('/', response_model=list[ParkResponse])
def get_parks(db: Session = Depends(get_db)):
    return ParkService.list_parks(db)

@router.post('/', response_model=ParkResponse)
def create_park(payload: ParkCreate, db: Session = Depends(get_db)):
    try:
        if not payload.name:
            raise HTTPException(status_code=400, detail='El nombre del parque es obligatorio')
        park = ParkService.create_park(db, payload.name, payload.address, payload.rating)
        db.commit()
        return park
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.get('/{park_id}', response_model=ParkResponse)
def get_park(park_id: int, db: Session = Depends(get_db)):
    park = ParkService.get_park(db, park_id)
    if not park:
        raise HTTPException(status_code=404, detail='Parque no encontrado')
    return park

@router.put('/{park_id}', response_model=ParkResponse)
def update_park(park_id: int, payload: ParkUpdate, db: Session = Depends(get_db)):
    try:
        park = ParkService.update_park(db, park_id, payload.name, payload.address, payload.rating)
        if not park:
            raise HTTPException(status_code=404, detail='Parque no encontrado')
        db.commit()
        return park
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))

@router.delete('/{park_id}')
def delete_park(park_id: int, db: Session = Depends(get_db)):
    try:
        success = ParkService.delete_park(db, park_id)
        if not success:
            raise HTTPException(status_code=404, detail='Parque no encontrado')
        db.commit()
        return {"message": "Parque eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
