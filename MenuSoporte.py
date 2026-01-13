from Usuario import Soporte, RepositorioSolicitudesJSON, SoporteHandler, AdministradorHandler, Administrador
soporte = Soporte("01010101", "Ana", "Perez", "soporte@hotmail.com")#Soporte
admin = Administrador("02020202", "Luis", "Garcia", "admin@uni.com", "Director")#Administrador
cadena = SoporteHandler(soporte, AdministradorHandler(admin))#Cadena de responsabilidad
repo = RepositorioSolicitudesJSON()#Repositorio de solicitudes
while True:#Menú de soporte
    print("\n=== Menú de Soporte SASFU ===")
    soporte.iniciar_sesion()
    print("1. Revisar solicitudes de ayuda")
    print("2. Responder estado de solicitud")
    print("3. Derivar solicitud al administrador")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":#Revisar solicitudes de ayuda
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        if not solicitudes:#Verificar si hay solicitudes
            print("No hay solicitudes registradas.")
        else:#Mostrar solicitudes
            print("\n--- SOLICITUDES ---")
            for s in solicitudes:#Mostrar solicitudes
                estado = (
                    "Pendiente" if s["estado"] is None
                    else "Aceptada" if s["estado"]
                    else "Rechazada"
                )
                print(f"ID: {s['id']}")
                print(f"Cédula Aspirante: {s['cedula_aspirante']}")
                print(f"Asunto: {s.get('asunto', s.get('mensaje',''))}")
                print(f"Estado: {estado}")
                print("-" * 30)
    elif opcion == "2":#Responder estado de solicitud
        try:#Responder estado de solicitud
            id_solicitud = int(input("Ingrese el ID de la solicitud: "))
            decision = input("¿Aceptar la solicitud? (s/n): ").lower()
            if decision == "s":#Aceptar solicitud
                soporte.responder_solicitud(id_solicitud, True)
            elif decision == "n":#Rechazar solicitud
                soporte.responder_solicitud(id_solicitud, False)
            else:#Opción inválida
                print("Opción inválida.")
        except ValueError:#Capturar error de conversión a entero
            print("El ID debe ser un número.")
    elif opcion == "3":#Derivar solicitud al administrador
        try:#Derivar solicitud
            id_solicitud = int(input("Ingrese el ID de la solicitud a derivar: "))
            solicitudes = repo.leer_todos()
            solicitud = next((s for s in solicitudes if s["id"] == id_solicitud), None)
            if not solicitud:#Verificar si la solicitud existe
                print("Solicitud no encontrada.")
                continue
            tipo = input("Ingrese tipo de solicitud (tecnico/academico/grave): ").lower()
            solicitud["tipo"] = tipo#Asignar tipo de solicitud
            solicitud["estado"] = True if tipo in ["tecnico", "academico", "grave"] else False
            repo.guardar_todos(solicitudes)#Guardar cambios en el repositorio
            cadena.manejar(tipo)#Derivar solicitud a través de la cadena de responsabilidad
            print(f"Solicitud ID {id_solicitud} derivada como '{tipo}' y actualizada en el sistema.")
        except ValueError:#Capturar error de conversión a entero
            print("El ID debe ser un número.")
    elif opcion == "4":#Salir del menú de soporte
        print("Saliendo del menú de soporte...")
        soporte.cerrar_sesion()
        break
    else:#Opción inválida
        print("Opción no válida.")
