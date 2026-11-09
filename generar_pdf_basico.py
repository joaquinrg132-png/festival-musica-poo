#!/usr/bin/env python3
"""
Generador de PDF académico básico para el ITA
Tipografía:
- Títulos: Arial 14pt (Negrita)
- Texto general: Arial 12pt
Portada con el logo oficial del ITA
"""

import os
import Quartz.PDFKit as PDFKit
import AppKit
import Foundation

PAGE_W = 612   # Ancho tamaño Carta (Letter) en puntos
PAGE_H = 792   # Alto tamaño Carta (Letter) en puntos
SCALE = 2      # Escala 2x para nitidez Retina

# Fuentes requeridas por el usuario
FONT_TITLE = AppKit.NSFont.fontWithName_size_("Arial-BoldMT", 14.0) or AppKit.NSFont.boldSystemFontOfSize_(14.0)
FONT_SUBTITLE = AppKit.NSFont.fontWithName_size_("Arial-BoldMT", 12.0) or AppKit.NSFont.boldSystemFontOfSize_(12.0)
FONT_TEXT = AppKit.NSFont.fontWithName_size_("Arial", 12.0) or AppKit.NSFont.systemFontOfSize_(12.0)
FONT_TEXT_BOLD = AppKit.NSFont.fontWithName_size_("Arial-BoldMT", 12.0) or AppKit.NSFont.boldSystemFontOfSize_(12.0)
FONT_CODE = AppKit.NSFont.fontWithName_size_("Courier", 9.0) or AppKit.NSFont.userFixedPitchFontOfSize_(9.0)

COLOR_BLACK = AppKit.NSColor.blackColor()
COLOR_GRAY = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.3, 0.3, 0.3, 1.0)
COLOR_LINK = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.2, 0.6, 1.0)


def create_page():
    """Inicializa un lienzo en blanco para una página a 2x."""
    img = AppKit.NSImage.alloc().initWithSize_((PAGE_W * SCALE, PAGE_H * SCALE))
    img.lockFocus()

    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.saveGraphicsState()
    transform = AppKit.NSAffineTransform.transform()
    transform.scaleBy_(SCALE)
    transform.concat()

    # Fondo completamente blanco (básico, sin adornos)
    AppKit.NSColor.whiteColor().set()
    AppKit.NSBezierPath.fillRect_(((0, 0), (PAGE_W, PAGE_H)))

    return img


def close_page(img):
    """Cierra el lienzo y devuelve un PDFPage de tamaño estándar."""
    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.restoreGraphicsState()
    img.unlockFocus()
    img.setSize_((PAGE_W, PAGE_H))
    return PDFKit.PDFPage.alloc().initWithImage_(img)


def draw_text_line(text, x, y, font, color=COLOR_BLACK, center_w=None):
    """Dibuja una sola línea de texto. Si center_w está definido, se centra."""
    attrs = {
        AppKit.NSFontAttributeName: font,
        AppKit.NSForegroundColorAttributeName: color
    }
    s = AppKit.NSAttributedString.alloc().initWithString_attributes_(text, attrs)
    width = s.size().width
    draw_x = x if center_w is None else x + (center_w - width) / 2
    s.drawAtPoint_((draw_x, y))
    return s.size().height


def draw_paragraph(text, x, y, max_w, font=FONT_TEXT, color=COLOR_BLACK, line_spacing=4.0):
    """Dibuja un párrafo con ajuste automático de línea en Arial 12."""
    style = AppKit.NSMutableParagraphStyle.alloc().init()
    style.setLineSpacing_(line_spacing)
    attrs = {
        AppKit.NSFontAttributeName: font,
        AppKit.NSForegroundColorAttributeName: color,
        AppKit.NSParagraphStyleAttributeName: style
    }
    s = AppKit.NSAttributedString.alloc().initWithString_attributes_(text, attrs)
    size = s.boundingRectWithSize_options_((max_w, 2000), AppKit.NSStringDrawingUsesLineFragmentOrigin).size
    rect = Foundation.NSMakeRect(x, y - size.height, max_w, size.height)
    s.drawInRect_(rect)
    return size.height


def draw_page_number(page_num, total=4):
    """Número de página discreto en la parte inferior."""
    num_str = f"{page_num}"
    draw_text_line(num_str, 0, 30, FONT_TEXT, COLOR_GRAY, center_w=PAGE_W)


def build_pdf():
    doc = PDFKit.PDFDocument.alloc().init()
    margin_x = 54   # Margen de 0.75 pulgadas (54 pt)
    content_w = PAGE_W - (margin_x * 2)

    logo_path = "/Users/joaquingarcia/festival_musica/logo_ITA.png"

    # =========================================================================
    # PÁGINA 1: PORTADA BÁSICA INSTITUCIONAL
    # =========================================================================
    p1 = create_page()

    # Logo del ITA
    if os.path.exists(logo_path):
        logo_img = AppKit.NSImage.alloc().initWithContentsOfFile_(logo_path)
        if logo_img:
            # Aspect ratio 2034 x 738 (~2.75:1)
            logo_w = 270
            logo_h = logo_w * (738.0 / 2034.0)
            logo_x = (PAGE_W - logo_w) / 2
            logo_y = PAGE_H - 60 - logo_h
            logo_img.drawInRect_fromRect_operation_fraction_(
                ((logo_x, logo_y), (logo_w, logo_h)),
                Foundation.NSZeroRect,
                AppKit.NSCompositeSourceOver,
                1.0
            )
            cur_y = logo_y - 45
    else:
        cur_y = PAGE_H - 120

    # Institución
    draw_text_line("TECNOLÓGICO NACIONAL DE MÉXICO", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 22
    draw_text_line("INSTITUTO TECNOLÓGICO DE AGUASCALIENTES", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 20
    draw_text_line("DEPARTAMENTO DE SISTEMAS Y COMPUTACIÓN", margin_x, cur_y, FONT_SUBTITLE, COLOR_GRAY, center_w=content_w)

    cur_y -= 70

    # Título de la actividad
    draw_text_line("PROGRAMACIÓN ORIENTADA A OBJETOS", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 24
    draw_text_line("Actividad: Simulación de Festival de Música", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 20
    draw_text_line("Tema: Herencia y Polimorfismo en Python", margin_x, cur_y, FONT_TEXT, COLOR_GRAY, center_w=content_w)

    cur_y -= 100

    # Datos del alumno y entrega
    box_x = margin_x + 50
    draw_text_line("Alumno:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Joaquín García", box_x + 100, cur_y, FONT_TEXT, COLOR_BLACK)
    cur_y -= 22

    draw_text_line("Carrera:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Ingeniería en Sistemas Computacionales", box_x + 100, cur_y, FONT_TEXT, COLOR_BLACK)
    cur_y -= 22

    draw_text_line("Repositorio:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("https://github.com/joaquinrg132-png/festival-musica-poo", box_x + 100, cur_y, FONT_TEXT, COLOR_LINK)
    cur_y -= 22

    draw_text_line("Docente:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Profesor de Programación Orientada a Objetos", box_x + 100, cur_y, FONT_TEXT, COLOR_BLACK)

    # Lugar y fecha al pie
    draw_text_line("Aguascalientes, Ags. — Noviembre 2026", margin_x, 60, FONT_TEXT, COLOR_GRAY, center_w=content_w)

    doc.insertPage_atIndex_(close_page(p1), 0)

    # =========================================================================
    # PÁGINA 2: OBJETIVO, TEORÍA Y CAPTURA 1
    # =========================================================================
    p2 = create_page()
    draw_page_number(2, 4)
    cur_y = PAGE_H - 54

    # 1. Objetivo
    draw_text_line("1. Objetivo de la actividad", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    obj_text = (
        "Aplicar los conceptos de herencia y polimorfismo mediante la creación de un programa orientado "
        "a objetos en Python que simule un festival de música con diferentes tipos de artistas (Cantante, DJ, Banda), "
        "donde cada uno tenga su propia forma de presentarse y tocar."
    )
    h = draw_paragraph(obj_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)
    cur_y -= (h + 18)

    # 2. Fundamento Teórico
    draw_text_line("2. Fundamento teórico", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    teo_text = (
        "• Herencia: Se estructuró la clase base Artista con los atributos comunes nombre, genero y popularidad (1 al 100). "
        "Las clases derivadas Cantante, DJ y Banda reutilizan este constructor mediante super().__init__(...) y definen sus "
        "atributos específicos (cancion_mas_popular, estilo e integrantes).\n\n"
        "• Polimorfismo: Cada subclase sobrescribe el método actuar(). La función iniciar_festival(lista_artistas) invoca "
        "a presentarse(), actuar() y despedirse() de forma directa sobre cada objeto, sin emplear condicionales para "
        "discriminar su tipo."
    )
    h = draw_paragraph(teo_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)
    cur_y -= (h + 18)

    # 3. Enlace GitHub
    draw_text_line("3. Enlace al repositorio de GitHub", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    draw_text_line("Repositorio público: https://github.com/joaquinrg132-png/festival-musica-poo", margin_x, cur_y, FONT_TEXT, COLOR_LINK)
    cur_y -= 26

    # 4. Captura 1
    draw_text_line("4. Capturas de pantalla de la ejecución", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 16

    cap1_path = "/Users/joaquingarcia/festival_musica/capturas/captura_1_registro.png"
    if os.path.exists(cap1_path):
        cap1 = AppKit.NSImage.alloc().initWithContentsOfFile_(cap1_path)
        if cap1:
            img_w = content_w
            img_h = img_w * (620.0 / 860.0) * 0.62
            y_img = cur_y - img_h
            cap1.drawInRect_fromRect_operation_fraction_(((margin_x, y_img), (img_w, img_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
            draw_text_line("Figura 1: Registro interactivo de artistas solicitando atributos generales y específicos.", margin_x, y_img - 15, FONT_TEXT, COLOR_GRAY)

    doc.insertPage_atIndex_(close_page(p2), 1)

    # =========================================================================
    # PÁGINA 3: CAPTURA 2 Y CÓDIGO (PARTE 1)
    # =========================================================================
    p3 = create_page()
    draw_page_number(3, 4)
    cur_y = PAGE_H - 54

    # Captura 2
    cap2_path = "/Users/joaquingarcia/festival_musica/capturas/captura_2_festival.png"
    if os.path.exists(cap2_path):
        cap2 = AppKit.NSImage.alloc().initWithContentsOfFile_(cap2_path)
        if cap2:
            img_w = content_w
            img_h = img_w * (620.0 / 860.0) * 0.62
            y_img = cur_y - img_h
            cap2.drawInRect_fromRect_operation_fraction_(((margin_x, y_img), (img_w, img_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
            draw_text_line("Figura 2: Ejecución del festival aplicando polimorfismo y separadores de actuación.", margin_x, y_img - 15, FONT_TEXT, COLOR_GRAY)
            cur_y = y_img - 35

    # 5. Código fuente (Parte 1)
    draw_text_line("5. Código completo del programa (main.py) — Parte 1", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18

    codigo_parte_1 = [
        "class Artista:",
        "    def __init__(self, nombre: str, genero: str, popularidad: int):",
        "        self.nombre = nombre",
        "        self.genero = genero",
        "        self.popularidad = popularidad",
        "",
        "    def presentarse(self):",
        '        print(f"🎤 ¡Hola a todos! Soy {self.nombre}, exponente de {self.genero} (Popularidad: {self.popularidad}/100).")',
        "",
        "    def actuar(self):",
        '        print(f"🎵 {self.nombre} está realizando una presentación en el escenario.")',
        "",
        "    def despedirse(self):",
        '        print(f"👋 ¡Muchas gracias por su energía! Se despide {self.nombre}. ¡Hasta la próxima!")',
        "",
        "class Cantante(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, cancion_mas_popular: str):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.cancion_mas_popular = cancion_mas_popular",
        "",
        "    def actuar(self):",
        '        print(f"🎶 {self.nombre} canta su éxito {self.cancion_mas_popular} con gran energía.")',
        "",
        "class DJ(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, estilo: str):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.estilo = estilo",
        "",
        "    def actuar(self):",
        '        print(f"🎧 El DJ {self.nombre} mezcla temas de estilo {self.estilo}, haciendo vibrar al público.")',
        "",
        "class Banda(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, integrantes: int):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.integrantes = integrantes",
        "",
        "    def actuar(self):",
        '        print(f"🎸 La banda {self.nombre} con {self.integrantes} integrantes toca un poderoso solo de guitarra.")'
    ]

    line_h = 10.5
    for line in codigo_parte_1:
        draw_text_line(line, margin_x, cur_y - 8, FONT_CODE, COLOR_BLACK)
        cur_y -= line_h

    doc.insertPage_atIndex_(close_page(p3), 2)

    # =========================================================================
    # PÁGINA 4: CÓDIGO (PARTE 2) Y CONCLUSIONES
    # =========================================================================
    p4 = create_page()
    draw_page_number(4, 4)
    cur_y = PAGE_H - 54

    draw_text_line("5. Código completo del programa (main.py) — Parte 2", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18

    codigo_parte_2 = [
        "def iniciar_festival(lista_artistas):",
        '    print("\\n" + "=" * 60)',
        '    print("🎪✨ ¡COMIENZA EL GRAN FESTIVAL DE MÚSICA! ✨🎪")',
        '    print("=" * 60 + "\\n")',
        "    for i, artista in enumerate(lista_artistas, 1):",
        '        print(f"--- [Acto #{i}] ---")',
        "        artista.presentarse()",
        "        artista.actuar()",
        "        artista.despedirse()",
        '        print("\\n🎆 Fin de la actuación 🎆\\n" + "-" * 60 + "\\n")',
        "",
        "def pedir_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:",
        "    while True:",
        "        try:",
        "            valor = int(input(mensaje))",
        "            if minimo <= valor <= maximo: return valor",
        '            print(f"⚠️ Por favor ingresa un número entre {minimo} y {maximo}.")',
        "        except ValueError:",
        '            print("⚠️ Entrada no válida. Ingresa un número entero.")',
        "",
        "def main():",
        '    num = int(input("¿Cuántos artistas se presentarán en el festival?: "))',
        "    lista_artistas = []",
        "    for i in range(1, num + 1):",
        '        tipo = pedir_entero_rango("Opción (1. Cantante, 2. DJ, 3. Banda): ", 1, 3)',
        '        nom = input("Nombre: ").strip()',
        '        gen = input("Género musical: ").strip()',
        '        pop = pedir_entero_rango("Popularidad (1 al 100): ", 1, 100)',
        "        if tipo == 1:",
        '            lista_artistas.append(Cantante(nom, gen, pop, input("Canción más popular: ")))',
        "        elif tipo == 2:",
        '            lista_artistas.append(DJ(nom, gen, pop, input("Estilo de mezcla: ")))',
        "        else:",
        '            lista_artistas.append(Banda(nom, gen, pop, pedir_entero_rango("Integrantes: ", 1, 100)))',
        "    iniciar_festival(lista_artistas)",
        "",
        'if __name__ == "__main__":',
        "    main()"
    ]

    for line in codigo_parte_2:
        draw_text_line(line, margin_x, cur_y - 8, FONT_CODE, COLOR_BLACK)
        cur_y -= line_h

    cur_y -= 25

    # 6. Conclusión
    draw_text_line("6. Conclusión", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    concl_text = (
        "El desarrollo de este programa permitió constatar de forma práctica la utilidad de la herencia para "
        "evitar la redundancia de código, centralizando los atributos y métodos comunes en la clase padre Artista. "
        "A su vez, el polimorfismo hizo posible que la función iniciar_festival ejecute el método actuar() de cada "
        "objeto según su clase específica, sin requerir condicionales ni acoplamiento, logrando una arquitectura "
        "modular, escalable y mantenible."
    )
    draw_paragraph(concl_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)

    doc.insertPage_atIndex_(close_page(p4), 3)

    # Guardar PDF final
    output_pdf = "/Users/joaquingarcia/festival_musica/Actividad_Festival_Musica_POO.pdf"
    doc.writeToFile_(output_pdf)
    print(f"✅ PDF generado exitosamente: {output_pdf}")
    print(f"📄 Total de páginas: {doc.pageCount()}")


if __name__ == "__main__":
    build_pdf()
