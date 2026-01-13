from Usuario import Soporte, RepositorioSolicitudesJSON
soporte = Soporte("01010101", "Ana", "Perez", "soporte@hotmail.com")
while True:#Menú de soporte
    print("\nMenú de Soporte SASFU")
    soporte.iniciar_sesion()
    print("1. Revisar solicitudes de ayuda")
    print("2. Responder estado de solicitud")
    print("3. Derivar solicitud al administrador")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":#Revisar solicitudes de ayuda
        repo = RepositorioSolicitudesJSON()#Importar el repositorio de solicitudes
        solicitudes = repo.leer_todos()#Leer todas las solicitudes
        if not solicitudes:#Verificar si hay solicitudes
            print("No hay solicitudes registradas.")
        else:#Mostrar solicitudes
            print("\n--- SOLICITUDES ---")
            for s in solicitudes:
                estado = (
                    "Pendiente" if s["estado"] is None
                    else "Aceptada" if s["estado"]
                    else "Rechazada"
                )
                print(f"ID: {s['id']}")
                print(f"Cédula Aspirante: {s['cedula_aspirante']}")
                print(f"Mensaje: {s['mensaje']}")
                print(f"Estado: {estado}")
                print("-" * 30)
    elif opcion == "2":
        try:#Responder estado de solicitud
            id_solicitud = int(input("Ingrese el ID de la solicitud: "))#Solicitar ID de solicitud
            decision = input("¿Aceptar la solicitud? (s/n): ").lower()#Solicitar decisión
            if decision == "s":#Aceptar solicitud
                soporte.responder_solicitud(id_solicitud, True)
            elif decision == "n":#Rechazar solicitud
                soporte.responder_solicitud(id_solicitud, False)
            else:#Opción inválida
                print("Opción inválida.")
        except ValueError:#Capturar error de conversión a entero
            print("El ID debe ser un número.")
    elif opcion == "3":#Derivar solicitud al administrador
        print("Solicitud derivada al administrador (simulado).")
    elif opcion == "4":#Salir del menú de soporte
        print("Saliendo del menú de soporte...")
        soporte.cerrar_sesion()
        break
    else:#Opción inválida
        print("Opción no válida.")
