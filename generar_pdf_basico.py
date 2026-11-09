#!/usr/bin/env python3
"""
Generador de PDF academico basico para el ITA (Sin emojis)
Tipografia:
- Titulos: Arial 14pt (Negrita)
- Texto general: Arial 12pt
Portada con el logo oficial del ITA
"""

import os
import Quartz.PDFKit as PDFKit
import AppKit
import Foundation

PAGE_W = 612   # Ancho tamano Carta (Letter) en puntos
PAGE_H = 792   # Alto tamano Carta (Letter) en puntos
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
    img = AppKit.NSImage.alloc().initWithSize_((PAGE_W * SCALE, PAGE_H * SCALE))
    img.lockFocus()

    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.saveGraphicsState()
    transform = AppKit.NSAffineTransform.transform()
    transform.scaleBy_(SCALE)
    transform.concat()

    AppKit.NSColor.whiteColor().set()
    AppKit.NSBezierPath.fillRect_(((0, 0), (PAGE_W, PAGE_H)))

    return img


def close_page(img):
    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.restoreGraphicsState()
    img.unlockFocus()
    img.setSize_((PAGE_W, PAGE_H))
    return PDFKit.PDFPage.alloc().initWithImage_(img)


def draw_text_line(text, x, y, font, color=COLOR_BLACK, center_w=None):
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
    num_str = f"{page_num}"
    draw_text_line(num_str, 0, 30, FONT_TEXT, COLOR_GRAY, center_w=PAGE_W)


def build_pdf():
    doc = PDFKit.PDFDocument.alloc().init()
    margin_x = 54
    content_w = PAGE_W - (margin_x * 2)

    logo_path = "/Users/joaquingarcia/festival_musica/logo_ITA.png"

    # =========================================================================
    # PAGINA 1: PORTADA BASICA INSTITUCIONAL
    # =========================================================================
    p1 = create_page()

    if os.path.exists(logo_path):
        logo_img = AppKit.NSImage.alloc().initWithContentsOfFile_(logo_path)
        if logo_img:
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

    draw_text_line("TECNOLOGICO NACIONAL DE MEXICO", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 22
    draw_text_line("INSTITUTO TECNOLOGICO DE AGUASCALIENTES", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 20
    draw_text_line("DEPARTAMENTO DE SISTEMAS Y COMPUTACION", margin_x, cur_y, FONT_SUBTITLE, COLOR_GRAY, center_w=content_w)

    cur_y -= 70

    draw_text_line("PROGRAMACION ORIENTADA A OBJETOS", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 24
    draw_text_line("Actividad: Simulacion de Festival de Musica", margin_x, cur_y, FONT_TITLE, COLOR_BLACK, center_w=content_w)
    cur_y -= 20
    draw_text_line("Tema: Herencia y Polimorfismo en Python", margin_x, cur_y, FONT_TEXT, COLOR_GRAY, center_w=content_w)

    cur_y -= 100

    box_x = margin_x + 30
    val_x = box_x + 90
    draw_text_line("Alumno:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Joaquín García", val_x, cur_y, FONT_TEXT, COLOR_BLACK)
    cur_y -= 22

    draw_text_line("Carrera:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Ingeniería en Tecnologías de la Información y Comunicaciones", val_x, cur_y, FONT_TEXT, COLOR_BLACK)
    cur_y -= 22

    draw_text_line("Repositorio:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("https://github.com/joaquinrg132-png/festival-musica-poo", val_x, cur_y, FONT_TEXT, COLOR_LINK)
    cur_y -= 22

    draw_text_line("Docente:", box_x, cur_y, FONT_TEXT_BOLD, COLOR_BLACK)
    draw_text_line("Mtra. Yomira del Carmen Rosales Martínez", val_x, cur_y, FONT_TEXT, COLOR_BLACK)

    draw_text_line("Aguascalientes, Ags. - Noviembre 2026", margin_x, 60, FONT_TEXT, COLOR_GRAY, center_w=content_w)

    doc.insertPage_atIndex_(close_page(p1), 0)

    # =========================================================================
    # PAGINA 2: OBJETIVO, TEORIA Y CAPTURA 1
    # =========================================================================
    p2 = create_page()
    draw_page_number(2, 4)
    cur_y = PAGE_H - 54

    draw_text_line("1. Objetivo de la actividad", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    obj_text = (
        "Aplicar los conceptos de herencia y polimorfismo mediante la creacion de un programa orientado "
        "a objetos en Python que simule un festival de musica con diferentes tipos de artistas (Cantante, DJ, Banda), "
        "donde cada uno tenga su propia forma de presentarse y tocar."
    )
    h = draw_paragraph(obj_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)
    cur_y -= (h + 18)

    draw_text_line("2. Fundamento teorico", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    teo_text = (
        "• Herencia: Se estructuro la clase base Artista con los atributos comunes nombre, genero y popularidad (1 al 100). "
        "Las clases derivadas Cantante, DJ y Banda reutilizan este constructor mediante super().__init__(...) y definen sus "
        "atributos especificos (cancion_mas_popular, estilo e integrantes).\n\n"
        "• Polimorfismo: Cada subclase sobrescribe el metodo actuar(). La funcion iniciar_festival(lista_artistas) invoca "
        "a presentarse(), actuar() y despedirse() de forma directa sobre cada objeto, sin emplear condicionales para "
        "discriminar su tipo."
    )
    h = draw_paragraph(teo_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)
    cur_y -= (h + 18)

    draw_text_line("3. Enlace al repositorio de GitHub", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    draw_text_line("Repositorio publico: https://github.com/joaquinrg132-png/festival-musica-poo", margin_x, cur_y, FONT_TEXT, COLOR_LINK)
    cur_y -= 26

    draw_text_line("4. Capturas de pantalla de la ejecucion", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 16

    cap1_path = "/Users/joaquingarcia/festival_musica/capturas/captura_1_registro.png"
    if os.path.exists(cap1_path):
        cap1 = AppKit.NSImage.alloc().initWithContentsOfFile_(cap1_path)
        if cap1:
            img_w = content_w
            img_h = img_w * (620.0 / 860.0) * 0.62
            y_img = cur_y - img_h
            cap1.drawInRect_fromRect_operation_fraction_(((margin_x, y_img), (img_w, img_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
            draw_text_line("Figura 1: Registro interactivo de artistas solicitando atributos generales y especificos.", margin_x, y_img - 15, FONT_TEXT, COLOR_GRAY)

    doc.insertPage_atIndex_(close_page(p2), 1)

    # =========================================================================
    # PAGINA 3: CAPTURA 2 Y CODIGO (PARTE 1)
    # =========================================================================
    p3 = create_page()
    draw_page_number(3, 4)
    cur_y = PAGE_H - 54

    cap2_path = "/Users/joaquingarcia/festival_musica/capturas/captura_2_festival.png"
    if os.path.exists(cap2_path):
        cap2 = AppKit.NSImage.alloc().initWithContentsOfFile_(cap2_path)
        if cap2:
            img_w = content_w
            img_h = img_w * (620.0 / 860.0) * 0.62
            y_img = cur_y - img_h
            cap2.drawInRect_fromRect_operation_fraction_(((margin_x, y_img), (img_w, img_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
            draw_text_line("Figura 2: Ejecucion del festival aplicando polimorfismo y separadores de actuacion.", margin_x, y_img - 15, FONT_TEXT, COLOR_GRAY)
            cur_y = y_img - 35

    draw_text_line("5. Codigo completo del programa (main.py) - Parte 1", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18

    codigo_parte_1 = [
        "class Artista:",
        "    def __init__(self, nombre: str, genero: str, popularidad: int):",
        "        self.nombre = nombre",
        "        self.genero = genero",
        "        self.popularidad = popularidad",
        "",
        "    def presentarse(self):",
        '        print(f"Hola a todos! Soy {self.nombre}, exponente de {self.genero} (Popularidad: {self.popularidad}/100).")',
        "",
        "    def actuar(self):",
        '        print(f"{self.nombre} esta realizando una presentacion en el escenario.")',
        "",
        "    def despedirse(self):",
        '        print(f"Muchas gracias por su energia! Se despide {self.nombre}. Hasta la proxima!")',
        "",
        "class Cantante(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, cancion_mas_popular: str):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.cancion_mas_popular = cancion_mas_popular",
        "",
        "    def actuar(self):",
        '        print(f"{self.nombre} canta su exito {self.cancion_mas_popular} con gran energia.")',
        "",
        "class DJ(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, estilo: str):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.estilo = estilo",
        "",
        "    def actuar(self):",
        '        print(f"El DJ {self.nombre} mezcla temas de estilo {self.estilo}, haciendo vibrar al publico.")',
        "",
        "class Banda(Artista):",
        "    def __init__(self, nombre: str, genero: str, popularidad: int, integrantes: int):",
        "        super().__init__(nombre, genero, popularidad)",
        "        self.integrantes = integrantes",
        "",
        "    def actuar(self):",
        '        print(f"La banda {self.nombre} con {self.integrantes} integrantes toca un poderoso solo de guitarra.")'
    ]

    line_h = 10.5
    for line in codigo_parte_1:
        draw_text_line(line, margin_x, cur_y - 8, FONT_CODE, COLOR_BLACK)
        cur_y -= line_h

    doc.insertPage_atIndex_(close_page(p3), 2)

    # =========================================================================
    # PAGINA 4: CODIGO (PARTE 2) Y CONCLUSIONES
    # =========================================================================
    p4 = create_page()
    draw_page_number(4, 4)
    cur_y = PAGE_H - 54

    draw_text_line("5. Codigo completo del programa (main.py) - Parte 2", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18

    codigo_parte_2 = [
        "def iniciar_festival(lista_artistas):",
        '    print("\\n" + "=" * 60)',
        '    print("        COMIENZA EL GRAN FESTIVAL DE MUSICA        ")',
        '    print("=" * 60 + "\\n")',
        "    for i, artista in enumerate(lista_artistas, 1):",
        '        print(f"--- [Acto #{i}] ---")',
        "        artista.presentarse()",
        "        artista.actuar()",
        "        artista.despedirse()",
        '        print("\\n--- Fin de la actuacion ---\\n" + "-" * 60 + "\\n")',
        "",
        "def pedir_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:",
        "    while True:",
        "        try:",
        "            valor = int(input(mensaje))",
        "            if minimo <= valor <= maximo: return valor",
        '            print(f"Por favor ingresa un numero entre {minimo} y {maximo}.")',
        "        except ValueError:",
        '            print("Entrada no valida. Ingresa un numero entero.")',
        "",
        "def main():",
        '    num = int(input("Cuantos artistas se presentaran en el festival?: "))',
        "    lista_artistas = []",
        "    for i in range(1, num + 1):",
        '        tipo = pedir_entero_rango("Opcion (1. Cantante, 2. DJ, 3. Banda): ", 1, 3)',
        '        nom = input("Nombre: ").strip()',
        '        gen = input("Genero musical: ").strip()',
        '        pop = pedir_entero_rango("Popularidad (1 al 100): ", 1, 100)',
        "        if tipo == 1:",
        '            lista_artistas.append(Cantante(nom, gen, pop, input("Cancion mas popular: ")))',
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

    draw_text_line("6. Conclusion", margin_x, cur_y, FONT_TITLE, COLOR_BLACK)
    cur_y -= 18
    concl_text = (
        "El desarrollo de este programa permitio constatar de forma practica la utilidad de la herencia para "
        "evitar la redundancia de codigo, centralizando los atributos y metodos comunes en la clase padre Artista. "
        "A su vez, el polimorfismo hizo posible que la funcion iniciar_festival ejecute el metodo actuar() de cada "
        "objeto segun su clase especifica, sin requerir condicionales ni acoplamiento, logrando una arquitectura "
        "modular, escalable y mantenible."
    )
    draw_paragraph(concl_text, margin_x, cur_y, content_w, font=FONT_TEXT, line_spacing=3.0)

    doc.insertPage_atIndex_(close_page(p4), 3)

    output_pdf = "/Users/joaquingarcia/festival_musica/Actividad_Festival_Musica_POO.pdf"
    doc.writeToFile_(output_pdf)
    print(f"PDF generado sin emojis: {output_pdf}")
    print(f"Total de paginas: {doc.pageCount()}")


if __name__ == "__main__":
    build_pdf()
