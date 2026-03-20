from src.conversor import processamento_em_massa
from pathlib import Path
import time

def executar_pipeline():
    pasta_entrada = Path("data/entrada")
    pasta_saida = Path("data/saida")
    
    # Busca os arquivos Excel
    arquivos = list(pasta_entrada.glob("*.xlsx"))
    
    if not arquivos:
        print("Nenhum arquivo .xlsx encontrado na pasta 'data/entrada'.")
        print("Por favor, adicione os arquivos e tente novamente.")
        return

    print(f"Iniciando conversão de {len(arquivos)} arquivos...")
    inicio = time.time()
    
    # Executa a conversão chamando o nosso script blindado
    resultado = processamento_em_massa(arquivos, pasta_saida)
    
    fim = time.time()
    
    # Exibe o relatório final no terminal
    print("\n--- Relatório Final de Conversão ---")
    print(f"✅ Sucessos: {resultado['sucessos']}")
    print(f"⏭️ Ignorados (nome fora do padrão): {resultado['ignorados']}")
    print(f"❌ Falhas: {resultado['falhas']}")
    
    if resultado['erros']:
        print("\nDetalhes dos erros:")
        for arquivo, erro in resultado['erros']:
            print(f" - {Path(arquivo).name}: {erro}")
            
    print(f"\nTempo total de execução: {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    executar_pipeline()