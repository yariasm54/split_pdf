# Standard Libraries
from io import BytesIO

# Thirdparty Libraries
import pandas as pd

def get_df(pdf_data):
    archivo_excel = BytesIO(pdf_data)
    df = pd.read_excel(archivo_excel)
    return df
