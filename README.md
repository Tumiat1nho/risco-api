# Risco API

API secundária do MVP de avaliação de risco de fornecedores/terceiros.
Recebe dados cadastrais de uma empresa e calcula um nível de risco com base em
regras de negócio simples, mantendo um histórico das avaliações realizadas.

Esta API é consumida pela [Fornecedores API](https://github.com/Tumiat1nho/fornecedores-api),
que atua como componente principal do MVP.

## Regras de cálculo de risco

O score é a soma dos pontos abaixo, mapeado para um nível final:

| Fator                                          | Pontos |
|-------------------------------------------------|--------|
| Situação cadastral diferente de "ATIVA"          | +40    |
| Situação cadastral não informada                 | +20    |
| Capital social < R$ 1.000                        | +30    |
| Capital social < R$ 10.000                       | +15    |
| Empresa aberta há menos de 1 ano                 | +30    |
| Empresa aberta há menos de 2 anos                | +15    |

| Pontuação | Nível de risco |
|-----------|----------------|
| 0–19      | baixo          |
| 20–44     | médio          |
| 45–69     | alto           |
| 70+       | crítico        |

## Rotas

| Método | Rota                          | Descrição                                  |
|--------|-------------------------------|---------------------------------------------|
| POST   | `/risco/calcular`             | Calcula o risco e salva no histórico         |
| GET    | `/risco/historico`            | Lista avaliações (filtros/paginação)         |
| GET    | `/risco/historico/{id}`       | Detalha uma avaliação                        |
| PUT    | `/risco/historico/{id}`       | Atualiza nível de risco ou observação        |
| DELETE | `/risco/historico/{id}`       | Remove uma avaliação do histórico            |

## Como executar

### Opção 1 — Docker Compose

Esta API é buildada automaticamente pelo `docker-compose.yml` presente no
repositório da `fornecedores-api`. Basta ter as duas pastas lado a lado e
rodar o compose a partir de lá.

### Opção 2 — Localmente, sem Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Acesse o Swagger em http://localhost:8001/docs

## Estrutura do projeto

```
risco_api/
├── app/
│   ├── main.py       # Rotas da API
│   ├── database.py   # Conexão e criação da tabela SQLite
│   ├── schemas.py     # Modelos Pydantic
│   └── regras.py      # Lógica de cálculo do score de risco
├── Dockerfile
└── requirements.txt
```

## Tecnologias

- Python 3.11+
- FastAPI
- SQLite (via `sqlite3`, sem ORM)
- Docker
