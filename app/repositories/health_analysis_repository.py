from datetime import datetime
from sqlalchemy.orm import Session
from app.models.health_analysis import HealthAnalysis
from sqlalchemy import desc


class HealthAnalysisRepository:
    @staticmethod
    def create_analysis(
        db: Session,
        user_id: int,
        height_cm: float,
        weight_kg: float,
        resting_hr: int,
        age: int | None,
        imc: float,
        imc_category: str,
        score: int,
        level: str,
        recommendation: str,
        max_hr: int | None = None,
        heart_reserve: int | None = None,
        recovery_zone_min: int | None = None,
        recovery_zone_max: int | None = None,
        aerobic_zone_min: int | None = None,
        aerobic_zone_max: int | None = None,
        performance_zone_min: int | None = None,
        performance_zone_max: int | None = None,
        health_summary: str | None = None,
        warnings: str | None = None,
        suggestions: str | None = None
    ) -> HealthAnalysis:
        """Crea un nuevo análisis de salud en el historial"""
        analysis = HealthAnalysis(
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
            max_hr=max_hr,
            heart_reserve=heart_reserve,
            recovery_zone_min=recovery_zone_min,
            recovery_zone_max=recovery_zone_max,
            aerobic_zone_min=aerobic_zone_min,
            aerobic_zone_max=aerobic_zone_max,
            performance_zone_min=performance_zone_min,
            performance_zone_max=performance_zone_max,
            health_summary=health_summary,
            warnings=warnings,
            suggestions=suggestions
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> list[HealthAnalysis]:
        """Obtiene todos los análisis de un usuario ordenados por fecha descendente"""
        return db.query(HealthAnalysis).filter(
            HealthAnalysis.user_id == user_id
        ).order_by(desc(HealthAnalysis.created_at)).all()

    @staticmethod
    def get_latest_by_user(db: Session, user_id: int) -> HealthAnalysis | None:
        """Obtiene el análisis más reciente de un usuario"""
        return db.query(HealthAnalysis).filter(
            HealthAnalysis.user_id == user_id
        ).order_by(desc(HealthAnalysis.created_at)).first()

    @staticmethod
    def get_by_id(db: Session, analysis_id: int) -> HealthAnalysis | None:
        """Obtiene un análisis específico por ID"""
        return db.query(HealthAnalysis).filter(HealthAnalysis.id == analysis_id).first()

    @staticmethod
    def delete_analysis(db: Session, analysis_id: int) -> bool:
        """Elimina un análisis específico"""
        analysis = db.query(HealthAnalysis).filter(HealthAnalysis.id == analysis_id).first()
        if not analysis:
            return False
        db.delete(analysis)
        db.commit()
        return True

    @staticmethod
    def get_analysis_count_by_user(db: Session, user_id: int) -> int:
        """Obtiene la cantidad de análisis realizados por un usuario"""
        return db.query(HealthAnalysis).filter(HealthAnalysis.user_id == user_id).count()
