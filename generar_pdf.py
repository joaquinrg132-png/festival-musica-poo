#!/usr/bin/env python3
"""
Generador del Documento PDF para la Actividad de Herencia y Polimorfismo
"""
import os
import html
import AppKit
import Foundation
import pypdf

def generar_documento_pdf():
    main_py_path = "/Users/joaquingarcia/festival_musica/main.py"
    with open(main_py_path, "r", encoding="utf-8") as f:
        codigo_python = f.read()

    codigo_escapado = html.escape(codigo_python)

    captura1_path = "file:///Users/joaquingarcia/festival_musica/capturas/captura_1_registro.png"
    captura2_path = "file:///Users/joaquingarcia/festival_musica/capturas/captura_2_festival.png"
    repo_url = "https://github.com/joaquinrg132-png/festival-musica-poo"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #24292e;
        line-height: 1.5;
        font-size: 11pt;
        margin: 0;
        padding: 0;
    }}
    .header {{
        border-bottom: 3px solid #0366d6;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }}
    .inst-title {{
        font-size: 15pt;
        font-weight: bold;
        color: #1b365d;
        margin: 0 0 4px 0;
        text-transform: uppercase;
    }}
    .sub-title {{
        font-size: 13pt;
        font-weight: 600;
        color: #0366d6;
        margin: 0 0 4px 0;
    }}
    .activity-name {{
        font-size: 11pt;
        color: #586069;
        margin: 0;
    }}
    .meta-box {{
        background-color: #f6f8fa;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 22px;
    }}
    .meta-row {{
        margin: 4px 0;
        font-size: 10.5pt;
    }}
    .meta-label {{
        font-weight: bold;
        color: #24292e;
    }}
    .repo-link {{
        color: #0366d6;
        font-weight: bold;
        text-decoration: underline;
    }}
    h2 {{
        font-size: 13pt;
        color: #1b365d;
        border-bottom: 1px solid #e1e4e8;
        padding-bottom: 6px;
        margin-top: 24px;
        margin-bottom: 12px;
    }}
    p, li {{
        font-size: 10.5pt;
        color: #24292e;
    }}
    ul {{
        margin-top: 6px;
        margin-bottom: 12px;
        padding-left: 24px;
    }}
    .code-block {{
        background-color: #f6f8fa;
        border: 1px solid #d1d5da;
        border-radius: 6px;
        padding: 12px;
        font-family: "Courier New", Courier, monospace;
        font-size: 8.5pt;
        line-height: 1.35;
        white-space: pre-wrap;
        color: #24292e;
        margin-bottom: 20px;
    }}
    .image-card {{
        margin-bottom: 25px;
        text-align: center;
    }}
    .image-caption {{
        font-size: 9.5pt;
        font-style: italic;
        color: #586069;
        margin-top: 6px;
    }}
    .page-break {{
        page-break-before: always;
    }}
</style>
</head>
<body>

<div class="header">
    <div class="inst-title">Tecnológico Nacional de México</div>
    <div class="sub-title">Instituto Tecnológico de Aguascalientes</div>
    <div class="activity-name">Materia: Programación Orientada a Objetos | Actividad: Simulación de Festival de Música</div>
</div>

<div class="meta-box">
    <div class="meta-row"><span class="meta-label">Estudiante:</span> Joaquín García</div>
    <div class="meta-row"><span class="meta-label">Tema:</span> Herencia, Polimorfismo y Constructores en Python</div>
    <div class="meta-row"><span class="meta-label">Repositorio de GitHub:</span> <a class="repo-link" href="{repo_url}">{repo_url}</a></div>
</div>

<h2>1. Objetivo y Fundamentación Teórica</h2>
<p>
El objetivo de esta práctica es diseñar e implementar un programa orientado a objetos que simula un festival musical interactivo, aplicando rigurosamente los dos pilares fundamentales de la POO solicitados:
</p>
<ul>
    <li><b>Herencia:</b> Se definió una clase base <code>Artista</code> con los atributos comunes (<code>nombre</code>, <code>genero</code>, <code>popularidad</code>) y métodos esenciales (<code>presentarse</code>, <code>actuar</code>, <code>despedirse</code>). A partir de ella se derivaron las subclases especializadas <code>Cantante</code>, <code>DJ</code> y <code>Banda</code>, cada una utilizando la función <code>super().__init__(...)</code> para inicializar los atributos heredados y añadiendo sus propios atributos específicos (<code>cancion_mas_popular</code>, <code>estilo</code> e <code>integrantes</code>, respectivamente).</li>
    <li><b>Polimorfismo:</b> Cada subclase sobreescribió el método <code>actuar()</code> con una implementación personalizada. En la función <code>iniciar_festival(lista_artistas)</code>, se recorre la colección de artistas y se invoca <code>actuar()</code> de manera uniforme sin evaluar condicionales de tipo (<code>isinstance</code> o comparaciones de clase), permitiendo que cada objeto responda según su propia forma de actuar.</li>
</ul>

<h2>2. Repositorio de GitHub</h2>
<p>
El código fuente del proyecto se encuentra disponible de forma pública en el siguiente enlace:
<br>
🌐 <a class="repo-link" href="{repo_url}">{repo_url}</a>
</p>

<h2>3. Capturas de Pantalla de la Ejecución</h2>
<p>
A continuación se muestran las capturas de la terminal ejecutando el programa con los tres tipos de artistas (Cantante, DJ y Banda):
</p>

<div class="image-card">
    <img src="{captura1_path}" width="540" />
    <div class="image-caption">Figura 1: Registro interactivo de artistas solicitando atributos comunes y atributos específicos por subclase.</div>
</div>

<div class="image-card">
    <img src="{captura2_path}" width="540" />
    <div class="image-caption">Figura 2: Ejecución del festival aplicando polimorfismo en actuar() y separación entre actos con “🎆 Fin de la actuación 🎆”.</div>
</div>

<h2>4. Código Fuente Completo (<code>main.py</code>)</h2>
<p>Implementación en Python con validación de entradas, jerarquía de clases y función polimórfica:</p>

<div class="code-block">{codigo_escapado}</div>

</body>
</html>
"""

    data = html_content.encode("utf-8")
    options = {
        AppKit.NSDocumentTypeDocumentAttribute: AppKit.NSHTMLTextDocumentType,
        AppKit.NSCharacterEncodingDocumentAttribute: Foundation.NSUTF8StringEncoding,
        AppKit.NSBaseURLDocumentOption: Foundation.NSURL.fileURLWithPath_("/Users/joaquingarcia/festival_musica/")
    }

    attr_str, _, err = AppKit.NSAttributedString.alloc().initWithData_options_documentAttributes_error_(
        Foundation.NSData.dataWithBytes_length_(data, len(data)),
        options,
        None,
        None
    )

    if not attr_str:
        print(f"Error cargando HTML: {err}")
        return

    # Dimensiones de página tamaño Carta (Letter: 612 x 792 pt)
    frame = Foundation.NSMakeRect(0, 0, 540, 720)
    text_view = AppKit.NSTextView.alloc().initWithFrame_(frame)
    text_view.textStorage().setAttributedString_(attr_str)

    output_pdf_path = "/Users/joaquingarcia/festival_musica/Actividad_Festival_Musica_POO.pdf"

    print_info = AppKit.NSPrintInfo.sharedPrintInfo().copy()
    print_info.setPaperSize_(Foundation.NSMakeSize(612, 792))
    print_info.setTopMargin_(36)
    print_info.setBottomMargin_(36)
    print_info.setLeftMargin_(36)
    print_info.setRightMargin_(36)
    print_info.dictionary()[AppKit.NSPrintJobDisposition] = AppKit.NSPrintSaveJob
    print_info.dictionary()[AppKit.NSPrintSavePath] = output_pdf_path

    op = AppKit.NSPrintOperation.printOperationWithView_printInfo_(text_view, print_info)
    op.setShowsPrintPanel_(False)
    op.setShowsProgressPanel_(False)
    success = op.runOperation()

    if success:
        reader = pypdf.PdfReader(output_pdf_path)
        print(f"✅ PDF generado exitosamente: {output_pdf_path}")
        print(f"📄 Número total de páginas: {len(reader.pages)}")
        print(f"📊 Tamaño del archivo: {os.path.getsize(output_pdf_path) / 1024:.1f} KB")
    else:
        print("❌ Falló la generación del PDF.")

if __name__ == "__main__":
    generar_documento_pdf()
