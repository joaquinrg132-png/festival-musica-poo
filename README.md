# 🎵 Festival de Música - Simulación con POO en Python

Este proyecto es una simulación de un festival de música orientada a objetos que implementa conceptos fundamentales de **Herencia**, **Polimorfismo** y constructores en Python.

---

## 📋 Estructura del Código

1. **Clase Base `Artista`**:
   - **Atributos**: `nombre`, `genero`, `popularidad` (1 a 100).
   - **Métodos**: `presentarse()`, `actuar()`, `despedirse()`.

2. **Subclases (Herencia)**:
   - **`Cantante`**: Añade `cancion_mas_popular` y sobrescribe `actuar()`.
   - **`DJ`**: Añade `estilo` y sobrescribe `actuar()`.
   - **`Banda`**: Añade `integrantes` y sobrescribe `actuar()`.

3. **Función `iniciar_festival(lista_artistas)` (Polimorfismo)**:
   - Itera sobre los artistas invocando `presentarse()`, `actuar()` y `despedirse()` de forma uniforme, sin evaluar condicionalmente el tipo de objeto.

4. **Función `main()`**:
   - Pide interactivamente los datos para registrar la cantidad deseada de artistas.
   - Ejecuta el festival.

---

## 🚀 Cómo ejecutar el programa

En la terminal, ejecuta:

```bash
python3 main.py
```

