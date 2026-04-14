from sqlalchemy.orm import Session
from app.models.park import Park


class ParkRepository:
    @staticmethod
    def list_parks(db: Session) -> list[Park]:
        return db.query(Park).order_by(Park.name).all()

    @staticmethod
    def get_park(db: Session, park_id: int) -> Park | None:
        return db.query(Park).filter(Park.id == park_id).first()

    @staticmethod
    def create_park(db: Session, name: str, address: str | None, rating: float | None) -> Park:
        park = Park(name=name, address=address, rating=rating)
        db.add(park)
        db.commit()
        db.refresh(park)
        return park

    @staticmethod
    def update_park(db: Session, park_id: int, name: str | None, address: str | None, rating: float | None) -> Park | None:
        park = db.query(Park).filter(Park.id == park_id).first()
        if not park:
            return None
        if name:
            park.name = name
        if address:
            park.address = address
        if rating is not None:
            park.rating = rating
        db.commit()
        db.refresh(park)
        return park

    @staticmethod
    def delete_park(db: Session, park_id: int) -> bool:
        park = db.query(Park).filter(Park.id == park_id).first()
        if not park:
            return False
        db.delete(park)
        db.commit()
        return True
