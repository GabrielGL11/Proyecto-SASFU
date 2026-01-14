from OfertaAcademica import (
    Universidad,
    Oferta_Academica,
    Presencial,
    Virtual,
    Hibrida,
    OfertaRepositorio,
    ControladorOfertas,
    Periodo
)

def menu():
    repo = OfertaRepositorio()
    controlador = ControladorOfertas(repo)
    controlador.cargar()   

    periodo = None

    while True:
        print("\nMENÚ")
        print("1. Crear Universidad")
        print("2. Crear Oferta Académica")
        print("3. Listar Ofertas Académicas")
        print("4. Buscar Oferta por Carrera")
        print("5. Iniciar Periodo")
        print("6. Finalizar Periodo")
        print("7. Verificar si Periodo está Activo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                nombre = input("Nombre: ")
                provincia = input("Provincia: ")
                canton = input("Cantón: ")
                direccion = input("Dirección: ")
                enlace = input("Enlace: ")
                universidad = input("Tipo de universidad (Publica/Privada): ")
                tipo = input("Tipo (Normal/Tecnica): ")

                u = Universidad(nombre, provincia, canton, direccion, enlace, universidad, tipo)
                print(f"Universidad {u.nombre} creada correctamente.")

            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":

            if not periodo or not periodo.esta_activo():
                print("No se pueden crear ofertas sin un periodo activo.")
                continue

            try:
                universidad = input("Universidad: ")
                carrera = input("Carrera: ")
                cantidad = int(input("Cantidad de cupos: "))
                codigo = int(input("Código: "))
                modalidad_str = input("Modalidad (Presencial/Virtual/Hibrida): ").capitalize()

            except ValueError:
                print("Error: debe ingresar valores numéricos válidos.")
                continue

            modalidades = {
                "Presencial": Presencial(),
                "Virtual": Virtual(),
                "Hibrida": Hibrida()
            }

            if modalidad_str not in modalidades:
                print("Modalidad inválida.")
                continue

            try:
                oferta = Oferta_Academica(
                    universidad,
                    carrera,
                    cantidad,
                    codigo,
                    modalidades[modalidad_str]
                )
                controlador.agregar_oferta(oferta)
                print("Oferta académica creada y guardada.")

            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            ofertas = controlador.listar()

            if not ofertas:
                print("No hay ofertas registradas.")
            else:
                for o in ofertas:
                    print(o.exportar())

        elif opcion == "4":
            carrera = input("Ingrese la carrera a buscar: ")

            resultados = controlador.buscar_por_carrera(carrera)

            if resultados:
                for r in resultados:
                    print(r.exportar())
            else:
                print("No se encontraron ofertas para esa carrera.")

        elif opcion == "5":
            ano = input("Año lectivo: ")
            semestre = input("Semestre: ")
            periodo = Periodo(ano, semestre)
            periodo.iniciar()

        elif opcion == "6":
            if periodo:
                periodo.finalizar()
            else:
                print("No hay periodo iniciado.")

        elif opcion == "7":
            if periodo:
                print("Periodo activo" if periodo.esta_activo() else "Periodo inactivo")
            else:
                print("No hay periodo definido.")

        elif opcion == "0":
            print("Saliendo del sistema")
            break

        else:
            print("Opción inválida.")
          
if __name__ == "__main__":
    menu()
