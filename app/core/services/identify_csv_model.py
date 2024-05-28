import csv
import codecs
from app.core.ports.csv_port import CsvPort
from app.adapters.csv_reader.csv_reader_model1 import CsvReaderModel1
from app.adapters.csv_reader.csv_reader_model2 import CsvReaderModel2
from app.adapters.csv_reader.csv_reader_model3 import CsvReaderModel3
from app.adapters.csv_reader.csv_reader_model4 import CsvReaderModel4

def identify_csv_model(file_path: str) -> CsvPort:
    with codecs.open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader((line.replace('\0', '') for line in csvfile), delimiter=';')
        headers = next(reader)
        headers = [header.strip().lower() for header in headers if header.strip()]
        print(headers)
        model1_headers = {"data", "descrição", "referencia", "nota fiscal", "entrada", "saida"}
        model2_headers = {"data", "descrição", "valor", "descricao"}
        model3_headers = {"data", "descrição", "documento", "crédito", "débito", "saldo"}
        model4_headers = {"data", "descrição", "valor"}
        
        if set(headers) == model1_headers:
            return CsvReaderModel1()
        elif set(headers) == model2_headers:
            return CsvReaderModel2()
        elif set(headers) == model3_headers:
            return CsvReaderModel3()
        elif set(headers) == model4_headers:
            return CsvReaderModel4()
        else:
            raise ValueError("Modelo não reconhecido")
