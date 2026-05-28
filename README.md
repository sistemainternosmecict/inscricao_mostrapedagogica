# Inscrições Mostra Pedagógica

## Descrição
Este é um aplicativo Flask simples que serve como um backend para gerenciar inscrições. Atualmente, ele oferece um endpoint para receber dados de inscrição via requisições POST com suporte a CORS.

## Pré-requisitos
- Python 3.8+
- uv (gerenciador de pacotes Python)

## Configuração do Ambiente

1. **Clone o repositório (se ainda não o fez):**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd inscricoes_mostra_pedagogica
   ```

2. **Instale as dependências usando `uv`:**
   Certifique-se de ter o `uv` instalado. Se não tiver, você pode instalá-lo com `pip`:
   ```bash
   pip install uv
   ```
   Em seguida, use `uv` para sincronizar as dependências do projeto:
   ```bash
   uv sync
   ```

## Como Rodar a Aplicação

Para iniciar o servidor Flask em modo de desenvolvimento:

```bash
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Endpoints da API

### `POST /inscricao_entrada`

Este endpoint recebe dados de inscrição em formato JSON.

- **URL:** `/inscricao_entrada`
- **Método:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Corpo da Requisição (Exemplo):**
  ```json
  {
    "nome": "João Silva",
    "email": "joao.silva@example.com",
    "curso": "Engenharia de Software",
    "periodo": "Noturno"
  }
  ```
- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "message": "Dados recebidos com sucesso!"
  }
  ```
- **Resposta de Erro (400 Bad Request):**
  ```json
  {
    "error": "Request must be JSON"
  }
  ```

### Suporte a CORS
Este aplicativo possui suporte a CORS (Cross-Origin Resource Sharing) habilitado para todas as rotas, permitindo que clientes de diferentes origens acessem a API.
