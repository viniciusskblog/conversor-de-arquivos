import pytest
import pandas as pd
from pathlib import Path
from src.conversor import (
    identificar_aba_alvo, 
    eh_arquivo_valido, 
    converter_excel_para_csv, 
    processamento_em_massa,
)


@pytest.fixture
def ambiente_arquivos(tmp_path):
    dir_entrada = tmp_path / "entrada"
    dir_saida = tmp_path / "saida"
    dir_entrada.mkdir()
    dir_saida.mkdir()

    # Cenário 1: Arquivo PERFEITO (Aba toda em maiúsculo: CELULAR_2026)
    arquivo_valido = dir_entrada / "CelularesSubtraidos_2026.xlsx"
    with pd.ExcelWriter(arquivo_valido) as writer:
        pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='Metodologia', index=False)
        pd.DataFrame({'ID': [1, 2], 'Valor': [100, 200]}).to_excel(writer, sheet_name='CELULAR_2026', index=False)
        pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='Dicionário de dados', index=False)

    # Cenário 2: Arquivo com NOME INVÁLIDO
    arquivo_nome_invalido = dir_entrada / "dados_regiao_sul.xlsx"
    with pd.ExcelWriter(arquivo_nome_invalido) as writer:
        pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='CELULAR_2026', index=False)

    # Cenário 3: Arquivo com NOME VÁLIDO (mas SEM a aba alvo)
    arquivo_sem_aba = dir_entrada / "CelularesSubtraidos_2025.xlsx"
    with pd.ExcelWriter(arquivo_sem_aba) as writer:
        pd.DataFrame({'A': [1]}).to_excel(writer, sheet_name='Metodologia', index=False)

    return dir_entrada, dir_saida, arquivo_valido, arquivo_nome_invalido, arquivo_sem_aba

# --- Testes Unitários ---
def test_eh_arquivo_valido():
    assert eh_arquivo_valido("CelularesSubtraidos_2026") is True
    assert eh_arquivo_valido("CELULARESsubtraidos_2024") is True # Testa case insensitive no nome do arquivo
    assert eh_arquivo_valido("Celulares_2026") is False
    assert eh_arquivo_valido("dados_teste") is False

def test_identificar_aba_alvo():
    # Testa tudo maiúsculo
    assert identificar_aba_alvo(['Metodologia', 'CELULAR_2026', 'Outra']) == 'CELULAR_2026'
    
    # Testa tudo minúsculo com espaço no final
    assert identificar_aba_alvo(['Metodologia', 'celular_2026 ', 'Outra']) == 'celular_2026 '
    
    # Testa capitalizado no plural
    assert identificar_aba_alvo(['Metodologia', 'Celulares_2026', 'Outra']) == 'Celulares_2026'
    
    # Testa falha
    assert identificar_aba_alvo(['Metodologia', 'Aba_Errada', 'Outra']) is None

# --- Testes de Funcionalidade ---
def test_converter_excel_para_csv_sucesso(ambiente_arquivos):
    _, dir_saida, arquivo_valido, _, _ = ambiente_arquivos
    
    arquivo_csv = converter_excel_para_csv(arquivo_valido, dir_saida)
    
    assert arquivo_csv.exists()
    assert arquivo_csv.name == "CelularesSubtraidos_2026.csv" 
    
    df_convertido = pd.read_csv(arquivo_csv)
    assert list(df_convertido.columns) == ['ID', 'Valor']

def test_converter_excel_para_csv_falha_nome_invalido(ambiente_arquivos):
    _, dir_saida, _, arquivo_nome_invalido, _ = ambiente_arquivos
    
    with pytest.raises(ValueError, match="não segue o padrão 'CelularesSubtraidos_ano'"):
        converter_excel_para_csv(arquivo_nome_invalido, dir_saida)

# --- Testes de Integração ---
def test_processamento_em_massa(ambiente_arquivos):
    dir_entrada, dir_saida, _, _, _ = ambiente_arquivos
    arquivos_entrada = list(dir_entrada.glob("*.xlsx"))
    
    relatorio = processamento_em_massa(arquivos_entrada, dir_saida)
    
    assert relatorio['sucessos'] == 1
    assert relatorio['falhas'] == 1
    assert relatorio['ignorados'] == 1
    assert len(list(dir_saida.glob("*.csv"))) == 1