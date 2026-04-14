from datetime import date
from sqlalchemy.orm import Session
from app.repositories.health_repository import HealthRepository
from app.repositories.health_analysis_repository import HealthAnalysisRepository
from app.repositories.user_repository import UserRepository
from app.models.health import HealthProfile
from app.models.health_analysis import HealthAnalysis
import json


class HealthService:
    @staticmethod
    def calculate_age_from_birth_date(birth_date: date | None) -> int | None:
        """Calcula la edad a partir de la fecha de nacimiento"""
        if not birth_date:
            return None
        from datetime import date as date_class
        today = date_class.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    @staticmethod
    def calculate_metrics(height_cm: float, weight_kg: float, resting_hr: int, age: int | None = None) -> tuple[float, int, str, str]:
        """Calcula métricas de salud básicas"""
        height_m = height_cm / 100.0
        imc = weight_kg / (height_m * height_m)
        score = 100

        # Penalización por IMC
        if imc < 18.5 or imc > 30:
            score -= 30
        elif imc > 25:
            score -= 15

        # Penalización por frecuencia cardíaca
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
    def get_imc_category(imc: float) -> str:
        """Obtiene la categoría de IMC"""
        if imc < 18.5:
            return 'Bajo peso'
        elif imc < 25:
            return 'Óptimo'
        elif imc < 30:
            return 'Sobrepeso'
        else:
            return 'Obesidad'

    @staticmethod
    def calculate_heart_zones(age: int | None, resting_hr: int) -> dict:
        """Calcula las zonas de frecuencia cardíaca para ejercicio"""
        if not age:
            return {}
        
        max_hr = 220 - age
        heart_reserve = max_hr - resting_hr
        
        zones = {
            'max_hr': max_hr,
            'heart_reserve': heart_reserve,
            'recovery': {
                'min': int(resting_hr + heart_reserve * 0.5),
                'max': int(resting_hr + heart_reserve * 0.6),
                'percentage': 50
            },
            'aerobic': {
                'min': int(resting_hr + heart_reserve * 0.6),
                'max': int(resting_hr + heart_reserve * 0.7),
                'percentage': 65
            },
            'performance': {
                'min': int(resting_hr + heart_reserve * 0.7),
                'max': int(resting_hr + heart_reserve * 0.85),
                'percentage': 80
            }
        }
        return zones

    @staticmethod
    def generate_health_summary(imc: float, score: int, resting_hr: int, age: int | None) -> str:
        """Genera un resumen de conclusiones"""
        lines = []
        
        # Conclusión sobre IMC
        imc_category = HealthService.get_imc_category(imc)
        if imc_category == 'Optimal':
            lines.append("✓ Tu índice de masa corporal está en el rango óptimo (18.5-25).")
        elif imc_category == 'Sobrepeso':
            lines.append("⚠️ Tienes sobrepeso. Considera aumentar actividad física y revisar tu dieta.")
        elif imc_category == 'Bajo peso':
            lines.append("⚠️ Tienes bajo peso. Consulta con un nutricionista para un plan alimentario.")
        else:
            lines.append("⚠️ Tu IMC está en rango de obesidad. Te recomendamos buscar asesoría profesional.")
        
        # Conclusión sobre frecuencia cardíaca
        if resting_hr < 60:
            lines.append("✓ Excelente capacidad cardiovascular. Tu frecuencia cardíaca en reposo es muy baja.")
        elif resting_hr <= 80:
            lines.append("✓ Tu frecuencia cardíaca en reposo es saludable.")
        else:
            lines.append("⚠️ Tu frecuencia cardíaca en reposo es elevada. Aumenta tu actividad aeróbica.")
        
        # Conclusión sobre score general
        if score >= 85:
            lines.append("🔥 Tu estado físico general es excelente. Mantén estos hábitos.")
        elif score >= 70:
            lines.append("💪 Tu estado es bueno. Con más consistencia en el ejercicio mejorarás.")
        elif score >= 50:
            lines.append("⚡ Tu estado es mejorable. Diseña un plan estructurado de ejercicio.")
        else:
            lines.append("⚠️ Tu estado requiere atención. Comienza con ejercicio suave y consistente.")
        
        return "\n".join(lines)

    @staticmethod
    def generate_warnings(imc: float, resting_hr: int) -> list[str]:
        """Genera alertas importantes"""
        warnings = []
        
        if imc > 30:
            warnings.append("Peso: Riesgo de problemas de salud relacionados con obesidad")
        elif imc < 18.5:
            warnings.append("Peso: Bajo peso puede indicar desnutrición")
        
        if resting_hr > 100:
            warnings.append("Frecuencia cardíaca: Muy elevada, consulta a un médico")
        
        return warnings

    @staticmethod
    def generate_suggestions(imc: float, score: int, resting_hr: int) -> list[str]:
        """Genera sugerencias de mejora"""
        suggestions = []
        
        # Sugerencias de ejercicio
        if score < 70:
            if resting_hr > 80:
                suggestions.append("Realiza actividad cardiovascular 150 minutos por semana")
            if imc > 25:
                suggestions.append("Incorpora ejercicio de fuerza 2-3 veces por semana")
        
        # Sugerencias de nutrición
        if imc > 25:
            suggestions.append("Revisa tu ingesta calórica y aumenta el consumo de proteína")
        
        suggestions.append("Duerme 7-9 horas por noche para mejor recuperación")
        suggestions.append("Mantén sesiones de análisis mensual para monitorear tu progreso")
        
        return suggestions

    @staticmethod
    def create_or_update_profile(
        db: Session,
        user_id: int,
        height_cm: float,
        weight_kg: float,
        resting_hr: int,
        age: int | None = None
    ) -> HealthProfile:
        """Crea o actualiza el perfil principal, y también crea un análisis en el historial
        
        Gestiona la transacción completa - se debe hacer commit desde el controlador
        """
        try:
            # Obtener usuario para la edad si no se proporciona
            if age is None:
                user = UserRepository.get_by_id(db, user_id) if hasattr(UserRepository, 'get_by_id') else None
                if user and user.birth_date:
                    age = HealthService.calculate_age_from_birth_date(user.birth_date)
            
            # Calcular métricas
            imc, score, level, recommendation = HealthService.calculate_metrics(height_cm, weight_kg, resting_hr, age)
            
            # Actualizar perfil principal (no hace commit)
            profile = HealthRepository.create_or_update(
                db, user_id, height_cm, weight_kg, resting_hr, imc, score, level, recommendation
            )
            
            # Crear análisis en el historial (no hace commit)
            imc_category = HealthService.get_imc_category(imc)
            heart_zones = HealthService.calculate_heart_zones(age, resting_hr)
            health_summary = HealthService.generate_health_summary(imc, score, resting_hr, age)
            warnings = HealthService.generate_warnings(imc, resting_hr)
            suggestions = HealthService.generate_suggestions(imc, score, resting_hr)
            
            analysis = HealthAnalysisRepository.create_analysis(
                db,
                user_id=user_id,
                height_cm=height_cm,
                weight_kg=weight_kg,
                resting_hr=resting_hr,
                age=age,
                imc=imc,
                imc_category=imc_category,
                score=score,
                level=level,
                recommendation=recommendation,
                max_hr=heart_zones.get('max_hr'),
                heart_reserve=heart_zones.get('heart_reserve'),
                recovery_zone_min=heart_zones.get('recovery', {}).get('min'),
                recovery_zone_max=heart_zones.get('recovery', {}).get('max'),
                aerobic_zone_min=heart_zones.get('aerobic', {}).get('min'),
                aerobic_zone_max=heart_zones.get('aerobic', {}).get('max'),
                performance_zone_min=heart_zones.get('performance', {}).get('min'),
                performance_zone_max=heart_zones.get('performance', {}).get('max'),
                health_summary=health_summary,
                warnings=json.dumps(warnings),
                suggestions=json.dumps(suggestions)
            )
            
            # Make sure objects are properly attached to session
            db.flush()
            
            return profile
            
        except Exception as e:
            # Log error but don't commit - let caller handle rollback
            print(f"Error in create_or_update_profile: {e}")
            raise

    @staticmethod
    def get_profile(db: Session, user_id: int) -> HealthProfile | None:
        return HealthRepository.get_by_user(db, user_id)

    @staticmethod
    def delete_profile(db: Session, user_id: int) -> bool:
        return HealthRepository.delete_profile(db, user_id)

    @staticmethod
    def get_analysis_history(db: Session, user_id: int) -> list[HealthAnalysis]:
        """Obtiene el historial de análisis del usuario"""
        return HealthAnalysisRepository.get_by_user(db, user_id)

    @staticmethod
    def get_analysis_by_id(db: Session, analysis_id: int) -> HealthAnalysis | None:
        """Obtiene un análisis específico"""
        return HealthAnalysisRepository.get_by_id(db, analysis_id)

