import json
import random
from datetime import datetime, timedelta

# =========================
# Nombres por sexo
# =========================
nombres_hombre = [
    "Luis", "Carlos", "Pedro", "Juan", "José", "Daniel", "Andrés",
    "Miguel", "Fernando", "Jorge", "Ricardo", "Rafael", "Diego",
    "Bryan", "Kevin", "Cristian", "Jonathan", "Steven", "Alex", "Samuel"
]

nombres_mujer = [
    "Ana", "María", "Sofía", "Lucía", "Paola", "Diana", "Valeria",
    "Gabriela", "Camila", "Natalia", "Andrea", "Karla", "Melissa",
    "Isabel", "Carolina", "Verónica"
]

apellidos = [
    "Pérez", "Gómez", "Torres", "Vargas", "Mendoza", "Ramos",
    "Rodríguez", "Martínez", "López", "García", "Sánchez", "Castro",
    "Morales", "Ortega", "Flores", "Chávez", "Cedeño", "Zambrano",
    "Macías", "Intriago", "Alvarado", "Ponce", "Bravo", "Salazar",
    "Molina", "Reyes", "Cruz", "Vega", "Navarro", "Silva", "Díaz",
]

# =========================
# Países extranjeros
# =========================
paises_extranjeros = {
    "BRA": {"pais": "Brasil", "nacionalidad": "BRASILEÑO", "codigo": 55},
    "ARG": {"pais": "Argentina", "nacionalidad": "ARGENTINO", "codigo": 54},
    "COL": {"pais": "Colombia", "nacionalidad": "COLOMBIANO", "codigo": 57},
    "PER": {"pais": "Perú", "nacionalidad": "PERUANO", "codigo": 51},
    "VEN": {"pais": "Venezuela", "nacionalidad": "VENEZOLANO", "codigo": 58},
    "CHI": {"pais": "Chile", "nacionalidad": "CHILENO", "codigo": 56},
    "MEX": {"pais": "México", "nacionalidad": "MEXICANO", "codigo": 52},
    "ESP": {"pais": "España", "nacionalidad": "ESPAÑOL", "codigo": 34},
    "PAN": {"pais": "Panamá", "nacionalidad": "PANAMEÑO", "codigo": 507},
}

# =========================
# Provincias de Ecuador
# =========================
provincias_ec = {
    "01": "Azuay",
    "02": "Bolívar",
    "03": "Cañar",
    "04": "Carchi",
    "05": "Cotopaxi",
    "06": "Chimborazo",
    "07": "El Oro",
    "08": "Esmeraldas",
    "09": "Guayas",
    "10": "Imbabura",
    "11": "Loja",
    "12": "Los Ríos",
    "13": "Manabí",
    "14": "Morona Santiago",
    "15": "Napo",
    "16": "Pastaza",
    "17": "Pichincha",
    "18": "Tungurahua",
    "19": "Zamora Chinchipe",
    "20": "Galápagos",
    "21": "Sucumbíos",
    "22": "Orellana",
    "23": "Santo Domingo de los Tsáchilas",
    "24": "Santa Elena"
}

# =========================
# Funciones auxiliares
# =========================
def prob(p):
    return random.random() < p

def fecha_nacimiento_desde_edad(edad):
    hoy = datetime.now()
    return (hoy - timedelta(days=edad * 365)).strftime("%d/%m/%Y")

def fecha_registro():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def celular_ecuador():
    return "09" + "".join(str(random.randint(0, 9)) for _ in range(8))

def correo(nombre, apellido):
    dominios = ["gmail.com", "hotmail.com", "outlook.com"]
    return f"{nombre.lower()}.{apellido.lower()}@{random.choice(dominios)}"

# =========================
# Cédula / Pasaporte
# =========================
def generar_cedula_ecuador():
    provincia_codigo = f"{random.randint(1, 24):02d}"
    base = provincia_codigo + "".join(str(random.randint(0, 9)) for _ in range(7))
    coef = [2, 1] * 4 + [2]
    total = 0
    for i in range(9):
        v = int(base[i]) * coef[i]
        total += v - 9 if v >= 10 else v
    digito = (10 - (total % 10)) % 10
    cedula = base + str(digito)
    provincia = provincias_ec.get(provincia_codigo)
    return cedula, provincia

def generar_pasaporte(codigo_pais):
    return f"{codigo_pais}-" + "".join(str(random.randint(0, 9)) for _ in range(7))

# =========================
# Catálogos
# =========================
estados_civiles = ["S", "C", "U", "D", "V", "N"]

etnias = {
    127: "Afroecuatoriana/o",
    130: "Blanca/o",
    126: "Indígena",
    129: "Mestiza/o",
    128: "Montubia/o",
    132: "Mulata/o",
    131: "Negra/o",
    133: "Otro/a",
}

sostenimiento_ue = ["Fiscal", "Particular", "Fiscomisional", "Municipal"]

# =========================
# Generar aspirantes
# =========================
aspirantes = []
ids = set()

while len(aspirantes) < 100:

    # Sexo coherente con nombre
    sexo = random.choice(["HOMBRE", "MUJER"])
    if sexo == "HOMBRE":
        nombre = random.choice(nombres_hombre)
        codigo_genero = 124
        identidad_genero = "Masculino"
    else:
        nombre = random.choice(nombres_mujer)
        codigo_genero = 125
        identidad_genero = "Femenino"

    apellido = random.choice(apellidos)
    edad = random.randint(17, 30)
    codigo_etnia = random.choice(list(etnias.keys()))
    es_ecuatoriano = random.random() < 0.9

    if es_ecuatoriano:
        identificacion, provincia = generar_cedula_ecuador()
        tipo_documento = "CEDULA"
        codigo_nacionalidad = 1
        pais_origen = "Ecuador"
        nacionalidad = "ECUATORIANO"
        celular = celular_ecuador()
    else:
        cod = random.choice(list(paises_extranjeros.keys()))
        pais = paises_extranjeros[cod]
        identificacion = generar_pasaporte(cod)
        tipo_documento = "PASAPORTE"
        codigo_nacionalidad = pais["codigo"]
        pais_origen = pais["pais"]
        nacionalidad = pais["nacionalidad"]
        celular = None
        provincia = None  
    if identificacion in ids:
        continue
    ids.add(identificacion)

    # Datos personales
    aspirante = {
        "tipo_documento": tipo_documento,
        "numero_identidad": identificacion,
        "nacionalidad": nacionalidad,
        "pais_origen": pais_origen,
        "codigo_nacionalidad": codigo_nacionalidad,
        "provincia": provincia,  
        "nombres": nombre,
        "apellidos": apellido,
        "sexo": sexo,
        "codigo_genero": codigo_genero,
        "identidad_genero": identidad_genero,
        "edad": edad,
        "fecha_nacimiento": fecha_nacimiento_desde_edad(edad),
        "estado_civil": random.choice(estados_civiles),
        "codigo_autoidentificacion_etnica": codigo_etnia,
        "autoidentificacion_etnica": etnias[codigo_etnia],
        "celular": celular,
        "correo": correo(nombre, apellido),

        # Académico
        "titulo_bachiller_homologado": "SI",
        "sostenimiento_ue": random.choice(sostenimiento_ue),
        "nota_grado": round(random.uniform(7.0, 10.0), 2),

        # Registro
        "fecha_registro_nacional": fecha_registro(),
        "estado_registro_nacional": random.choice(["Completo", "Incompleto"]),
        "estado_participacion_2025": random.choice(
            ["HABILITADO", "NO HABILITADO", "CONDICIONADO"]
        ),

        # Datos adicionales
        "cupo_aceptado_historico_pc": prob(0.3),
        "anulacion_matricula_niv_carr": prob(0.1),
        "periodo_sancion_anul_niv_carr": "2023-2" if prob(0.1) else None,
        "obs_anulacion_matricu_niv_carr": "Anulación por inasistencia" if prob(0.1) else None,
        "cupo_historico_activo": prob(0.4),
        "numero_cupos_activos": random.randint(0, 2),
        "cupo_pendiente_registro": prob(0.2),
        "observacion_cupo_pendiente_reg": "Pendiente de documentos" if prob(0.2) else None,

        "aspirante_focalizado": prob(0.3),
        "tiene_puntaje_eval_4_ult_periodos": prob(0.7),
        "puntaje_mayor_eval_4_ult_periodos": random.randint(600, 1000),

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

        "merito_academico": prob(0.1),
        "bachiller_pueblos_nacionalidad": prob(0.12),
        "bachiller_periodo_academico": True,
        "poblacion_general": True
    }

    aspirantes.append(aspirante)

# =========================
# Guardar JSON
# =========================
with open("aspirantes_universidad.json", "w", encoding="utf-8") as f:
    json.dump(aspirantes, f, indent=4, ensure_ascii=False)

print("Archivo aspirantes_universidad.json generado correctamente ✅")
