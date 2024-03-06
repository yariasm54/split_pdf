# Standard Libraries
import re

# Thirdparty Libraries
import PyPDF2

def get_pages(pdf_file):
    # expresion_regular = r"ID\.(\d+)ProcesodeSelección"
    # expresion_regular = r"porpartedelaspirante(\d+)\,inscritoalempleocon"
    # expresion_regular = r"AUTONo\.(\d+)DE2024"
    expresion_regular = r"aspirante(\d+)\,"
    paginas_de_division = []
    ID_por_pagina = {}
    numero = 0
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # palabras_a_buscar = ["Proyectó:"]
    palabras_a_buscar = ["Revisó:"]
    for pagina_num, pagina in enumerate(pdf_reader.pages):
        contenido = pagina.extract_text()
        texto_limpio = contenido.replace("\n", "").replace(" ", "")
        coincidencia = re.search(expresion_regular, texto_limpio)
        if coincidencia:
            numero = coincidencia.group(1)
        for palabra in palabras_a_buscar:
            if palabra in contenido:
                paginas_de_division.append(pagina_num + 1)
                ID_por_pagina[pagina_num + 1] = numero
                numero = 0
    return paginas_de_division, ID_por_pagina
