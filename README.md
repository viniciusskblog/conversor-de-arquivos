# Conversor de Arquivos

Este projeto é uma aplicação em Python desenvolvida para automatizar a conversão de arquivos Excel (`.xlsx`) para CSV (`.csv`). Ele lê arquivos de um diretório de entrada, processa os dados de forma segura e salva o resultado em um diretório de saída, contando com um rigoroso módulo de auditoria para garantir a total integridade dos dados transformados.

## 📁 Estrutura do Projeto

A arquitetura do projeto foi pensada para manter a separação de responsabilidades:

* **`data/`**: Diretório de armazenamento de arquivos.
  * `entrada/`: Pasta onde os arquivos originais (`.xlsx`) devem ser colocados.
  * `saida/`: Pasta onde os arquivos convertidos (`.csv`) serão gerados.
* **`src/`**: Diretório contendo as regras de negócio.
  * `conversor.py`: Módulo responsável pela lógica de conversão e formatação.
* **`tests/`**: Diretório reservado para testes automatizados.
  * `test_conversor.py`: Testes unitários para validar as funções do `conversor.py`.
* **`main.py`**: Ponto de entrada que orquestra a leitura, conversão e gravação.
* **`auditoria.py`**: Módulo de validação de integridade de dados pós-conversão.
* **`requirements.txt`**: Lista de dependências externas do projeto.

---

## ⚙️ Como funciona cada componente?

### 1. Ponto de Entrada (`main.py`)
Verifica a pasta `data/entrada`, identifica os arquivos pendentes, aciona o módulo de conversão e salva o resultado em `data/saida`.

### 2. O Motor de Conversão (`src/conversor.py`)
Contém as funções que abrem o arquivo de origem, aplicam as regras de transformação de formato e retornam os dados prontos. É isolado para facilitar a manutenção.

### 3. Auditoria e Logs (`auditoria.py`)
Realiza uma comparação célula por célula entre o Excel original e o CSV gerado, garantindo um "espelho perfeito". Ele audita especificamente:
* **Perda de Arquivos:** Verifica se para cada Excel na entrada, foi gerado um CSV correspondente.
* **Mutação de Tipos de Dados:** Lê o CSV estritamente como texto puro (`dtype=str`) para evitar que o Pandas altere números com zeros à esquerda ou modifique identificadores.
* **Corrupção de Datas:** Assegura que as datas foram transpostas para o formato padrão (`YYYY-MM-DD HH:MM:SS`).
* **Dimensões e Nulos:** Confirma se o arquivo final tem o tamanho exato do original e padroniza células vazias para evitar falsos positivos.

### 4. Testes Automatizados (`tests/test_conversor.py`)
Utiliza o framework `pytest` para enviar dados de teste ao `conversor.py` e verificar as saídas, garantindo que futuras atualizações não quebrem o código.

---

## 🚀 Passo a Passo para Execução Local

Siga as instruções abaixo para configurar o projeto do zero na sua máquina, criar o ambiente isolado e realizar as conversões.

### 📋 Pré-requisitos
* **Python 3.13** (ou superior) instalado.
* **Git** (opcional, para clonar via terminal).

### 1. Clonar ou Baixar o Projeto
Traga o código para a sua máquina executando no terminal:

```bash
git clone https://link-do-seu-repositorio.git
cd CONVERSOR-DE-ARQUIVOS
```

### 2. Criar o Ambiente Virtual

```bash
python -m venv venv
```
Isso criará uma pasta chamada `venv` na raiz do projeto.

### 3. Ativar o Ambiente Virtual
O comando para acesso muda dependendo do sistema operacional:

**No Linux ou macOS:**
```bash
source venv/bin/activate
```

**No Windows (CMD ou PowerShell):**
```cmd
venv\Scripts\activate
```
*(Você saberá que deu certo quando aparecer `(venv)` no início da linha do seu terminal).*

### 4. Instalar as Dependências do Projeto
Com o ambiente ativado, você precisa baixar as bibliotecas que fazem o código funcionar (como `pandas`, `numpy` e `pytest`). O arquivo `requirements.txt` tem a lista de todas elas. Para baixar e instalar tudo de uma vez, execute:

```bash
pip install -r requirements.txt
```

### 5. Preparar os Arquivos para Conversão
O projeto não vem com arquivos de dados por padrão. Para realizar a conversão, você deve:

1. Obter os seus arquivos Excel originais (`.xlsx`).
2. Colar esses arquivos dentro da pasta `data/entrada/`.

*(Nota: Certifique-se de que a pasta `data/entrada/` e `data/saida/` existem. Se não existirem, você pode criá-las manualmente).*

### 6. Executar o Conversor
Com tudo configurado e os arquivos na pasta de entrada, rode o script principal:

```bash
python main.py
```
O sistema irá ler os arquivos da pasta de entrada, fazer a conversão e salvar os arquivos `.csv` na pasta `data/saida/`.

### 7. Verificação e Auditoria
Após a execução, o script de auditoria (`auditoria.py`) rodará automaticamente (ou pode ser executado manualmente, dependendo de como o `main.py` está configurado). Acompanhe o terminal: ele fará uma checagem rigorosa, linha por linha, garantindo que o CSV gerado é um espelho perfeito do Excel original. Procure pela mensagem verde de "**✅ INTEGRIDADE CONFIRMADA**".

---

## 🧪 Como rodar os testes automatizados
Sempre que houver uma alteração no código (`src/conversor.py`), é importante garantir que nada quebrou. Para isso, com o ambiente virtual ativado, basta digitar:

```bash
pytest
```
O sistema executará os testes programados na pasta `tests/` e mostrará se todas as lógicas de conversão continuam funcionando corretamente.
