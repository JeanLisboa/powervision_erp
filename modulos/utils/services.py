import os
import openpyxl

def download_planilha():
    pasta = r"C:\Users\jean.lino\Downloads"  # Substitua pelo caminho da sua pasta
    file_name = "planilha.xlsx"
    file_path = os.path.join(pasta, file_name)

    # Crie a pasta se ela não existir
    os.makedirs(pasta, exist_ok=True)

    # Crie uma nova planilha
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Adicione as colunas à planilha
    columns = [
        "Fornecedor",
        "EAN",
        "Valor",
        "Unidade",
        "Quantidade",
    ]  # Substitua pelos nomes das suas colunas
    sheet.append(columns)

    # Salve a planilha na pasta específica
    workbook.save(file_path)

    print(f"Planilha salva em: {file_path}")
