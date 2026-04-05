from typing import List

class ParkService:
    @staticmethod
    def list_parks() -> List[dict]:
        return [
            {"name": "Parque Central de la Ciudad", "address": "Av. Principal 123", "rating": 4.5, "distance": "0.8 km", "features": ["Senderos", "Área de ejercicio", "Baños", "Bancas"]},
            {"name": "Plaza del Sol", "address": "Calle 45 y 12", "rating": 4.2, "distance": "1.2 km", "features": ["Gimnasio al aire libre", "Fuente de agua", "Iluminación"]},
            {"name": "Jardines del Río", "address": "Calle Río 78", "rating": 4.6, "distance": "1.9 km", "features": ["Circuito cardiovascular", "Zona de descanso"]}
        ]
