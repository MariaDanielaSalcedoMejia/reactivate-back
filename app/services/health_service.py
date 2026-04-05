from sqlalchemy.orm import Session
from app.repositories.health_repository import HealthRepository
from app.models.health import HealthProfile

class HealthService:
    @staticmethod
    def calculate_metrics(height_cm: float, weight_kg: float, resting_hr: int) -> tuple[float, int, str, str]:
        height_m = height_cm / 100.0
        imc = weight_kg / (height_m * height_m)
        score = 100

        if imc < 18.5 or imc > 30:
            score -= 30
        elif imc > 25:
            score -= 15

        if resting_hr > 80:
            score -= 30
        elif resting_hr > 70:
            score -= 15

        score = max(0, score)

        if score >= 85:
            level = 'Atleta 🔥'
            recommendation = 'Estás en un nivel excelente. Mantén tu rutina y cuida la recuperación.'
        elif score >= 70:
            level = 'Buen nivel 💪'
            recommendation = 'Buen estado físico. Puedes mejorar con entrenamientos más estructurados.'
        elif score >= 50:
            level = 'Mejorable ⚡'
            recommendation = 'Necesitas mejorar resistencia y composición corporal.'
        else:
            level = 'Bajo rendimiento ⚠️'
            recommendation = 'Enfócate en hábitos básicos: descanso, alimentación y ejercicio progresivo.'

        return round(imc, 2), score, level, recommendation

    @staticmethod
    def create_or_update_profile(db: Session, user_id: int, height_cm: float, weight_kg: float, resting_hr: int) -> HealthProfile:
        imc, score, level, recommendation = HealthService.calculate_metrics(height_cm, weight_kg, resting_hr)
        return HealthRepository.create_or_update(db, user_id, height_cm, weight_kg, resting_hr, imc, score, level, recommendation)

    @staticmethod
    def get_profile(db: Session, user_id: int) -> HealthProfile | None:
        return HealthRepository.get_by_user(db, user_id)
