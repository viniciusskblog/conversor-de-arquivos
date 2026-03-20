import pandas as pd
import numpy as np
from pathlib import Path
from src.conversor import identificar_aba_alvo, eh_arquivo_valido

def auditar_conversao():
    pasta_entrada = Path("data/entrada")
    pasta_saida = Path("data/saida")
    
    arquivos_excel = list(pasta_entrada.glob("*.xlsx"))
    
    print("Iniciando auditoria rigorosa de integridade...\n" + "-"*40)
    
    for caminho_excel in arquivos_excel:
        if not eh_arquivo_valido(caminho_excel.stem):
            continue
            
        caminho_csv = pasta_saida / f"{caminho_excel.stem}.csv"
        
        if not caminho_csv.exists():
            print(f"⚠️ ALERTA: Arquivo CSV não encontrado para '{caminho_excel.name}'.")
            continue
            
        print(f"Auditando: {caminho_excel.name}  <-->  {caminho_csv.name}")
        
        try:
            # 1. Carrega o Excel Original
            arquivo_excel = pd.ExcelFile(caminho_excel)
            aba = identificar_aba_alvo(arquivo_excel.sheet_names)
            df_excel = arquivo_excel.parse(sheet_name=aba)
            
            # 2. MUDANÇA CRÍTICA: Lendo o CSV estritamente como TEXTO
            # O parâmetro dtype=str impede que o Python transforme as coordenadas em floats
            df_csv = pd.read_csv(caminho_csv, dtype=str)
            
            # 3. Formata o Excel para comparar como texto puro
            for col in df_excel.columns:
                if pd.api.types.is_datetime64_any_dtype(df_excel[col]):
                    df_excel[col] = df_excel[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Transforma tudo no Excel em texto para parear com o CSV
            df_excel_str = df_excel.astype(str)
            
            # Padroniza células vazias para não gerar falsos positivos
            df_excel_str = df_excel_str.replace(['nan', 'NaT', 'None', '<NA>', ''], np.nan)
            df_csv = df_csv.replace(['nan', 'NaT', 'None', '<NA>', ''], np.nan)
            
            # --- NOVO TRECHO INSERIDO AQUI ---
            # Extrai e imprime as dimensões (linhas e colunas)
            linhas_ex, colunas_ex = df_excel_str.shape
            linhas_csv, colunas_csv = df_csv.shape
            print(f"   -> Dimensões: Excel ({linhas_ex} linhas x {colunas_ex} colunas) | CSV ({linhas_csv} linhas x {colunas_csv} colunas)")
            # ---------------------------------
            
            # 4. O Teste de Fogo Literal
            pd.testing.assert_frame_equal(df_excel_str, df_csv, check_dtype=False)
            
            print("✅ INTEGRIDADE CONFIRMADA: O CSV é um espelho exato e literal do Excel.\n")
            
        except AssertionError as erro_diferenca:
            print(f"❌ INCONSISTÊNCIA ENCONTRADA: Os dados não batem!")
            print(f"Detalhes técnicos: {erro_diferenca}\n")
        except Exception as e:
            print(f"❌ ERRO na leitura dos arquivos: {e}\n")

if __name__ == "__main__":
    auditar_conversao()