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

    @staticmethod
    def get_park(db: Session, park_id: int) -> dict | None:
        park = ParkRepository.get_park(db, park_id)
        if not park:
            return None
        return {
            "name": park.name,
            "address": park.address or "",
            "rating": float(park.rating) if park.rating is not None else 0.0,
            "distance": "N/A",
            "features": [feature.name for feature in park.features]
        }

    @staticmethod
    def create_park(db: Session, name: str, address: str | None, rating: float | None) -> dict:
        park = ParkRepository.create_park(db, name, address, rating)
        return {
            "name": park.name,
            "address": park.address or "",
            "rating": float(park.rating) if park.rating is not None else 0.0,
            "distance": "N/A",
            "features": []
        }

    @staticmethod
    def update_park(db: Session, park_id: int, name: str | None, address: str | None, rating: float | None) -> dict | None:
        park = ParkRepository.update_park(db, park_id, name, address, rating)
        if not park:
            return None
        return {
            "name": park.name,
            "address": park.address or "",
            "rating": float(park.rating) if park.rating is not None else 0.0,
            "distance": "N/A",
            "features": [feature.name for feature in park.features]
        }

    @staticmethod
    def delete_park(db: Session, park_id: int) -> bool:
        return ParkRepository.delete_park(db, park_id)
