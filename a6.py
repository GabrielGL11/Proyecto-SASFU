import json
import os

# Cargar datos de aspirantes desde el archivo JSON (ruta relativa al script)
def cargar_aspirantes():
    ruta = os.path.join(os.path.dirname(__file__), "aspirantes_universidad.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{ruta}'.")
        return []
    except json.JSONDecodeError:
        print("ERROR: El archivo JSON no tiene un formato válido.")
        return []

aspirantes = cargar_aspirantes()

# Funciones de consulta
def buscar_por_cedula(cedula):
    for a in aspirantes:
        if a.get("numero_identidad") == cedula:
            return a
    return None

def aspirantes_con_vulnerabilidad():
    return [a for a in aspirantes if a.get("vulnerabilidad_socioeconomica")]

def aspirantes_con_merito():
    return [a for a in aspirantes if a.get("merito_academico")]

def aspirantes_rurales():
    return [a for a in aspirantes if a.get("ruralidad")]

def aspirantes_con_discapacidad():
    return [a for a in aspirantes if a.get("discapacidad")]

def aspirantes_cupo_activo():
    return [a for a in aspirantes if a.get("cupo_historico_activo")]

def top_puntajes(n=10):
    # Solo incluir aspirantes que tengan puntaje definido
    aspirantes_validos = [a for a in aspirantes if "puntaje_mayor_eval_4_ult_periodos" in a]
    return sorted(
        aspirantes_validos,
        key=lambda a: a["puntaje_mayor_eval_4_ult_periodos"],
        reverse=True
    )[:n]

# Muestra de datos
if __name__ == "__main__":
    print("Total aspirantes:", len(aspirantes))
    print("Vulnerables:", len(aspirantes_con_vulnerabilidad()))
    print("Con mérito académico:", len(aspirantes_con_merito()))
    print("Rurales:", len(aspirantes_rurales()))
    print("Con discapacidad:", len(aspirantes_con_discapacidad()))
    print("Cupo histórico activo:", len(aspirantes_cupo_activo()))

    print("\nTop 5 puntajes:")
    for a in top_puntajes(5):
        nombre_completo = f"{a.get('nombres', '')} {a.get('apellidos', '')}".strip()
        puntaje = a.get("puntaje_mayor_eval_4_ult_periodos", "Sin puntaje")
        print(nombre_completo, "-", puntaje)

    # Ejemplo de búsqueda por cédula
    cedula_buscar = "2249317518"
    resultado = buscar_por_cedula(cedula_buscar)
    if resultado:
        print(f"\nAspirante encontrado ({cedula_buscar}): {resultado.get('nombres')} {resultado.get('apellidos')}")
    else:
        print(f"\nNo se encontró aspirante con cédula {cedula_buscar}.")
