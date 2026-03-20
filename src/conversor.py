import pandas as pd
from pathlib import Path
import re
import logging


# Configuração básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def eh_arquivo_valido(nome_arquivo: str) -> bool:
    """
    Verifica se o nome do arquivo (sem extensão) segue o padrão 'CelularesSubtraidos_ano'.
    """
    padrao = re.compile(r"^CelularesSubtraidos_\d{4}$", re.IGNORECASE)
    return bool(padrao.match(nome_arquivo))

def identificar_aba_alvo(nome_abas: list[str]) -> str | None:
    """
    Busca a aba utilizando o padrão 'CELULAR_YYYY', ignorando maiúsculas, minúsculas e espaços.
    """
    padrao = re.compile(r"^CELULAR(ES)?_\d{4}$", re.IGNORECASE)
    
    for aba in nome_abas:
        if padrao.match(aba.strip()):
            return aba
    return None

def converter_excel_para_csv(caminho_entrada: str | Path, diretorio_saida: str | Path) -> Path:
    """
    Lê a aba correta e exporta para CSV mantendo o nome original e formato exato dos dados.
    """
    caminho_entrada = Path(caminho_entrada)
    diretorio_saida = Path(diretorio_saida)
    
    if not eh_arquivo_valido(caminho_entrada.stem):
        raise ValueError(f"O arquivo '{caminho_entrada.name}' não segue o padrão 'CelularesSubtraidos_ano'.")
    
    arquivo_excel = pd.ExcelFile(caminho_entrada)
    aba_alvo = identificar_aba_alvo(arquivo_excel.sheet_names)
    
    if not aba_alvo:
        raise ValueError(f"Nenhuma aba com o padrão 'CELULAR_YYYY' encontrada. Abas existentes no arquivo: {arquivo_excel.sheet_names}")
    
    df = arquivo_excel.parse(sheet_name=aba_alvo)
    caminho_saida = diretorio_saida / f"{caminho_entrada.stem}.csv"
    
    # MUDANÇA AQUI: Adicionado date_format para preservar a integridade exata das datas e horários
    df.to_csv(caminho_saida, index=False, encoding='utf-8', date_format='%Y-%m-%d %H:%M:%S')
    
    return caminho_saida

def processamento_em_massa(lista_arquivos: list[str | Path], diretorio_saida: str | Path) -> dict:
    """
    Processa arquivos em lote, filtrando apenas os que possuem nomes válidos.
    """
    diretorio_saida = Path(diretorio_saida)
    diretorio_saida.mkdir(parents=True, exist_ok=True)
    
    relatorio = {'sucessos': 0, 'falhas': 0, 'ignorados': 0, 'erros': []}
    
    for arquivo in lista_arquivos:
        caminho_arquivo = Path(arquivo)
        
        if not eh_arquivo_valido(caminho_arquivo.stem):
            logging.info(f"Ignorado: '{caminho_arquivo.name}' não é um arquivo alvo.")
            relatorio['ignorados'] += 1
            continue

        try:
            converter_excel_para_csv(arquivo, diretorio_saida)
            logging.info(f"Sucesso: '{caminho_arquivo.name}' convertido para CSV.")
            relatorio['sucessos'] += 1
        except Exception as e:
            logging.error(f"Falha ao processar '{caminho_arquivo.name}': {e}")
            relatorio['falhas'] += 1
            relatorio['erros'].append((arquivo, str(e)))
            
    return relatorio