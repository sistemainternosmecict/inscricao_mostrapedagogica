# Inscrições Mostra Pedagógica

## Descrição
Este aplicativo Flask gerencia inscrições, com integração ao Google Drive e Google Docs para automação de documentos.

## Pré-requisitos
- Python 3.8+
- uv (gerenciador de pacotes Python)
- Conta de Serviço do Google Cloud com acesso às APIs do Google Drive e Google Docs.

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

3. **Configuração do Módulo Gide:**
   O módulo Gide automatiza a criação de pastas e documentos no Google Drive.
   
   - **`creds.json`**: Crie este arquivo no diretório raiz com as credenciais da sua Conta de Serviço do Google Cloud (formato JSON baixado do console do GCP). Este arquivo é obrigatório para autenticação.

## Como Rodar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000/`.

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

### Arquivos de Configuração Mínima:
1. `creds.json`: Credenciais da Conta de Serviço (GCP).
2. O sistema espera que a pasta compartilhada no Drive (onde os documentos serão criados) seja configurada e seu ID passado adequadamente para os métodos do `Gide`.
