from typing import List

class ExerciseService:
    @staticmethod
    def list_exercises() -> List[dict]:
        return [
            {"nombre": "Sentadillas", "tipo": "piernas", "descripcion": "Fortalece piernas y glúteos", "imagen": "https://images.unsplash.com/photo-1599058917212-d750089bc07e", "parque": "Parque El Cortijo - zona de barras"},
            {"nombre": "Zancadas", "tipo": "piernas", "descripcion": "Equilibrio y fuerza", "imagen": "https://images.unsplash.com/photo-1594737625785-c0e7c1f1c0df", "parque": "Parque El Cortijo - zona funcional"},
            {"nombre": "Step-up", "tipo": "piernas", "descripcion": "Subidas controladas", "imagen": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438", "parque": "Parque El Cortijo - escaleras"},
            {"nombre": "Curl bíceps", "tipo": "brazos", "descripcion": "Trabajo de bíceps", "imagen": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61", "parque": "Parque El Cortijo - máquinas superiores"},
            {"nombre": "Fondos en banca", "tipo": "brazos", "descripcion": "Tríceps y fuerza", "imagen": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b", "parque": "Parque El Cortijo - bancas"},
            {"nombre": "Dominadas asistidas", "tipo": "brazos", "descripcion": "Espalda y brazos", "imagen": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5", "parque": "Parque El Cortijo - barras"},
            {"nombre": "Flexiones", "tipo": "pecho", "descripcion": "Pecho y core", "imagen": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b", "parque": "Parque El Cortijo - zona funcional"},
            {"nombre": "Flexiones inclinadas", "tipo": "pecho", "descripcion": "Menor carga", "imagen": "https://images.unsplash.com/photo-1599058917212-d750089bc07e", "parque": "Parque El Cortijo - bancas"},
            {"nombre": "Caminata rápida", "tipo": "cardio", "descripcion": "Resistencia básica", "imagen": "https://images.unsplash.com/photo-1558611848-73f7eb4001a1", "parque": "Parque El Cortijo - senderos"},
            {"nombre": "Trote suave", "tipo": "cardio", "descripcion": "Mejora cardiovascular", "imagen": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8", "parque": "Parque El Cortijo - pista"}
        ]
