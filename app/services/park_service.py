from typing import List
from sqlalchemy.orm import Session
from app.repositories.park_repository import ParkRepository


class ParkService:
    @staticmethod
    def list_parks(db: Session) -> List[dict]:
        parks = ParkRepository.list_parks(db)
        return [
            {
                "name": park.name,
                "address": park.address or "",
                "rating": float(park.rating) if park.rating is not None else 0.0,
                "distance": "N/A",
                "features": [feature.name for feature in park.features]
            }
            for park in parks
        ]
