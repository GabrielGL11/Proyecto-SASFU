import random
import json
from abc import ABC, abstractmethod

#Facultades
facultades = [
    "Ingeniería, Industria y Arquitectura",
    "Ciencias Sociales, Derecho y Bienestar",
    "Educación, Turismo y Humanidades",
    "Ciencias de la Salud",
    "Ciencias de la Vida y Tecnologías",
    "Ciencias Administrativas, Contables y Comercio"
]

#Matrices con nombre de las ciudades 
matrices = ["Manta", "Chone", "Sucre", "El Carmen", "Pedernales",
            "Pichincha", "Flavio Alfaro", "Santo Domingo", "Tosagua"]

#Horarios fijos para la prueba
horarios = ["08:00-10:00", "11:00-13:00", "14:00-16:00", "17:00-19:00"]

#Función para elegir matrices sin repetir, pero ponderando Manta
def elegir_matrices_sin_repetir(matrices, pesos, k):
    seleccion = []
    disponibles = matrices.copy()
    pesos_disp = pesos.copy()
    while len(seleccion) < k and disponibles:
        matriz = random.choices(disponibles, weights=pesos_disp, k=1)[0]
        seleccion.append(matriz)
        # eliminamos la matriz elegida para que no se repita en el mismo bloque
        idx = disponibles.index(matriz)
        disponibles.pop(idx)
        pesos_disp.pop(idx)
    return seleccion

#Abstract Factory
class AbstractOfertaFactory(ABC):
    @abstractmethod
    def crear_ofertas(self):
        """Debe devolver una lista de ofertas"""
        pass

#Fábrica concreta por facultad
class FacultadOfertaFactory(AbstractOfertaFactory):
    codigo_oferta = 200
    def __init__(self, facultad):
        self.facultad = facultad
    def crear_ofertas(self):
        ofertas = []
        pesos = [50] + [7]*(len(matrices)-1)#Manta 50%, otras 7%
        aulas = ["Aula 1", "Aula 2", "Aula 3"]
        for aula, horario in zip(aulas, horarios[:3]):
            matrices_elegidas = elegir_matrices_sin_repetir(matrices, pesos, 6)
            for matriz in matrices_elegidas:
                oferta = {
                    "facultad": self.facultad,
                    "aula": aula,
                    "horario": horario,
                    "matriz": matriz,
                    "cantidad": random.randint(30, 40),
                    "codigo": FacultadOfertaFactory.codigo_oferta
                }
                FacultadOfertaFactory.codigo_oferta += 1
                ofertas.append(oferta)
        return ofertas

#Uso del Abstract Factory y crea la base de datos
def crear_base_datos_horarios():
    FacultadOfertaFactory.codigo_oferta = 200
    todas_ofertas = []
    for facultad in facultades:
        factory = FacultadOfertaFactory(facultad)
        todas_ofertas.extend(factory.crear_ofertas())

#Guardar en JSON
    with open("horarios_evaluacion.json", "w", encoding="utf-8") as f:
        json.dump(todas_ofertas, f, indent=4, ensure_ascii=False)
    return len(todas_ofertas)

#Para general manualmente
if __name__ == "__main__":
    total = crear_base_datos_horarios()
    print(f"Base de datos creada correctamente. Total ofertas: {total}")