import Usuario#Importar módulo Usuario
from datetime import date#Importar date para manejo de fechas y abajo crea la cuenta de administrador
admin = Usuario.Administrador("01010101", "Admin", "ULEAMBUENASMANOS", "admin@hotmail.com", "Administrador")
while True:#Menú de administrador
    print("\nMenú de Administrador SASFU")
    print("1. Abrir inscripciones")
    print("2. Cerrar inscripciones")
    print("3. Abrir evaluaciones")
    print("4. Cerrar evaluaciones")
    print("5. Abrir postulaciones")
    print("6. Cerrar postulaciones")
    print("7. Salir")
    opcion = input("Seleccione una opción (1-7): ")#Solicitar opción
    if opcion == "1":#Abrir inscripciones con fechas personalizadas
        print("=== Abrir Inscripciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_inscripciones(fecha_inicio, fecha_fin)
        except ValueError as e:#Capturar error en formato de fechas
            print("Error en las fechas:", e)
    elif opcion == "2":#Cerrar inscripciones
        admin.cerrar_inscripciones()
    elif opcion == "3":#Abrir evaluaciones con fechas personalizadas
        print("=== Abrir Evaluaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_evaluaciones(fecha_inicio, fecha_fin)
        except ValueError as e:
            print("Error en las fechas:", e)
    elif opcion == "4":#Cerrar evaluaciones
        admin.cerrar_evaluaciones()
    elif opcion == "5":#Abrir postulaciones con fechas personalizadas
        print("=== Abrir Postulaciones ===")
        fi = input("Fecha inicio (YYYY-MM-DD): ")
        ff = input("Fecha fin (YYYY-MM-DD): ")
        try:#Validar formato de fechas
            fecha_inicio = date.fromisoformat(fi)
            fecha_fin = date.fromisoformat(ff)
            admin.abrir_postulaciones(fecha_inicio, fecha_fin)
        except ValueError as e:
            print("Error en las fechas:", e)
    elif opcion == "6":#Cerrar postulaciones
        admin.cerrar_postulaciones()
    elif opcion == "7":#Salir del menú
        print("Saliendo del menú de administrador...")
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")


