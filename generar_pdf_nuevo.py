#!/usr/bin/env python3
"""
Generador del Documento PDF Oficial de la Actividad
Utiliza PDFKit y AppKit con renderizado de alta resolución (2x Retina).
"""
import os
import Quartz.PDFKit as PDFKit
import AppKit
import Foundation

PAGE_W = 612
PAGE_H = 792
SCALE = 2  # 2x Retina resolution

def create_page_canvas():
    """Crea una imagen de alta resolución para una página."""
    img = AppKit.NSImage.alloc().initWithSize_((PAGE_W * SCALE, PAGE_H * SCALE))
    img.lockFocus()

    # Escalar contexto a 2x
    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.saveGraphicsState()
    transform = AppKit.NSAffineTransform.transform()
    transform.scaleBy_(SCALE)
    transform.concat()

    # Fondo blanco
    AppKit.NSColor.whiteColor().set()
    AppKit.NSBezierPath.fillRect_(((0, 0), (PAGE_W, PAGE_H)))

    return img

def close_page_canvas(img):
    """Cierra el contexto y ajusta el tamaño a puntos PDF."""
    ctx = AppKit.NSGraphicsContext.currentContext()
    ctx.restoreGraphicsState()
    img.unlockFocus()
    img.setSize_((PAGE_W, PAGE_H))
    return PDFKit.PDFPage.alloc().initWithImage_(img)

def draw_header_footer(page_num, total_pages=4):
    """Dibuja encabezado y pie de página institucional."""
    # Línea superior azul institucional
    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.25, 0.50, 1.0).set()
    AppKit.NSBezierPath.fillRect_(((40, PAGE_H - 35), (PAGE_W - 80, 2)))

    # Texto encabezado
    h_font = AppKit.NSFont.systemFontOfSize_(8.5)
    h_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.35, 0.40, 0.45, 1.0)
    h_attrs = {AppKit.NSFontAttributeName: h_font, AppKit.NSForegroundColorAttributeName: h_color}
    h_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(
        "TecNM — Instituto Tecnológico de Aguascalientes | Programación Orientada a Objetos", h_attrs
    )
    h_str.drawAtPoint_((40, PAGE_H - 30))

    # Pie de página
    f_str = AppKit.NSAttributedString.alloc().initWithString_attributes_(
        f"Página {page_num} de {total_pages}", h_attrs
    )
    f_str.drawAtPoint_((PAGE_W - 100, 25))

    # Línea pie
    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.85, 0.85, 0.88, 1.0).set()
    AppKit.NSBezierPath.fillRect_(((40, 38), (PAGE_W - 80, 1)))

def draw_text(text, x, y, font, color, max_w=None):
    attrs = {AppKit.NSFontAttributeName: font, AppKit.NSForegroundColorAttributeName: color}
    if max_w:
        style = AppKit.NSMutableParagraphStyle.alloc().init()
        style.setLineSpacing_(3.0)
        attrs[AppKit.NSParagraphStyleAttributeName] = style
        rect = Foundation.NSMakeRect(x, y - 200, max_w, 200) # bounding box
        s = AppKit.NSAttributedString.alloc().initWithString_attributes_(text, attrs)
        size = s.boundingRectWithSize_options_((max_w, 1000), AppKit.NSStringDrawingUsesLineFragmentOrigin).size
        actual_rect = Foundation.NSMakeRect(x, y - size.height, max_w, size.height)
        s.drawInRect_(actual_rect)
        return size.height
    else:
        s = AppKit.NSAttributedString.alloc().initWithString_attributes_(text, attrs)
        s.drawAtPoint_((x, y))
        return s.size().height

def draw_box(x, y, w, h, bg_color, border_color=None, radius=4.0):
    bg_color.set()
    path = AppKit.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(((x, y), (w, h)), radius, radius)
    path.fill()
    if border_color:
        border_color.set()
        path.setLineWidth_(1.0)
        path.stroke()

def draw_code_block(lines, x, y, w, line_h=12.5, font_size=8.0):
    total_h = len(lines) * line_h + 16
    draw_box(
        x, y - total_h, w, total_h,
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.96, 0.97, 0.98, 1.0),
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.82, 0.85, 0.88, 1.0),
        radius=4.0
    )
    code_font = AppKit.NSFont.fontWithName_size_("Menlo", font_size) or AppKit.NSFont.userFixedPitchFontOfSize_(font_size)
    text_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.15, 0.17, 0.20, 1.0)

    cur_y = y - 14
    for line in lines:
        attrs = {AppKit.NSFontAttributeName: code_font, AppKit.NSForegroundColorAttributeName: text_color}
        s = AppKit.NSAttributedString.alloc().initWithString_attributes_(line, attrs)
        s.drawAtPoint_((x + 10, cur_y - font_size))
        cur_y -= line_h
    return total_h

def build_pdf():
    doc = PDFKit.PDFDocument.alloc().init()

    # =========================================================================
    # PÁGINA 1: Portada, Datos, Fundamentación Teórica y Enlace GitHub
    # =========================================================================
    p1 = create_page_canvas()
    draw_header_footer(1, 4)

    # Título Principal
    draw_text(
        "REPORTE DE PRÁCTICA: FESTIVAL DE MÚSICA",
        40, PAGE_H - 70,
        AppKit.NSFont.boldSystemFontOfSize_(16),
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0)
    )
    draw_text(
        "Tema: Herencia y Polimorfismo en Programación Orientada a Objetos",
        40, PAGE_H - 90,
        AppKit.NSFont.systemFontOfSize_(11),
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.01, 0.40, 0.84, 1.0)
    )

    # Cuadro de Metadatos
    draw_box(
        40, PAGE_H - 180, PAGE_W - 80, 75,
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.95, 0.97, 1.0, 1.0),
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.75, 0.85, 0.95, 1.0),
        radius=6.0
    )
    draw_text("Estudiante: Joaquín García", 55, PAGE_H - 125, AppKit.NSFont.boldSystemFontOfSize_(10), AppKit.NSColor.blackColor())
    draw_text("Institución: Tecnológico Nacional de México — Instituto Tecnológico de Aguascalientes", 55, PAGE_H - 140, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.darkGrayColor())
    draw_text("Materia: Programación Orientada a Objetos | Lenguaje: Python 3", 55, PAGE_H - 155, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.darkGrayColor())
    draw_text("Repositorio GitHub: https://github.com/joaquinrg132-png/festival-musica-poo", 55, PAGE_H - 170, AppKit.NSFont.boldSystemFontOfSize_(9.5), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.01, 0.40, 0.84, 1.0))

    # Sección 1: Objetivo
    cur_y = PAGE_H - 200
    draw_text("1. Objetivo de la Actividad", 40, cur_y, AppKit.NSFont.boldSystemFontOfSize_(12), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    cur_y -= 18
    obj_text = (
        "El objetivo es diseñar e implementar un programa orientado a objetos en Python que simule un festival musical "
        "con diversos tipos de artistas (Cantante, DJ, Banda), aplicando rigurosamente los conceptos de Herencia, "
        "Polimorfismo y constructores para permitir que cada participante se presente, actúe y se despida con su propia identidad."
    )
    h_used = draw_text(obj_text, 40, cur_y, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.blackColor(), max_w=PAGE_W - 80)
    cur_y -= (h_used + 18)

    # Sección 2: Fundamentación Teórica
    draw_text("2. Fundamentación Teórica y Arquitectura", 40, cur_y, AppKit.NSFont.boldSystemFontOfSize_(12), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    cur_y -= 18

    p_herencia = (
        "• Herencia (Clase Base y Subclases):\n"
        "  Se implementó la clase base 'Artista' que encapsula los atributos comunes: nombre, género y popularidad (1 a 100), "
        "  así como los métodos presentarse(), actuar() y despedirse(). Las subclases 'Cantante', 'DJ' y 'Banda' extienden de Artista "
        "  y utilizan super().__init__(nombre, genero, popularidad) para reutilizar la lógica de inicialización, agregando atributos "
        "  específicos como cancion_mas_popular, estilo e integrantes."
    )
    h_used = draw_text(p_herencia, 40, cur_y, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.blackColor(), max_w=PAGE_W - 80)
    cur_y -= (h_used + 14)

    p_polimorfismo = (
        "• Polimorfismo y Sobrescritura de Métodos:\n"
        "  Cada subclase sobrescribe el método actuar() adaptando su comportamiento particular. En la función iniciar_festival(lista_artistas), "
        "  se itera sobre la colección invocando presentarse(), actuar() y despedirse() de forma uniforme. Esto cumple con el principio de "
        "  polimorfismo puro, eliminando por completo sentencias condicionales (if/elif) para discriminar el tipo de objeto en tiempo de ejecución."
    )
    h_used = draw_text(p_polimorfismo, 40, cur_y, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.blackColor(), max_w=PAGE_W - 80)
    cur_y -= (h_used + 20)

    # Cuadro Enlace GitHub Destacado
    draw_box(
        40, cur_y - 50, PAGE_W - 80, 48,
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.94, 0.98, 0.94, 1.0),
        AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.65, 0.85, 0.65, 1.0),
        radius=5.0
    )
    draw_text("🔗 ENLACE OFICIAL AL REPOSITORIO DE GITHUB (PÚBLICO)", 55, cur_y - 18, AppKit.NSFont.boldSystemFontOfSize_(9.5), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.15, 0.50, 0.20, 1.0))
    draw_text("https://github.com/joaquinrg132-png/festival-musica-poo", 55, cur_y - 34, AppKit.NSFont.boldSystemFontOfSize_(10.5), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.01, 0.40, 0.84, 1.0))

    doc.insertPage_atIndex_(close_page_canvas(p1), 0)

    # =========================================================================
    # PÁGINA 2: Capturas de Pantalla de la Ejecución
    # =========================================================================
    p2 = create_page_canvas()
    draw_header_footer(2, 4)

    draw_text("3. Evidencias de Ejecución del Programa", 40, PAGE_H - 70, AppKit.NSFont.boldSystemFontOfSize_(14), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    draw_text("Capturas reales de la terminal interactiva demostrando el registro y la ejecución polimórfica:", 40, PAGE_H - 88, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.darkGrayColor())

    # Cargar y dibujar Captura 1 (Registro)
    cap1_img = AppKit.NSImage.alloc().initWithContentsOfFile_("/Users/joaquingarcia/festival_musica/capturas/captura_1_registro.png")
    if cap1_img:
        cap_w = PAGE_W - 80
        cap_h = cap_w * (620.0 / 860.0) * 0.72  # proporción de aspecto
        y_pos = PAGE_H - 110 - cap_h
        cap1_img.drawInRect_fromRect_operation_fraction_(((40, y_pos), (cap_w, cap_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
        draw_text("Figura 1: Registro interactivo de artistas solicitando nombre, género, popularidad (1-100) y atributos específicos.", 40, y_pos - 15, AppKit.NSFont.systemFontOfSize_(8.5), AppKit.NSColor.darkGrayColor())

    # Cargar y dibujar Captura 2 (Festival)
    cap2_img = AppKit.NSImage.alloc().initWithContentsOfFile_("/Users/joaquingarcia/festival_musica/capturas/captura_2_festival.png")
    if cap2_img:
        y_pos2 = y_pos - 35 - cap_h
        cap2_img.drawInRect_fromRect_operation_fraction_(((40, y_pos2), (cap_w, cap_h)), Foundation.NSZeroRect, AppKit.NSCompositeSourceOver, 1.0)
        draw_text("Figura 2: Invocación polimórfica de actuar() para Cantante, DJ y Banda con separador de actuaciones.", 40, y_pos2 - 15, AppKit.NSFont.systemFontOfSize_(8.5), AppKit.NSColor.darkGrayColor())

    doc.insertPage_atIndex_(close_page_canvas(p2), 1)

    # =========================================================================
    # PÁGINA 3: Código Fuente (main.py) - Parte 1
    # =========================================================================
    p3 = create_page_canvas()
    draw_header_footer(3, 4)

    draw_text("4. Código Fuente Completo (Parte 1: Clases y Herencia)", 40, PAGE_H - 70, AppKit.NSFont.boldSystemFontOfSize_(14), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    draw_text("Definición de la clase base Artista y las subclases especializadas Cantante, DJ y Banda:", 40, PAGE_H - 88, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.darkGrayColor())

    codigo_p1 = [
        '# ============================================================',
        '# 1️⃣ CLASE BASE: Artista',
        '# ============================================================',
        'class Artista:',
        '    """Clase base que representa a un artista musical genérico."""',
        '    def __init__(self, nombre: str, genero: str, popularidad: int):',
        '        self.nombre = nombre',
        '        self.genero = genero',
        '        self.popularidad = popularidad',
        '',
        '    def presentarse(self):',
        '        print(f"🎤 ¡Hola a todos! Soy {self.nombre}, exponente de {self.genero} (Popularidad: {self.popularidad}/100).")',
        '',
        '    def actuar(self):',
        '        """Método base que será sobrescrito por cada subclase (polimorfismo)."""',
        '        print(f"🎵 {self.nombre} está realizando una presentación en el escenario.")',
        '',
        '    def despedirse(self):',
        '        print(f"👋 ¡Muchas gracias por su energía! Se despide {self.nombre}. ¡Hasta la próxima!")',
        '',
        '# ============================================================',
        '# 2️⃣ SUBCLASES DE Artista (HERENCIA Y POLIMORFISMO)',
        '# ============================================================',
        'class Cantante(Artista):',
        '    """Subclase que representa a un cantante solista."""',
        '    def __init__(self, nombre: str, genero: str, popularidad: int, cancion_mas_popular: str):',
        '        super().__init__(nombre, genero, popularidad)  # Llamada al constructor padre',
        '        self.cancion_mas_popular = cancion_mas_popular',
        '',
        '    def actuar(self):',
        '        print(f"🎶 {self.nombre} canta su éxito {self.cancion_mas_popular} con gran energía.")',
        '',
        'class DJ(Artista):',
        '    """Subclase que representa a un DJ."""',
        '    def __init__(self, nombre: str, genero: str, popularidad: int, estilo: str):',
        '        super().__init__(nombre, genero, popularidad)  # Llamada al constructor padre',
        '        self.estilo = estilo',
        '',
        '    def actuar(self):',
        '        print(f"🎧 El DJ {self.nombre} mezcla temas de estilo {self.estilo}, haciendo vibrar al público.")',
        '',
        'class Banda(Artista):',
        '    """Subclase que representa a una banda musical."""',
        '    def __init__(self, nombre: str, genero: str, popularidad: int, integrantes: int):',
        '        super().__init__(nombre, genero, popularidad)  # Llamada al constructor padre',
        '        self.integrantes = integrantes',
        '',
        '    def actuar(self):',
        '        print(f"🎸 La banda {self.nombre} con {self.integrantes} integrantes toca un poderoso solo de guitarra.")'
    ]

    draw_code_block(codigo_p1, 40, PAGE_H - 105, PAGE_W - 80, line_h=11.2, font_size=7.5)
    doc.insertPage_atIndex_(close_page_canvas(p3), 2)

    # =========================================================================
    # PÁGINA 4: Código Fuente (main.py) - Parte 2 y Conclusiones
    # =========================================================================
    p4 = create_page_canvas()
    draw_header_footer(4, 4)

    draw_text("4. Código Fuente (Parte 2: Función Polimórfica y main)", 40, PAGE_H - 70, AppKit.NSFont.boldSystemFontOfSize_(14), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    draw_text("Implementación de iniciar_festival() y función interactiva de captura de datos:", 40, PAGE_H - 88, AppKit.NSFont.systemFontOfSize_(9.5), AppKit.NSColor.darkGrayColor())

    codigo_p2 = [
        '# ============================================================',
        '# 3️⃣ FUNCIÓN DE INICIO DEL FESTIVAL (POLIMORFISMO PURO)',
        '# ============================================================',
        'def iniciar_festival(lista_artistas):',
        '    print("\\n" + "=" * 60)',
        '    print("🎪✨ ¡COMIENZA EL GRAN FESTIVAL DE MÚSICA! ✨🎪")',
        '    print("=" * 60 + "\\n")',
        '    for i, artista in enumerate(lista_artistas, 1):',
        '        print(f"--- [Acto #{i}] ---")',
        '        artista.presentarse()',
        '        artista.actuar()       # Invocación polimórfica: no requiere if/elif',
        '        artista.despedirse()',
        '        print("\\n🎆 Fin de la actuación 🎆\\n" + "-" * 60 + "\\n")',
        '',
        '# ============================================================',
        '# 4️⃣ PROGRAMA PRINCIPAL (main.py)',
        '# ============================================================',
        'def pedir_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:',
        '    while True:',
        '        try:',
        '            val = int(input(mensaje))',
        '            if minimo <= val <= maximo: return val',
        '            print(f"⚠️ Ingresa un número entre {minimo} y {maximo}.")',
        '        except ValueError:',
        '            print("⚠️ Entrada no válida.")',
        '',
        'def main():',
        '    num = pedir_entero_rango("¿Cuántos artistas se presentarán?: ", 1, 50)',
        '    lista_artistas = []',
        '    for i in range(1, num + 1):',
        '        tipo = pedir_entero_rango("Tipo (1. Cantante, 2. DJ, 3. Banda): ", 1, 3)',
        '        nom, gen = input("Nombre: ").strip(), input("Género: ").strip()',
        '        pop = pedir_entero_rango("Popularidad (1 al 100): ", 1, 100)',
        '        if tipo == 1:',
        '            lista_artistas.append(Cantante(nom, gen, pop, input("Canción más popular: ")))',
        '        elif tipo == 2:',
        '            lista_artistas.append(DJ(nom, gen, pop, input("Estilo: ")))',
        '        else:',
        '            lista_artistas.append(Banda(nom, gen, pop, pedir_entero_rango("Integrantes: ", 1, 50)))',
        '    iniciar_festival(lista_artistas)',
        '',
        'if __name__ == "__main__":',
        '    main()'
    ]

    h_code = draw_code_block(codigo_p2, 40, PAGE_H - 105, PAGE_W - 80, line_h=11.2, font_size=7.5)

    # Conclusión final
    y_conc = PAGE_H - 105 - h_code - 20
    draw_text("5. Conclusiones", 40, y_conc, AppKit.NSFont.boldSystemFontOfSize_(11), AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.21, 0.38, 1.0))
    y_conc -= 16
    conc_text = (
        "La implementación demostró exitosamente cómo la herencia permite centralizar atributos y comportamientos comunes "
        "en la clase padre evitando duplicidad, mientras que el polimorfismo faculta al sistema a tratar a cualquier artista de manera "
        "homogénea sin acoplar la función principal a los tipos concretos de las subclases, logrando un código modular, extensible y limpio."
    )
    draw_text(conc_text, 40, y_conc, AppKit.NSFont.systemFontOfSize_(9), AppKit.NSColor.blackColor(), max_w=PAGE_W - 80)

    doc.insertPage_atIndex_(close_page_canvas(p4), 3)

    # Guardar archivo
    output_path = "/Users/joaquingarcia/festival_musica/Actividad_Festival_Musica_POO.pdf"
    doc.writeToFile_(output_path)
    print(f"✅ Nuevo PDF generado con éxito en: {output_path}")
    print(f"📄 Páginas: {doc.pageCount()}")

if __name__ == "__main__":
    build_pdf()
