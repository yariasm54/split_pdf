def obtener_df_nombres_archivos(pdf_data):
    archivo_excel = BytesIO(pdf_data)
    df = pd.read_excel(archivo_excel)
    return df
