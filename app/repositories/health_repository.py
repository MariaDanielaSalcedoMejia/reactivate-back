from sqlalchemy.orm import Session
from app.models.health import HealthProfile

class HealthRepository:
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> HealthProfile | None:
        return db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()

    @staticmethod
    def create_or_update(db: Session, user_id: int, height_cm: float, weight_kg: float, resting_hr: int, imc: float, score: int, level: str, recommendation: str) -> HealthProfile:
        profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
        if profile is None:
            profile = HealthProfile(
                user_id=user_id,
                height_cm=height_cm,
                weight_kg=weight_kg,
                resting_hr=resting_hr,
                imc=imc,
                score=score,
                level=level,
                recommendation=recommendation
            )
            db.add(profile)
        else:
            profile.height_cm = height_cm
            profile.weight_kg = weight_kg
            profile.resting_hr = resting_hr
            profile.imc = imc
            profile.score = score
            profile.level = level
            profile.recommendation = recommendation
        db.commit()
        db.refresh(profile)
        return profile
