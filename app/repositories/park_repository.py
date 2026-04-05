from sqlalchemy.orm import Session
from app.models.park import Park


class ParkRepository:
    @staticmethod
    def list_parks(db: Session) -> list[Park]:
        return db.query(Park).order_by(Park.name).all()
