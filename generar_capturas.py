#!/usr/bin/env python3
"""
Script para generar capturas de pantalla de la terminal sin emojis
"""
import os
import AppKit
import Foundation

def create_terminal_screenshot(output_path, title, lines_data, width=850, height=620):
    image = AppKit.NSImage.alloc().initWithSize_(Foundation.NSMakeSize(width, height))
    image.lockFocus()

    # Fondo de la ventana (Dark Theme macOS)
    bg_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.11, 0.12, 0.15, 1.0)
    bg_color.set()
    clip_path = AppKit.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(
        Foundation.NSMakeRect(0, 0, width, height), 10.0, 10.0
    )
    clip_path.fill()

    # Barra de título
    title_bar_height = 36
    bar_rect = Foundation.NSMakeRect(0, height - title_bar_height, width, title_bar_height)
    bar_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.16, 0.17, 0.21, 1.0)
    bar_color.set()
    AppKit.NSBezierPath.fillRect_(bar_rect)

    # Botones macOS
    button_y = height - title_bar_height / 2 - 6
    btn_colors = [
        (0.98, 0.36, 0.35),
        (0.99, 0.75, 0.20),
        (0.16, 0.79, 0.38)
    ]
    for idx, (r, g, b) in enumerate(btn_colors):
        b_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, 1.0)
        b_color.set()
        b_rect = Foundation.NSMakeRect(16 + idx * 20, button_y, 12, 12)
        AppKit.NSBezierPath.bezierPathWithOvalInRect_(b_rect).fill()

    # Título en la barra
    title_font = AppKit.NSFont.boldSystemFontOfSize_(12.0)
    title_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.65, 0.67, 0.72, 1.0)
    title_attrs = {
        AppKit.NSFontAttributeName: title_font,
        AppKit.NSForegroundColorAttributeName: title_color
    }
    title_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(title, title_attrs)
    title_size = title_str.size()
    title_x = (width - title_size.width) / 2
    title_y = height - title_bar_height + (title_bar_height - title_size.height) / 2
    title_str.drawAtPoint_(Foundation.NSMakePoint(title_x, title_y))

    # Contenido de la terminal
    font = AppKit.NSFont.fontWithName_size_("Menlo", 12.0)
    if not font:
        font = AppKit.NSFont.fontWithName_size_("Monaco", 12.0)
    if not font:
        font = AppKit.NSFont.userFixedPitchFontOfSize_(12.0)

    cur_y = height - title_bar_height - 24
    line_spacing = 18

    for text, (r, g, b) in lines_data:
        text_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, 1.0)
        attrs = {
            AppKit.NSFontAttributeName: font,
            AppKit.NSForegroundColorAttributeName: text_color
        }
        line_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(text, attrs)
        line_str.drawAtPoint_(Foundation.NSMakePoint(20, cur_y))
        cur_y -= line_spacing
        if cur_y < 15:
            break

    image.unlockFocus()

    # Guardar como PNG
    tiff_data = image.TIFFRepresentation()
    bitmap = AppKit.NSBitmapImageRep.imageRepsWithData_(tiff_data)[0]
    png_data = bitmap.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, None)
    png_data.writeToFile_atomically_(output_path, True)
    print(f"Captura guardada en: {output_path}")

# Datos para Captura 1: Entrada y Registro (Sin emojis)
lineas_captura_1 = [
    ("joaquin@MacBook-Pro festival_musica % python3 main.py", (0.40, 0.85, 0.40)),
    ("========================================", (0.45, 0.50, 0.60)),
    ("    REGISTRO DEL FESTIVAL DE MUSICA     ", (0.35, 0.75, 1.00)),
    ("========================================", (0.45, 0.50, 0.60)),
    ("Cuantos artistas se presentaran en el festival?: 3", (0.95, 0.95, 0.95)),
    ("", (1, 1, 1)),
    ("--- Datos del Artista #1 ---", (1.00, 0.80, 0.30)),
    ("Selecciona el tipo de artista:", (0.75, 0.75, 0.75)),
    ("  1. Cantante", (0.75, 0.75, 0.75)),
    ("  2. DJ", (0.75, 0.75, 0.75)),
    ("  3. Banda", (0.75, 0.75, 0.75)),
    ("Opcion (1-3): 1", (0.95, 0.95, 0.95)),
    ("Nombre: Dua Lipa", (0.95, 0.95, 0.95)),
    ("Genero musical: Pop", (0.95, 0.95, 0.95)),
    ("Popularidad (1 al 100): 95", (0.95, 0.95, 0.95)),
    ("Cancion mas popular: Levitating", (0.95, 0.95, 0.95)),
    ("", (1, 1, 1)),
    ("--- Datos del Artista #2 ---", (1.00, 0.80, 0.30)),
    ("Selecciona el tipo de artista:", (0.75, 0.75, 0.75)),
    ("  1. Cantante", (0.75, 0.75, 0.75)),
    ("  2. DJ", (0.75, 0.75, 0.75)),
    ("  3. Banda", (0.75, 0.75, 0.75)),
    ("Opcion (1-3): 2", (0.95, 0.95, 0.95)),
    ("Nombre: Tiesto", (0.95, 0.95, 0.95)),
    ("Genero musical: Electronica", (0.95, 0.95, 0.95)),
    ("Popularidad (1 al 100): 90", (0.95, 0.95, 0.95)),
    ("Estilo de mezcla (ej. House, Techno, Electro): Trance", (0.95, 0.95, 0.95)),
    ("", (1, 1, 1)),
    ("--- Datos del Artista #3 ---", (1.00, 0.80, 0.30)),
    ("Opcion (1-3): 3", (0.95, 0.95, 0.95)),
    ("Nombre: Queen | Genero: Rock | Popularidad: 99 | Integrantes: 4", (0.95, 0.95, 0.95)),
]

# Datos para Captura 2: Ejecución del Festival (Sin emojis)
lineas_captura_2 = [
    ("============================================================", (0.45, 0.50, 0.60)),
    ("        COMIENZA EL GRAN FESTIVAL DE MUSICA        ", (1.00, 0.84, 0.00)),
    ("============================================================", (0.45, 0.50, 0.60)),
    ("", (1, 1, 1)),
    ("--- [Acto #1] ---", (0.35, 0.75, 1.00)),
    ("Hola a todos! Soy Dua Lipa, exponente de Pop (Popularidad: 95/100).", (0.90, 0.90, 0.90)),
    ("Dua Lipa canta su exito 'Levitating' con gran energia.", (0.40, 0.85, 0.40)),
    ("Muchas gracias por su energia! Se despide Dua Lipa. Hasta la proxima!", (0.80, 0.80, 0.80)),
    ("", (1, 1, 1)),
    ("--- Fin de la actuacion ---", (1.00, 0.65, 0.65)),
    ("------------------------------------------------------------", (0.45, 0.50, 0.60)),
    ("", (1, 1, 1)),
    ("--- [Acto #2] ---", (0.35, 0.75, 1.00)),
    ("Hola a todos! Soy Tiesto, exponente de Electronica (Popularidad: 90/100).", (0.90, 0.90, 0.90)),
    ("El DJ Tiesto mezcla temas de estilo Trance, haciendo vibrar al publico.", (0.40, 0.85, 0.40)),
    ("Muchas gracias por su energia! Se despide Tiesto. Hasta la proxima!", (0.80, 0.80, 0.80)),
    ("", (1, 1, 1)),
    ("--- Fin de la actuacion ---", (1.00, 0.65, 0.65)),
    ("------------------------------------------------------------", (0.45, 0.50, 0.60)),
    ("", (1, 1, 1)),
    ("--- [Acto #3] ---", (0.35, 0.75, 1.00)),
    ("Hola a todos! Soy Queen, exponente de Rock (Popularidad: 99/100).", (0.90, 0.90, 0.90)),
    ("La banda Queen con 4 integrantes toca un poderoso solo de guitarra.", (0.40, 0.85, 0.40)),
    ("Muchas gracias por su energia! Se despide Queen. Hasta la proxima!", (0.80, 0.80, 0.80)),
    ("", (1, 1, 1)),
    ("--- Fin de la actuacion ---", (1.00, 0.65, 0.65)),
    ("------------------------------------------------------------", (0.45, 0.50, 0.60)),
    ("El festival ha concluido exitosamente. Gracias al publico asistente!", (1.00, 0.84, 0.00)),
]

if __name__ == "__main__":
    os.makedirs("/Users/joaquingarcia/festival_musica/capturas", exist_ok=True)
    create_terminal_screenshot(
        "/Users/joaquingarcia/festival_musica/capturas/captura_1_registro.png",
        "Terminal - Registro de Artistas (Cantante, DJ, Banda)",
        lineas_captura_1,
        width=860,
        height=620
    )
    create_terminal_screenshot(
        "/Users/joaquingarcia/festival_musica/capturas/captura_2_festival.png",
        "Terminal - Ejecucion del Festival (Polimorfismo)",
        lineas_captura_2,
        width=860,
        height=620
    )
