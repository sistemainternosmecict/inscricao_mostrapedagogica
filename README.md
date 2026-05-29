# Inscrições Mostra Pedagógica

## Descrição
Este aplicativo Flask gerencia inscrições, com integração ao Google Drive e Google Docs para automação de documentos.

## Pré-requisitos
- Python 3.8+
- uv (gerenciador de pacotes Python)
- Conta no Google Cloud Platform (GCP).

## Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd inscricoes_mostra_pedagogica
   ```

2. **Instale as dependências usando `uv`:**
   ```bash
   pip install uv
   uv sync
   ```

3. **Configuração do Google Cloud (Conta de Serviço):**
   Para permitir que o `Gide` manipule o Drive e Docs:
   - No Console do Google Cloud, crie um novo projeto ou selecione um existente.
   - Habilite a **Google Drive API** e a **Google Docs API**.
   - Acesse "IAM e administrador" > "Contas de serviço" e crie uma nova conta.
   - Gere uma **chave** para esta conta (formato JSON).
   - Salve o arquivo JSON na raiz do projeto e renomeie-o para `creds.json`.
   - **IMPORTANTE:** Compartilhe a pasta do Google Drive (onde os documentos serão criados) com o e-mail da conta de serviço (encontrado dentro do `creds.json` em `client_email`), dando permissão de **Editor**.

4. **Configuração de Variáveis de Ambiente (`.env`):**
   Crie um arquivo `.env` na raiz para configurações sensíveis ou específicas do ambiente:
   ```bash
   # Exemplo: ID da pasta raiz no Drive onde a estrutura será criada
   SHARED_FOLDER_ID=seu_id_de_pasta_no_drive
   ```
   *Certifique-se de não versionar (commitar) o `creds.json` ou o `.env` (adicione-os ao `.gitignore`).*

## Como Rodar a Aplicação

```bash
# Se necessário, carregue as variáveis de ambiente antes de rodar
uv run app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000/` onde poderá verificar o status da api.

## Endpoints da API

### `POST /inscricao_entrada`

Recebe dados de inscrição, processa-os e utiliza o `Gide` para gerar documentos no Google Docs.

- **URL:** `/inscricao_entrada`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`

## Módulo Gide (`modules/gide.py`)

O `Gide` é responsável pela interação com o ecossistema Google.

### Funcionalidades:
- **`criar_pasta`**: Cria pastas no Drive.
- **`criar_arquivo_docs`**: Cria e popula documentos Docs, incluindo a formatação automática de URLs para links clicáveis.
- **`criar_estrutura_categoria_unidade`**: Organiza documentos em estruturas de pastas hierárquicas.
