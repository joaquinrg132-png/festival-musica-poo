"""
Programa: Simulacion de Festival de Musica
Conceptos aplicados: Programacion Orientada a Objetos (POO), Herencia y Polimorfismo.
"""

# ==========================================
# 1. CLASE BASE: Artista
# ==========================================
class Artista:
    """Clase base que representa a un artista musical generico."""

    def __init__(self, nombre: str, genero: str, popularidad: int):
        self.nombre = nombre
        self.genero = genero
        self.popularidad = popularidad

    def presentarse(self):
        """Presentacion generica del artista."""
        print(f"Hola a todos! Soy {self.nombre}, exponente de {self.genero} (Popularidad: {self.popularidad}/100).")

    def actuar(self):
        """Metodo base que sera sobrescrito por cada subclase (polimorfismo)."""
        print(f"{self.nombre} esta realizando una presentacion en el escenario.")

    def despedirse(self):
        """Mensaje de despedida del artista."""
        print(f"Muchas gracias por su energia! Se despide {self.nombre}. Hasta la proxima!")


# ==========================================
# 2. SUBCLASES DE Artista (HERENCIA)
# ==========================================
class Cantante(Artista):
    """Subclase que representa a un cantante solista."""

    def __init__(self, nombre: str, genero: str, popularidad: int, cancion_mas_popular: str):
        super().__init__(nombre, genero, popularidad)
        self.cancion_mas_popular = cancion_mas_popular

    def actuar(self):
        """Sobrescribe actuar() con el comportamiento especifico de un cantante."""
        print(f"{self.nombre} canta su exito '{self.cancion_mas_popular}' con gran energia.")


class DJ(Artista):
    """Subclase que representa a un DJ."""

    def __init__(self, nombre: str, genero: str, popularidad: int, estilo: str):
        super().__init__(nombre, genero, popularidad)
        self.estilo = estilo

    def actuar(self):
        """Sobrescribe actuar() con el comportamiento especifico de un DJ."""
        print(f"El DJ {self.nombre} mezcla temas de estilo {self.estilo}, haciendo vibrar al publico.")


class Banda(Artista):
    """Subclase que representa a una banda musical."""

    def __init__(self, nombre: str, genero: str, popularidad: int, integrantes: int):
        super().__init__(nombre, genero, popularidad)
        self.integrantes = integrantes

    def actuar(self):
        """Sobrescribe actuar() con el comportamiento especifico de una banda."""
        print(f"La banda {self.nombre} con {self.integrantes} integrantes toca un poderoso solo de guitarra.")


# ==========================================
# 3. FUNCION DE INICIO DEL FESTIVAL (POLIMORFISMO)
# ==========================================
def iniciar_festival(lista_artistas):
    """
    Recorre la lista de artistas y ejecuta sus metodos.
    Aplica POLIMORFISMO: trata a todos los objetos como instancias de Artista
    sin necesidad de condicionales (if/elif) para verificar su tipo especifico.
    """
    if not lista_artistas:
        print("No hay artistas registrados para el festival.")
        return

    print("\n" + "=" * 60)
    print("        COMIENZA EL GRAN FESTIVAL DE MUSICA        ")
    print("=" * 60 + "\n")

    for i, artista in enumerate(lista_artistas, 1):
        print(f"--- [Acto #{i}] ---")
        artista.presentarse()
        artista.actuar()
        artista.despedirse()
        print("\n--- Fin de la actuacion ---\n" + "-" * 60 + "\n")

    print("El festival ha concluido exitosamente. Gracias al publico asistente!\n")


# ==========================================
# 4. PROGRAMA PRINCIPAL
# ==========================================
def pedir_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:
    """Funcion auxiliar para validar numeros enteros dentro de un rango."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Por favor ingresa un numero entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada no valida. Ingresa un numero entero.")


def main():
    print("========================================")
    print("    REGISTRO DEL FESTIVAL DE MUSICA     ")
    print("========================================")

    while True:
        try:
            num_artistas = int(input("Cuantos artistas se presentaran en el festival?: "))
            if num_artistas > 0:
                break
            print("Debes registrar al menos 1 artista.")
        except ValueError:
            print("Por favor ingresa un numero valido.")

    lista_artistas = []

    for i in range(1, num_artistas + 1):
        print(f"\n--- Datos del Artista #{i} ---")
        print("Selecciona el tipo de artista:")
        print("  1. Cantante")
        print("  2. DJ")
        print("  3. Banda")

        tipo = pedir_entero_rango("Opcion (1-3): ", 1, 3)

        nombre = input("Nombre: ").strip()
        genero = input("Genero musical: ").strip()
        popularidad = pedir_entero_rango("Popularidad (1 al 100): ", 1, 100)

        # Creacion del objeto segun el tipo seleccionado
        if tipo == 1:
            cancion = input("Cancion mas popular: ").strip()
            artista = Cantante(nombre, genero, popularidad, cancion)
        elif tipo == 2:
            estilo = input("Estilo de mezcla (ej. House, Techno, Electro): ").strip()
            artista = DJ(nombre, genero, popularidad, estilo)
        else:
            integrantes = pedir_entero_rango("Numero de integrantes: ", 1, 100)
            artista = Banda(nombre, genero, popularidad, integrantes)

        lista_artistas.append(artista)

    # Iniciar festival utilizando polimorfismo
    iniciar_festival(lista_artistas)


if __name__ == "__main__":
    main()
