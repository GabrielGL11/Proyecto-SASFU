import random
import json

#Ejemplo de Facultades
facultades = [
    "Ingeniería, Industria y Arquitectura",
    "Ciencias Sociales, Derecho y Bienestar",
    "Educación, Turismo y Humanidades",
    "Ciencias de la Salud",
    "Ciencias de la Vida y Tecnologías",
    "Ciencias Administrativas, Contables y Comercio"
]

#Matrizes con nombre de las ciudades 
matrices = ["Manta", "Chone", "Sucre", "El Carmen", "Pedernales",
            "Pichincha", "Flavio Alfaro", "Santo Domingo", "Tosagua"]

#Horarios fijos para la prueba
horarios = ["08:00-10:00", "11:00-13:00", "14:00-16:00", "17:00-19:00"]

#Probabilidades para matrices donde Manta tiene mas posibilidad
pesos = [50] + [7] * (len(matrices) - 1)  # Manta 50%, otras 7% cada una

#Lista que guaeda los horarios de evaluacion 
ofertas_generadas = []

codigo_oferta = 200

for facultad in facultades:#Cada facultad tiene tres bloque
    for bloque_num, horario in zip(range(1, 4), horarios[:3]):  # bloque 1,2,3 con horarios fijos
        matrices_elegidas = random.choices(matrices, weights=pesos, k=6)
        for matriz in matrices_elegidas:#Se genera de manera aleatoria los horarios
            cupos = random.randint(30, 40)
            oferta = {
                "facultad": facultad,
                "bloque": bloque_num,
                "horario": horario,
                "matriz": matriz,
                "cantidad": cupos,
                "codigo": codigo_oferta
            }
            ofertas_generadas.append(oferta)
            codigo_oferta += 1

#Se guarda en Json
with open("horarios_evaluacion.json", "w", encoding="utf-8") as f:
    json.dump(ofertas_generadas, f, indent=4, ensure_ascii=False)
print(f"Bloques de facultad generados correctamente ✅ Total ofertas: {len(ofertas_generadas)}")
