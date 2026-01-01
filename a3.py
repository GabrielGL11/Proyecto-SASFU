#Clases: Universidad, Oferta_Academica, Periodo
from abc import ABC #Impotar ABCMeta
from abc import abstractmethod #Importar abstractmethod
import json #Imporar json

class Iniciar_fase(ABC):#Interfaz Iniciar_fase/Patrón de diseño Strategy
    @abstractmethod
    def iniciar(self):
        pass

class Finalizar_fase(ABC):#Interfaz Finalizar_fase/Patrón de diseño Strategy 
    @abstractmethod
    def finalizar(self):
        pass

class Universidad:
    Pais = "Ecuador"
    def __init__(self, nombre:str, provincia:str, canton:str, direccion:str, enlace:str,universidad:str,tipo:str):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace
        self.universidad = universidad.upper()
        self.tipo = tipo.upper()
        
    @property
    def universidad(self):#Getter universidad
        return self._universidad
        
    @universidad.setter
    def universidad(self, valor:str):#Setter universidad con validación
        valor=valor.upper()
        valores_permitidos = ["PUBLICA", "PRIVADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._universidad = valor
        
    @property
    def tipo(self):#Getter tipo
        return self._tipo
        
    @tipo.setter
    def tipo(self, valor:str):#Setter tipo con validación
        valor=valor.upper()
        valores_permitidos = ["NORMAL", "TECNICA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad publica debe ser uno de los siguientes: {valores_permitidos}.")             
        self._tipo = valor

class Oferta_Academica:
    def __init__(self, universidad:str, carrera:str, cantidad:int, codigo:int, modalidad:str):
        self.universidad = universidad
        self.carrera = carrera
        self.cantidad = cantidad 
        self.codigo = codigo
        self.modalidad = modalidad 
        self.postulantes = []
        
        self.validar_codigo()
        self.validar_modalidad()
        
    @property
    def cantidad(self):#Getter cantidad
        return self._cantidad
        
    @cantidad.setter
    def cantidad(self, valor:int):#Setter cantidad con validacion
        if valor < 0:
            raise ValueError("La cantidad de cupos no puede ser negativa.")
        self._cantidad = valor  
   
    def esta_disponible(self): #Método esta_disponible
        return self.cantidad > 0

    def validar_modalidad(self): #Método validar_modalidad
        modalidades_validas = ["Presencial", "Virtual", "Híbrida"]
        if self.modalidad_oferta not in modalidades_validas:
            raise ValueError("Modalidad no válida")

    def validar_codigo(self): #Método validar_codigo
        if self.codigo <= 0:
            raise ValueError("El código debe ser un número positivo.")
  
    def verificar_cupos(self): #Método verificar_cupos
        disponibles = self.cantidad - len(self.postulantes)
        print(f"Cupos restantes para {self.carrera}: {disponibles}.")

    def exportar(self): #Método exportar
        return{
            "Universidad": self.universidad,
            "Carrera": self.carrera,
            "Codigo": self.codigo,
            "Modalidad": self.modalidad,
            "Cupos": self.cantidad,
            "Postulantes": len(self.postulantes)
        }

class OfertaFactory: #Patrón de diseño Factory Method 
    @staticmethod
    def crear_desde_json(data): #Método crear_desde_json
        return Oferta_Academica(
            universidad=data["Univerdiad"],
            carrera=data["Carrera"],
            cantidad=data["Cupos"],
            codigo=data["Codigo"],
            modalidad=data["Modalidad"]
        )
        
class OfertaRepositorio: #Repositorio json
    def __init(self, archivo="ofertas.json"):
        self.archivo = archivo
    
    def guardar(self, ofertas: list[Oferta_Academica]): #Método guardar
        data = [o.exportar() for o in ofertas]
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
     def cargar(self) -> list[Oferta_Academica]: #Método cargar
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [OfertaFactory.crear_desde_json(d) for d in data]
        except FileNotFoundError:
            return []

class ControladorOfertas: #Patrón de diseño Controller
    def __init__(self, repo: OfertaRepositorio):  
        self.repo = repo
        self.ofertas = []

    def cargar(self): #Método cargar
        self.ofertas = self.repo.cargar()  
        return self.ofertas

    def guardar(self): #Método guardar
        self.repo.guardar(self.ofertas)  

    def agregar_oferta(self, oferta: Oferta_Academica): #Método agregar_oferta
        self.ofertas.append(oferta)
        self.guardar()

    def listar(self): #Método listar
        return self.ofertas
    
class Periodo(Iniciar_fase,Finalizar_fase):#Clase Periodo que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, ano_lectivo:str, semestre:str):
        self.ano_lectivo = ano_lectivo
        self.semestre = semestre
        print("Los datos del periodo fueron ingresados con éxito.")
  
    def iniciar(self):#Método iniciar el peridodo
        print(f"El periodo {self.ano_lectivo} - {self.semestre} ha iniciado.")
    
    def finalizar(self):#Metodo finalizar el periodo
        print(f"El periodo {self.ano_lectivo} - {self.semestre} ha finalizado.")



