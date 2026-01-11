import Usuario
sistema = Usuario.SistemaFacade()
while True:#Menu principal
    print("\nBienvenido al sistema SASFU")
    print("1. Crear usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    opcion = input("Seleccione una opción (1-3): ")
    if opcion == "1":#Crear usuario
        cedula = input("Ingrese su cédula o pasaporte (será su usuario): ")
        contrasena = input("Ingrese su contraseña: ")
        confirmar = input("Confirme su contraseña: ")
        if contrasena != confirmar:#Validar contraseñas
            print("Las contraseñas no coinciden")
            continue
        try:#Validar con la base de datos
            sistema.registrar_usuario(cedula, cedula, contrasena)
        except ValueError as e:
            print(f"Error: {e}")
    elif opcion == "2":#Iniciar sesión
        usuario = input("Ingrese su usuario (cédula): ")
        contrasena = input("Ingrese su contraseña: ")
        sistema.login(usuario, contrasena)
    elif opcion == "3":#Salir
        print("Saliendo del sistema...")
        break
    else:#Opción inválida
        print("Opción inválida, intente nuevamente")
