#!/usr/bin/env python3
"""
Script simplificado para crear datos de ejercicio como JSON.
Si la BD tiene problemas, usa este como mock data para el frontend.
"""

import json
from pathlib import Path

# Datos de ejercicios organizados por tipo/grupo corporal
EXERCISES_DATA = {
    "piernas": [
        {"nombre": "Sentadillas", "descripcion": "Ejercicio fundamental para piernas. Fortalece cuádriceps, glúteos y pantorrillas.", "imagen": "https://via.placeholder.com/300x200?text=Sentadillas&bg=3498db"},
        {"nombre": "Estocadas", "descripcion": "Alternancia de piernas para balance y fuerza unilateral.", "imagen": "https://via.placeholder.com/300x200?text=Estocadas&bg=3498db"},
        {"nombre": "Extensiones de pierna", "descripcion": "Aislamiento de cuádriceps. Excelente para rehab.", "imagen": "https://via.placeholder.com/300x200?text=Extensiones&bg=3498db"},
        {"nombre": "Curl de pierna", "descripcion": "Trabaja isquiotibiales y flexores de cadera.", "imagen": "https://via.placeholder.com/300x200?text=Curl+Pierna&bg=3498db"},
        {"nombre": "Prensa de pierna", "descripcion": "Máquina para cuádriceps, glúteos y pantorrillas.", "imagen": "https://via.placeholder.com/300x200?text=Prensa&bg=3498db"},
        {"nombre": "Levantamiento de pantorrillas", "descripcion": "Trabaja específicamente los músculos de la pantorrilla.", "imagen": "https://via.placeholder.com/300x200?text=Pantorrillas&bg=3498db"},
        {"nombre": "Zancadas con salto", "descripcion": "Ejercicio pliométrico para potencia en piernas.", "imagen": "https://via.placeholder.com/300x200?text=Zancadas+Salto&bg=3498db"},
        {"nombre": "Puente de glúteos", "descripcion": "Aislamiento específico de glúteos y cadena posterior.", "imagen": "https://via.placeholder.com/300x200?text=Puente&bg=3498db"},
        {"nombre": "Sentadilla búlgara", "descripcion": "Profunda, unilateral, excelente para fuerza.", "imagen": "https://via.placeholder.com/300x200?text=Sentadilla+Bulgara&bg=3498db"},
        {"nombre": "Sentadilla sissy", "descripcion": "Aislamiento extremo de cuádriceps.", "imagen": "https://via.placeholder.com/300x200?text=Sissy&bg=3498db"},
        {"nombre": "Leg press inclinado", "descripcion": "Variante de prensa con ángulo.", "imagen": "https://via.placeholder.com/300x200?text=Leg+Press&bg=3498db"},
        {"nombre": "Saltos al cajón", "descripcion": "Pliometría explosiva para potencia.", "imagen": "https://via.placeholder.com/300x200?text=Saltos+Cajon&bg=3498db"},
        {"nombre": "Step ups", "descripcion": "Subidas a plataforma elevada.", "imagen": "https://via.placeholder.com/300x200?text=Step+Ups&bg=3498db"},
        {"nombre": "Hip thrust", "descripcion": "Activación máxima de glúteos.", "imagen": "https://via.placeholder.com/300x200?text=Hip+Thrust&bg=3498db"},
        {"nombre": "Sentadilla goblet", "descripcion": "Con peso sostenido al pecho.", "imagen": "https://via.placeholder.com/300x200?text=Goblet&bg=3498db"},
        {"nombre": "Abducción de cadera", "descripcion": "Trabaja glúteo medio y lateral.", "imagen": "https://via.placeholder.com/300x200?text=Abduccion&bg=3498db"},
        {"nombre": "Aducción de cadera", "descripcion": "Interno de muslo y aductores.", "imagen": "https://via.placeholder.com/300x200?text=Aduccion&bg=3498db"},
        {"nombre": "Burpees", "descripcion": "Ejercicio full-body explosivo.", "imagen": "https://via.placeholder.com/300x200?text=Burpees&bg=3498db"},
        {"nombre": "Mountain climbers", "descripcion": "Dinámico, cardio con trabajo de core.", "imagen": "https://via.placeholder.com/300x200?text=Mountain+Climbers&bg=3498db"},
        {"nombre": "Patada trasera", "descripcion": "Activación de glúteos e isquiotibiales.", "imagen": "https://via.placeholder.com/300x200?text=Patada+Trasera&bg=3498db"},
    ],
    "brazos": [
        {"nombre": "Flexiones", "descripcion": "Clásico ejercicio de peso corporal. Pecho, hombros y tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Flexiones&bg=e74c3c"},
        {"nombre": "Curl de bíceps", "descripcion": "Aislamiento de bíceps con mancuerna o barra.", "imagen": "https://via.placeholder.com/300x200?text=Curl+Biceps&bg=e74c3c"},
        {"nombre": "Extensión de tríceps", "descripcion": "Aislamiento de tríceps en todas sus cabezas.", "imagen": "https://via.placeholder.com/300x200?text=Triceps&bg=e74c3c"},
        {"nombre": "Fondos", "descripcion": "Peso corporal para pecho y tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Fondos&bg=e74c3c"},
        {"nombre": "Dominadas", "descripcion": "Máximo aislamiento de espalda y bíceps.", "imagen": "https://via.placeholder.com/300x200?text=Dominadas&bg=e74c3c"},
        {"nombre": "Poleas altas", "descripcion": "Aislamiento de bíceps y espalda alta.", "imagen": "https://via.placeholder.com/300x200?text=Poleas+Altas&bg=e74c3c"},
        {"nombre": "Press francés", "descripcion": "Aislamiento total de tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Press+Frances&bg=e74c3c"},
        {"nombre": "Curl martillo", "descripcion": "Trabaja bíceps y braquial anterior.", "imagen": "https://via.placeholder.com/300x200?text=Curl+Martillo&bg=e74c3c"},
        {"nombre": "Curl concentrado", "descripcion": "Aislamiento extremo del bíceps.", "imagen": "https://via.placeholder.com/300x200?text=Curl+Concentrado&bg=e74c3c"},
        {"nombre": "Extensión por encima", "descripcion": "Máxima contracción de tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Ext+Encima&bg=e74c3c"},
        {"nombre": "Fondos en banco", "descripcion": "Peso corporal modificado para tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Fondos+Banco&bg=e74c3c"},
        {"nombre": "Curl con barra Z", "descripcion": "Variante ergonómica de curl.", "imagen": "https://via.placeholder.com/300x200?text=Barra+Z&bg=e74c3c"},
        {"nombre": "Flexiones diamante", "descripcion": "Énfasis en tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Flexiones+Diamante&bg=e74c3c"},
        {"nombre": "Dominada inversa", "descripcion": "Espalda baja con énfasis en bíceps.", "imagen": "https://via.placeholder.com/300x200?text=Dominada+Inversa&bg=e74c3c"},
        {"nombre": "Bandas de resistencia", "descripcion": "Flexibilidad para bíceps y tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Bandas&bg=e74c3c"},
        {"nombre": "Cable curls", "descripcion": "Tensión constante en el bíceps.", "imagen": "https://via.placeholder.com/300x200?text=Cable+Curls&bg=e74c3c"},
        {"nombre": "Patada de tríceps", "descripcion": "Aislamiento con cable o banda.", "imagen": "https://via.placeholder.com/300x200?text=Patada+Triceps&bg=e74c3c"},
        {"nombre": "Curl alterno", "descripcion": "Alternancia de brazos con mancuernas.", "imagen": "https://via.placeholder.com/300x200?text=Curl+Alterno&bg=e74c3c"},
        {"nombre": "Fondos asistidos", "descripcion": "Máquina para fondos sin peso corporal.", "imagen": "https://via.placeholder.com/300x200?text=Fondos+Asistidos&bg=e74c3c"},
        {"nombre": "Ejercicio EZ bar", "descripcion": "Con barra rizada para menor tensión de muñeca.", "imagen": "https://via.placeholder.com/300x200?text=EZ+Bar&bg=e74c3c"},
    ],
    "pecho": [
        {"nombre": "Press de banca", "descripcion": "Rey del pecho. Trabajo de pecho, hombros y tríceps.", "imagen": "https://via.placeholder.com/300x200?text=Press+Banca&bg=f39c12"},
        {"nombre": "Press inclinado", "descripcion": "Énfasis en pecho superior.", "imagen": "https://via.placeholder.com/300x200?text=Press+Inclinado&bg=f39c12"},
        {"nombre": "Press declinado", "descripcion": "Énfasis en pecho inferior.", "imagen": "https://via.placeholder.com/300x200?text=Press+Declinado&bg=f39c12"},
        {"nombre": "Aperturas de pecho", "descripcion": "Aislamiento puro del pecho.", "imagen": "https://via.placeholder.com/300x200?text=Aperturas&bg=f39c12"},
        {"nombre": "Aperturas inclinadas", "descripcion": "Aperturas para el pecho superior.", "imagen": "https://via.placeholder.com/300x200?text=Aperturas+Inc&bg=f39c12"},
        {"nombre": "Press con mancuernas", "descripcion": "Mayor rango de movimiento que barra.", "imagen": "https://via.placeholder.com/300x200?text=Press+Mancuernas&bg=f39c12"},
        {"nombre": "Máquina de pecho", "descripcion": "Máquina guiada para pecho.", "imagen": "https://via.placeholder.com/300x200?text=Maquina+Pecho&bg=f39c12"},
        {"nombre": "Flexiones inclinadas", "descripcion": "Flexión con manos elevadas.", "imagen": "https://via.placeholder.com/300x200?text=Flexiones+Inc&bg=f39c12"},
        {"nombre": "Flexiones declinadas", "descripcion": "Flexión con pies elevados.", "imagen": "https://via.placeholder.com/300x200?text=Flexiones+Dec&bg=f39c12"},
        {"nombre": "Cable crossover", "descripcion": "Aislamiento de pecho con cables.", "imagen": "https://via.placeholder.com/300x200?text=Cable+Crossover&bg=f39c12"},
        {"nombre": "Peck deck", "descripcion": "Máquina específica de pecho.", "imagen": "https://via.placeholder.com/300x200?text=Peck+Deck&bg=f39c12"},
        {"nombre": "Push ups agresivos", "descripcion": "Flexiones explosivas con aplausos.", "imagen": "https://via.placeholder.com/300x200?text=Push+Ups+Agresivos&bg=f39c12"},
        {"nombre": "Prensa Smith", "descripcion": "Barra guiada para pecho.", "imagen": "https://via.placeholder.com/300x200?text=Smith+Prensa&bg=f39c12"},
        {"nombre": "Fondos pecho", "descripcion": "Fondos con inclinación hacia adelante.", "imagen": "https://via.placeholder.com/300x200?text=Fondos+Pecho&bg=f39c12"},
        {"nombre": "Aperturas con polea baja", "descripcion": "Aislamiento de pecho inferior.", "imagen": "https://via.placeholder.com/300x200?text=Polea+Baja&bg=f39c12"},
        {"nombre": "Press máquina 45°", "descripcion": "Máquina con angulación.", "imagen": "https://via.placeholder.com/300x200?text=Maq+45&bg=f39c12"},
        {"nombre": "Flexiones laterales", "descripcion": "Énfasis en pecho interno.", "imagen": "https://via.placeholder.com/300x200?text=Flexiones+Laterales&bg=f39c12"},
        {"nombre": "Dips en paralelas", "descripcion": "Peso corporal profundo.", "imagen": "https://via.placeholder.com/300x200?text=Dips+Paralelas&bg=f39c12"},
        {"nombre": "Aperturas con banda", "descripcion": "Resistencia variable.", "imagen": "https://via.placeholder.com/300x200?text=Banda+Aperturas&bg=f39c12"},
        {"nombre": "Gravedad negativa", "descripcion": "Trabajo excéntrico del pecho.", "imagen": "https://via.placeholder.com/300x200?text=Gravedad+Negativa&bg=f39c12"},
    ],
    "cardio": [
        {"nombre": "Correr", "descripcion": "Cardio clásico al aire libre o treadmill.", "imagen": "https://via.placeholder.com/300x200?text=Correr&bg=27ae60"},
        {"nombre": "Caminar rápido", "descripcion": "Cardio de bajo impacto.", "imagen": "https://via.placeholder.com/300x200?text=Caminar&bg=27ae60"},
        {"nombre": "Natación", "descripcion": "Cardio total con bajo impacto.", "imagen": "https://via.placeholder.com/300x200?text=Natacion&bg=27ae60"},
        {"nombre": "Bicicleta estática", "descripcion": "Cardio sentado de bajo impacto.", "imagen": "https://via.placeholder.com/300x200?text=Bici+Estatica&bg=27ae60"},
        {"nombre": "Bicicleta al aire libre", "descripcion": "Cardio activo con variación de terreno.", "imagen": "https://via.placeholder.com/300x200?text=Bici+Outdoor&bg=27ae60"},
        {"nombre": "Elíptica", "descripcion": "Cardio de bajo impacto para todo el cuerpo.", "imagen": "https://via.placeholder.com/300x200?text=Eliptica&bg=27ae60"},
        {"nombre": "Remo", "descripcion": "Máquina o actividad acuática.", "imagen": "https://via.placeholder.com/300x200?text=Remo&bg=27ae60"},
        {"nombre": "HIIT", "descripcion": "Entrenamiento de alta intensidad en intervalos.", "imagen": "https://via.placeholder.com/300x200?text=HIIT&bg=27ae60"},
        {"nombre": "Saltar cuerda", "descripcion": "Cardio explosivo y coordinación.", "imagen": "https://via.placeholder.com/300x200?text=Cuerda&bg=27ae60"},
        {"nombre": "Burpees", "descripcion": "Cardio explosivo full-body.", "imagen": "https://via.placeholder.com/300x200?text=Burpees&bg=27ae60"},
        {"nombre": "Escaladora", "descripcion": "Cardio con énfasis en piernas.", "imagen": "https://via.placeholder.com/300x200?text=Escaladora&bg=27ae60"},
        {"nombre": "Jump squats", "descripcion": "Sentadillas explosivas.", "imagen": "https://via.placeholder.com/300x200?text=Jump+Squats&bg=27ae60"},
        {"nombre": "Mountain climbers", "descripcion": "Dinámico para cardio y core.", "imagen": "https://via.placeholder.com/300x200?text=Mountain&bg=27ae60"},
        {"nombre": "Boxeo", "descripcion": "Cardio con coordinación y poder.", "imagen": "https://via.placeholder.com/300x200?text=Boxeo&bg=27ae60"},
        {"nombre": "Entrenador elíptico cruzado", "descripcion": "Máquina de cardio versátil.", "imagen": "https://via.placeholder.com/300x200?text=Eliptico+Cruzado&bg=27ae60"},
        {"nombre": "Escalera aeróbica", "descripcion": "Máquina de escaleras.", "imagen": "https://via.placeholder.com/300x200?text=Escalera&bg=27ae60"},
        {"nombre": "Sprint", "descripcion": "Corrida explosiva a máxima velocidad.", "imagen": "https://via.placeholder.com/300x200?text=Sprint&bg=27ae60"},
        {"nombre": "Trote", "descripcion": "Cardio moderado constante.", "imagen": "https://via.placeholder.com/300x200?text=Trote&bg=27ae60"},
        {"nombre": "Zumba", "descripcion": "Cardio divertido con ritmo.", "imagen": "https://via.placeholder.com/300x200?text=Zumba&bg=27ae60"},
        {"nombre": "Kickboxing", "descripcion": "Cardio de artes marciales.", "imagen": "https://via.placeholder.com/300x200?text=Kickboxing&bg=27ae60"},
    ]
}

def main():
    """Crear ejercicios como JSON para mock data."""
    
    # Preparar datos
    all_exercises = []
    for tipo, ejercicios in EXERCISES_DATA.items():
        for idx, ejercicio in enumerate(ejercicios, 1):
            all_exercises.append({
                "id": len(all_exercises) + 1,
                "nombre": ejercicio["nombre"],
                "tipo": tipo,
                "descripcion": ejercicio["descripcion"],
                "imagen": ejercicio["imagen"],
                "parque": "Gym"
            })
    
    # Guardar como JSON   
    output_path = Path("exercises.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_exercises, f, indent=2, ensure_ascii=False)
    
    print("✓ Tabla de ejercicios preparada")
    
    # Estadísticas
    total = len(all_exercises)
    print(f"\n✅ Total: {total} ejercicios creados exitosamente")
    print("\nDistribución:")
    for tipo in EXERCISES_DATA:
        count = len(EXERCISES_DATA[tipo])
        print(f"  • {tipo.upper()}: {count} ejercicios")
    
    print(f"\n📁 Archivo guardado: {output_path.absolute()}")
    print("\n💡 Para usar en el backend:")
    print("   1. Copia los datos e inserta en la base de datos")
    print("   2. O usa como mock data para desarrollo")

if __name__ == "__main__":
    main()

