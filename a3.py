#Clases: Universidad, Oferta_Academica, Periodo
from abc import ABC#impotar ABCMeta
from abc import abstractmethod#importar abstractmethod

class Iniciar_fase(ABC):#Interfaz Iniciar_fase
    @abstractmethod
    def iniciar(self):
        pass

class Finalizar_fase(ABC):#Interfaz Finalizar_fase
    @abstractmethod
    def finalizar(self):
        pass

class Universidad(Iniciar_fase,Finalizar_fase):#Clase Universidad que hereda de Iniciar_fase y Finalizar_fase
    Pais = "Ecuador"
    def __init__(self, nombre:str, provincia:str, canton:str, direccion:str, enlace:str,universidad:str,tipo:str):
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.direccion = direccion
        self.enlace = enlace
        self.universidad = universidad
        self.tipo = tipo
    @property
    def universidad(self):#Getter universidad
        return self._universidad
    @universidad.setter
    def universidad(self, valor:str):#Setter universidad con validacion
        valor=valor.upper()
        valores_permitidos = ["PUBLICA", "PRIVADA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad debe ser uno de los siguientes: {valores_permitidos}.")             
        self._universidad = valor
    @property
    def tipo(self):#Getter tipo
        return self._tipo
    @tipo.setter
    def tipo(self, valor:str):#Setter tipo con validacion
        valor=valor.upper()
        valores_permitidos = ["NORMAL", "TECNICA"]
        if valor not in valores_permitidos:
            raise ValueError(f"El tipo de universidad publica debe ser uno de los siguientes: {valores_permitidos}.")             
        self._tipo = valor
    def iniciar(self):#Metodo iniciar la universidad
        print(f"La universidad {self.nombre} ha iniciado su admisión en {self.Pais}.")
    def finalizar(self):#Metodo finalizar la universidad
        print(f"La universidad {self.nombre} ha finalizado su admisión en {self.Pais}.")
    def exportar_univeridad(self):
        return {
            "Nombre": self.nombre, 
            "Provincia": self.provincia,
            "Cantón": self.canton,
            "Dirección": self.direccion,
            "Enlace": self.enlace,
            "Tipo": self.universidad + " " + self.tipo
        }

class Oferta_Academica(Universidad):#Clase Oferta_Academica
    def __init__(self, carrera:str, cantidad:int, codigo:int, modalidad_oferta:str):
        self.carrera = carrera
        self.cantidad = cantidad
        self.codigo = codigo
        self.modalidad_oferta = modalidad_oferta
        self.cupos = cantidad
        self.postulantes = []
    @property
    def cantidad(self):#Getter cantidad
        return self._cantidad
    @cantidad.setter
    def cantidad(self, valor:int):#Setter cantidad con validacion
        if valor < 0:
            raise ValueError("La cantidad de cupos no puede ser negativa.")
        self._cantidad = valor  
    def crear_oferta(self):#Metodo crear_oferta
        print(f"La oferta académica para la carrera de {self.carrera} con {self.cantidad} cupos ha sido creada.")
    def esta_disponible(self): #Método esta_disponible
        return self.cantidad > 0
    def validar_modalidad(self): #Método validar_modalidad
        modalidades_validas = ["Presencial", "Virtual", "Híbrida"]
        if self.modalidad_oferta not in modalidades_validas:
            raise ValueError("Modalidad no válida")
    def validar_codigo(self): #Método validar_codigo
        if self.codigo <= 0:
            raise ValueError("El código debe ser un número positivo")
    def verificar_cupos(self): #Método verificar_cupos
        disponibles = self.cupos - len(self.postulantes)
        print(f"Cupos restantes para {self.carrera}: {disponibles}")
    def exportar_oferta(self):
        return{
            "Carrera": self.carrera,
            "Codigo": self.codigo",
            "Modalidad": self.modalidad_oferta,
            "Cupos": self.cupos,
            "Postulantes": len(self.postulantes)
        }
class Periodo(Iniciar_fase,Finalizar_fase):#Clase Periodo que hereda de Iniciar_fase y Finalizar_fase
    def __init__(self, Ano_Lectivo:str, Semestre:str):#Atributos de la clase Periodo
        self.Ano_Lectivo = Ano_Lectivo
        self.Semestre = Semestre
        print("Los datos del periodo fueron ingresados con éxitos")
    def iniciar(self):#Metodo iniciar el peridodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha iniciado.")
    def finalizar(self):#Metodo finalizar el periodo
        print(f"El periodo {self.Ano_Lectivo} - {self.Semestre} ha finalizado.")

