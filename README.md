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

Formato de entrada

```json
{
  "telefone": "",
  "eixo-tematico": "",
  "inst-diag-integra-tec": "",
  "autorizacao-imagem-item-edital": "",
  "email": "",
  "categoria": "",
  "ue": "",
  "projeto": "",
  "resumo": "",
  "fichasDeInscricao": "",
  "projetoIntegra": "",
  "videoProjeto": "",
  "arquivosComplementares": "",
  "direitoDeImagem": "",
  "numero-participantes": "",
  "1p-nome-completo": "",
  "1p-matricula": "",
  "1p-cpf": "",
  "2p-nome-completo-1": "",
  "2p-matricula-1": "",
  "2p-cpf-1": "",
  "2p-nome-completo-2": "",
  "2p-matricula-2": "",
  "2p-cpf-2": "",
  "3p-nome-completo-1": "",
  "3p-matricula-1": "",
  "3p-cpf-1": "",
  "3p-nome-completo-2": "",
  "3p-matricula-2": "",
  "3p-cpf-2": "",
  "3p-nome-completo-3": "",
  "3p-matricula-3": "",
  "3p-cpf-3": "",
  "4p-nome-completo-1": "",
  "4p-matricula-1": "",
  "4p-cpf-1": "",
  "4p-nome-completo-2": "",
  "4p-matricula-2": "",
  "4p-cpf-2": "",
  "4p-nome-completo-3": "",
  "4p-matricula-3": "",
  "4p-cpf-3": "",
  "4p-nome-completo-4": "",
  "4p-matricula-4": "",
  "4p-cpf-4": "",
  "5p-nome-completo-1": "",
  "5p-matricula-1": "",
  "5p-cpf-1": "",
  "5p-nome-completo-2": "",
  "5p-matricula-2": "",
  "5p-cpf-2": "",
  "5p-nome-completo-3": "",
  "5p-matricula-3": "",
  "5p-cpf-3": "",
  "5p-nome-completo-4": "",
  "5p-matricula-4": "",
  "5p-cpf-4": "",
  "5p-nome-completo-5": "",
  "5p-matricula-5": "",
  "5p-cpf-5": "",
  "6p-nome-completo-1": "",
  "6p-matricula-1": "",
  "6p-cpf-1": "",
  "6p-nome-completo-2": "",
  "6p-matricula-2": "",
  "6p-cpf-2": "",
  "6p-nome-completo-3": "",
  "6p-matricula-3": "",
  "6p-cpf-3": "",
  "6p-nome-completo-4": "",
  "6p-matricula-4": "",
  "6p-cpf-4": "",
  "6p-nome-completo-5": "",
  "6p-matricula-5": "",
  "6p-cpf-5": "",
  "6p-nome-completo-6": "",
  "6p-matricula-6": "",
  "6p-cpf-6": "",
  "7p-nome-completo-1": "",
  "7p-matricula-1": "",
  "7p-cpf-1": "",
  "7p-nome-completo-2": "",
  "7p-matricula-2": "",
  "7p-cpf-2": "",
  "7p-nome-completo-3": "",
  "7p-matricula-3": "",
  "7p-cpf-3": "",
  "7p-nome-completo-4": "",
  "7p-matricula-4": "",
  "7p-cpf-4": "",
  "7p-nome-completo-5": "",
  "7p-matricula-5": "",
  "7p-cpf-5": "",
  "7p-nome-completo-6": "",
  "7p-matricula-6": "",
  "7p-cpf-6": "",
  "7p-nome-completo-7": "",
  "7p-matricula-7": "",
  "7p-cpf-7": "",
  "8p-nome-completo-1": "",
  "8p-matricula-1": "",
  "8p-cpf-1": "",
  "8p-nome-completo-2": "",
  "8p-matricula-2": "",
  "8p-cpf-2": "",
  "8p-nome-completo-3": "",
  "8p-matricula-3": "",
  "8p-cpf-3": "",
  "8p-nome-completo-4": "",
  "8p-matricula-4": "",
  "8p-cpf-4": "",
  "8p-nome-completo-5": "",
  "8p-matricula-5": "",
  "8p-cpf-5": "",
  "8p-nome-completo-6": "",
  "8p-matricula-6": "",
  "8p-cpf-6": "",
  "8p-nome-completo-7": "",
  "8p-matricula-7": "",
  "8p-cpf-7": "",
  "8p-nome-completo-8": "",
  "8p-matricula-8": "",
  "8p-cpf-8": "",
  "9p-nome-completo-1": "",
  "9p-matricula-1": "",
  "9p-cpf-1": "",
  "9p-nome-completo-2": "",
  "9p-matricula-2": "",
  "9p-cpf-2": "",
  "9p-nome-completo-3": "",
  "9p-matricula-3": "",
  "9p-cpf-3": "",
  "9p-nome-completo-4": "",
  "9p-matricula-4": "",
  "9p-cpf-4": "",
  "9p-nome-completo-5": "",
  "9p-matricula-5": "",
  "9p-cpf-5": "",
  "9p-nome-completo-6": "",
  "9p-matricula-6": "",
  "9p-cpf-6": "",
  "9p-nome-completo-7": "",
  "9p-matricula-7": "",
  "9p-cpf-7": "",
  "9p-nome-completo-8": "",
  "9p-matricula-8": "",
  "9p-cpf-8": "",
  "9p-nome-completo-9": "",
  "9p-matricula-9": "",
  "9p-cpf-9": "",
  "10p-nome-completo-1": "",
  "10p-matricula-1": "",
  "10p-cpf-1": "",
  "10p-nome-completo-2": "",
  "10p-matricula-2": "",
  "10p-cpf-2": "",
  "10p-nome-completo-3": "",
  "10p-matricula-3": "",
  "10p-cpf-3": "",
  "10p-nome-completo-4": "",
  "10p-matricula-4": "",
  "10p-cpf-4": "",
  "10p-nome-completo-5": "",
  "10p-matricula-5": "",
  "10p-cpf-5": "",
  "10p-nome-completo-6": "",
  "10p-matricula-6": "",
  "10p-cpf-6": "",
  "10p-nome-completo-7": "",
  "10p-matricula-7": "",
  "10p-cpf-7": "",
  "10p-nome-completo-8": "",
  "10p-matricula-8": "",
  "10p-cpf-8": "",
  "10p-nome-completo-9": "",
  "10p-matricula-9": "",
  "10p-cpf-9": "",
  "10p-nome-completo-10": "",
  "10p-matricula-10": "",
  "10p-cpf-10": ""
}
```

Após o envio, a estrutura é criada no drive configurado.

## Módulo Gide (`modules/gide.py`)

O `Gide` é responsável pela interação com o ecossistema Google.

### Funcionalidades:
- **`criar_pasta`**: Cria pastas no Drive.
- **`criar_arquivo_docs`**: Cria e popula documentos Docs, incluindo a formatação automática de URLs para links clicáveis.
- **`criar_estrutura_categoria_unidade`**: Organiza documentos em estruturas de pastas hierárquicas.
