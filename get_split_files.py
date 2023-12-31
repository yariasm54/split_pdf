# Standard Libraries
from io import BytesIO

# Thirdparty Libraries
import PyPDF2
import zipfile
import pandas as pd
from IPython.display import display, FileLink

# Own Libraries
from get_df_name_files import get_df
from get_pages_to_divide import get_pages

def get_split(excel_data, pdf_data):
    pdf_file = BytesIO(pdf_data)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    paginas_de_division, ID_por_pagina = get_pages(pdf_file)
    df = get_df(excel_data)
    pagina_actual = 0
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for i, pagina_num in enumerate(paginas_de_division):
            pdf_writer = PyPDF2.PdfWriter()
            while pagina_actual < pagina_num:
                pagina = pdf_reader.pages[pagina_actual]
                pdf_writer.add_page(pagina)
                pagina_actual += 1
            try:
                nombre_nuevo_archivo = df.loc[df['ID. INSCRIPCIÓN'] == int(ID_por_pagina[pagina_num]), 'NOMBRE DE ARCHIVO'].values[0]
            except:
                nombre_nuevo_archivo = int(ID_por_pagina[pagina_num])
            nuevo_archivo = f'{nombre_nuevo_archivo}.pdf'
            with BytesIO() as nuevo_pdf:
                pdf_writer.write(nuevo_pdf)
                nuevo_pdf.seek(0)
                zipf.writestr(nuevo_archivo, nuevo_pdf.read())
        if pagina_actual < len(pdf_reader.pages):
            pdf_writer = PyPDF2.PdfWriter()
            while pagina_actual < len(pdf_reader.pages):
                pagina = pdf_reader.pages[pagina_actual]
                pdf_writer.add_page(pagina)
                pagina_actual += 1
            nuevo_archivo = f'{len(paginas_de_division) + 1}.pdf'
            with BytesIO() as nuevo_pdf:
                pdf_writer.write(nuevo_pdf)
                nuevo_pdf.seek(0)
                zipf.writestr(nuevo_archivo, nuevo_pdf.read())
    zip_buffer.seek(0)
    with open('archivo_comprimido.zip', 'wb') as f:
        f.write(zip_buffer.read())
    print("\nDivisión completada y archivo ZIP generado.")
