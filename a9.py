import json
import random

# =========================
# Nombres y apellidos
# =========================
nombres = [
    "Ana", "Luis", "Carlos", "María", "Pedro", "Sofía", "Juan", "Lucía",
    "José", "Daniel", "Andrés", "Miguel", "Fernando", "Jorge", "Ricardo",
    "Paola", "Diana", "Valeria", "Gabriela", "Camila",
    "Bryan", "Kevin", "Cristian", "Jonathan", "Steven", "Alex",
    "Natalia", "Andrea", "Karla", "Melissa"
]

apellidos = [
    "Pérez", "Gómez", "Torres", "Vargas", "Mendoza", "Ramos",
    "Rodríguez", "Martínez", "López", "García", "Sánchez", "Castro",
    "Morales", "Ortega", "Flores", "Chávez", "Cedeño", "Zambrano",
    "Macías", "Intriago", "Alvarado", "Ponce", "Bravo", "Salazar",
    "Molina", "Reyes"
]

# =========================
# Cédula ecuatoriana válida
# =========================
def generar_cedula_ecuador():
    provincia = random.randint(1, 24)
    base = f"{provincia:02d}" + "".join(str(random.randint(0, 9)) for _ in range(7))
    coef = [2, 1] * 4 + [2]
    total = 0

    for i in range(9):
        v = int(base[i]) * coef[i]
        total += v - 9 if v >= 10 else v

    digito = (10 - (total % 10)) % 10
    return base + str(digito)

def prob(p):
    return random.random() < p

# =========================
# Generar aspirantes
# =========================
aspirantes = []
cedulas = set()

while len(aspirantes) < 100:
    cedula = generar_cedula_ecuador()
    if cedula in cedulas:
        continue

    cedulas.add(cedula)
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)

    aspirante = {
        "cedula": cedula,
        "nombre": f"{nombre} {apellido}",
        "edad": random.randint(16, 25),

        # Cupos / historial
        "cupo_aceptado_historico_pc": prob(0.3),
        "anulacion_matricula_niv_carr": prob(0.1),
        "periodo_sancion_anul_niv_carr": "2023-2" if prob(0.1) else None,
        "obs_anulacion_matricu_niv_carr": "Anulación por inasistencia" if prob(0.1) else None,
        "cupo_historico_activo": prob(0.4),
        "numero_cupos_activos": random.randint(0, 2),
        "cupo_pendiente_registro": prob(0.2),
        "observacion_cupo_pendiente_reg": "Pendiente de documentos" if prob(0.2) else None,

        # Evaluación
        "aspirante_focalizado": prob(0.3),
        "tiene_puntaje_eval_4_ult_periodos": prob(0.7),
        "puntaje_mayor_eval_4_ult_periodos": random.randint(600, 1000),

        # Condiciones
        "bachiller_artes": prob(0.05),
        "condicion_socioeconomica": prob(0.2),
        "ruralidad": prob(0.25),
        "territorialidad": prob(0.2),
        "discapacidad": prob(0.05),
        "bono_jgl": prob(0.07),
        "victima_violencia": prob(0.05),
        "migrantes_retornados": prob(0.04),
        "femicidio": prob(0.01),
        "enfermedades_catastroficas": prob(0.03),
        "casa_acogida": prob(0.02),
        "pueblos_nacionalidades": prob(0.15),
        "vulnerabilidad_socioeconomica": prob(0.2),

        # Mérito académico
        "merito_academico": prob(0.1),
        "bachiller_pueblos_nacionalidad": prob(0.12),
        "bachiller_periodo_academico": True,

        # Clasificación
        "poblacion_general": True
    }

    aspirantes.append(aspirante)

# =========================
# Guardar JSON
# =========================
with open("aspirantes_universidad.json", "w", encoding="utf-8") as f:
    json.dump(aspirantes, f, indent=4, ensure_ascii=False)

print("Archivo aspirantes_universidad.json generado correctamente ✅")

