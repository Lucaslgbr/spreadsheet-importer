import pytest
from app.adapters.csv_reader.csv_reader_model1 import CsvReaderModel1
from app.adapters.csv_reader.csv_reader_model2 import CsvReaderModel2
from app.adapters.csv_reader.csv_reader_model3 import CsvReaderModel3
from app.adapters.csv_reader.csv_reader_model4 import CsvReaderModel4

@pytest.fixture
def sample_csv_file(tmp_path):
    content = "Data;descrição;referencia;nota fiscal;entrada;saida\n01/01/2023;Compra;123;456;100.00;0.00\n"
    file_path = tmp_path / "test_file.csv"
    file_path.write_text(content)
    return file_path

def test_csv_reader_model1(sample_csv_file):
    reader = CsvReaderModel1()
    spreadsheet = reader.read_csv(sample_csv_file)
    assert len(spreadsheet.data) == 1

def test_csv_reader_model2(sample_csv_file):
    content = "Data;descrição;valor;descricao\n01/01/2023;Compra;100.00;item\n"
    sample_csv_file.write_text(content)
    reader = CsvReaderModel2()
    spreadsheet = reader.read_csv(sample_csv_file)
    assert len(spreadsheet.data) == 1

def test_csv_reader_model3(sample_csv_file):
    content = "Data;descrição;documento;crédito;débito;saldo\n01/01/2023;Compra;123;100.00;0.00;100.00\n"
    sample_csv_file.write_text(content)
    reader = CsvReaderModel3()
    spreadsheet = reader.read_csv(sample_csv_file)
    assert len(spreadsheet.data) == 1

def test_csv_reader_model4(sample_csv_file):
    content = "Data;descrição;valor\n01/01/2023;Compra;100.00\n"
    sample_csv_file.write_text(content)
    reader = CsvReaderModel4()
    spreadsheet = reader.read_csv(sample_csv_file)
    assert len(spreadsheet.data) == 1
