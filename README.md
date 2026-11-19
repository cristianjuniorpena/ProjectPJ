# PJ Platform

API REST para uma plataforma de contratação de profissionais autônomos (PJ). O projeto conecta **contratantes** — que publicam demandas de serviço — a **contratados** — que consultam essas oportunidades.

Além da aplicação em si, o repositório tem um objetivo explícito de aprendizado: cada decisão de arquitetura é tomada para ser compreendida, documentada e justificada, com foco em engenharia de software backend.

---

## Sobre o projeto

O domínio é simples de propósito, o que permite concentrar o esforço nos problemas que realmente importam em uma API: autenticação, autorização, integridade de dados, separação de responsabilidades e evolução segura do schema.

Regras de negócio centrais:

- O usuário escolhe seu papel (`contractor` ou `provider`) no cadastro e **não pode alterá-lo** por uma requisição comum de atualização de perfil.
- Apenas contratantes podem criar, editar e excluir publicações.
- Apenas o proprietário de uma publicação pode alterá-la ou excluí-la.
- Contratados podem consultar publicações, mas não gerenciá-las.
- Toda autorização é validada no backend — o frontend nunca é fonte de verdade.

## Status atual

| Área | Estado |
|---|---|
| Cadastro de usuários | Funcional (`POST /auth/register`) |
| Login com JWT | Funcional (`POST /auth/login`, OAuth2 Password Flow) |
| Proteção de rotas com Bearer token | Funcional (`GET /user/me`) |
| Modelagem de `users` e `posts` + migração Alembic | Concluída |
| CRUD de publicações | Não iniciado |
| Autorização por papel (`contractor` / `provider`) | Não iniciada |
| Testes automatizados | Não iniciados |
| Frontend | Apenas o scaffold Vite + React; ainda não consome a API |

Este README é atualizado conforme o projeto avança.

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| API | FastAPI 0.162 + Uvicorn |
| Validação | Pydantic 2 |
| Banco | PostgreSQL |
| ORM | SQLAlchemy 2.x (estilo `Mapped` / `mapped_column`) |
| Driver | Psycopg 3 |
| Migrações | Alembic |
| Autenticação | JWT (PyJWT) com OAuth2 Password Flow |
| Hash de senhas | Argon2 via `pwdlib` |
| Frontend | React 19 + Vite (scaffold) |

## Arquitetura

O backend é organizado por responsabilidade, sem camadas cerimoniais:

```text
backend/
├── app/
│   ├── main.py           # instância FastAPI, routers e endpoints de infraestrutura
│   ├── core/             # configurações (.env) e segurança (JWT, Argon2, esquema OAuth2)
│   ├── database/         # engine, sessão e Base declarativa do SQLAlchemy
│   ├── models/           # tabelas e relacionamentos (SQLAlchemy)
│   ├── schemas/          # contratos de entrada/saída (Pydantic)
│   ├── crud/             # acesso a dados (queries reutilizáveis)
│   ├── services/         # regras de negócio e orquestração
│   └── api/
│       ├── dependencies.py   # sessão de banco e usuário autenticado
│       └── routes/           # endpoints HTTP
├── alembic/              # histórico de migrações
├── alembic.ini
├── requirements.txt
└── .env.example
```

O fluxo de uma requisição segue a direção: **rota → serviço → CRUD → modelo → banco**. A rota cuida de HTTP (status, dependências, resposta), o serviço concentra a regra de negócio e o CRUD isola as consultas.

## Modelo de dados

```mermaid
erDiagram
    users ||--o{ posts : publica
    users {
        bigint id PK
        varchar name
        varchar email UK
        varchar password_hash
        varchar role "contractor | provider"
        timestamptz created_at
    }
    posts {
        bigint id PK
        bigint user_id FK
        varchar title
        text description
        varchar category
        numeric budget "nullable, >= 0"
        varchar status "open | closed"
        timestamptz created_at
        timestamptz updated_at
    }
```

Parte das regras vive no próprio banco, e não só na aplicação:

- `uq_users_email` — e-mail único.
- `chk_users_role` — apenas `contractor` ou `provider`.
- `chk_posts_status` — apenas `open` ou `closed`.
- `chk_posts_budget` — orçamento nulo ou não negativo.
- `fk_posts_user_id` com `ON DELETE RESTRICT` — não é possível excluir um usuário que ainda possui publicações.
- `idx_posts_status_created_at` — índice para a listagem de oportunidades abertas.
- `budget` é `NUMERIC(12,2)` e `Decimal` no Python, nunca `float`.

## Autenticação e autorização

O fluxo usa **OAuth2 Password Flow** com JWT assinado em HS256 e sem refresh token (escopo atual).

```mermaid
sequenceDiagram
    participant C as Cliente
    participant A as API
    participant DB as PostgreSQL

    C->>A: POST /auth/register (JSON)
    A->>DB: SELECT por e-mail + INSERT (senha em Argon2)
    A-->>C: 201 + dados públicos do usuário

    C->>A: POST /auth/login (form: username=e-mail, password)
    A->>DB: SELECT usuário por e-mail
    A->>A: verifica Argon2 (ou hash descartável, se o e-mail não existir)
    A-->>C: 200 + access_token (JWT: sub, email, exp)

    C->>A: GET /user/me (Authorization: Bearer <token>)
    A->>A: valida assinatura e expiração
    A->>DB: SELECT usuário pelo id do claim "sub"
    A-->>C: 200 + dados do usuário autenticado
```

Pontos que explicam o desenho:

- **`sub` é o id do usuário em formato string.** É o que a RFC 7519 define e o que o PyJWT exige.
- **O token é verificado e o usuário é buscado no banco.** A assinatura prova apenas que o token foi emitido por esta API; a consulta garante que o usuário ainda existe e fornece o `role` atual, base para autorização.
- **E-mail inexistente também verifica um hash descartável (`DUMMY_HASH`).** Assim o tempo de resposta não revela se a conta existe.
- **Falhas de autenticação retornam 401 com `WWW-Authenticate: Bearer`**, sempre com a mesma mensagem genérica.
- **`response_model` nas rotas impede vazamento de `password_hash`**, mesmo que o objeto ORM completo seja retornado pela camada de serviço.

## Endpoints

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| `POST` | `/auth/register` | Cadastra um usuário (`contractor` ou `provider`) | Pública |
| `POST` | `/auth/login` | Autentica e devolve o JWT (form-urlencoded) | Pública |
| `GET` | `/user/me` | Dados do usuário autenticado | Bearer token |
| `GET` | `/user/` | Lista usuários | **Pública — em correção** |
| `DELETE` | `/user/delete` | Exclui usuário por e-mail | **Pública — em correção** |
| `GET` | `/database-test` | Verifica a conexão com o banco | Pública |
| `GET` | `/status` | Health check | Pública |

Documentação interativa (Swagger UI) em `/docs`, com botão **Authorize** para testar rotas protegidas.

> As rotas `GET /user/` e `DELETE /user/delete` ainda não estão protegidas e não possuem `response_model` — são as próximas a serem corrigidas (ver Roadmap). Não use este estado em produção.

## Decisões de engenharia

- **JWT stateless, mas com consulta ao banco.** Um token puramente stateless não permite revogar acesso; buscar o usuário a cada requisição custa uma query e resolve revogação e mudança de papel.
- **Argon2 em vez de bcrypt/SHA.** Algoritmo recomendado atualmente para senhas, com parâmetros de custo embutidos no hash.
- **Contratos Pydantic separados para entrada e saída.** `UserCreateSchema` valida a entrada; `UserReadSchema` define o que pode sair. Isso evita mass assignment e vazamento de campos sensíveis.
- **Integridade no banco além da aplicação.** Constraints e chaves estrangeiras não dependem de o código lembrar de validar.
- **Alembic desde o início.** Nada de `create_all()`; todo o schema tem histórico versionado e reversível.
- **Sessão por requisição via `Depends`.** `get_database` abre e fecha a sessão com `yield`, garantindo fechamento mesmo em erro.
- **Dependências síncronas para I/O de banco.** O FastAPI executa dependências `def` em threadpool, evitando bloquear o event loop.
- **Sem abstrações prematuras.** Não há Repository, Unit of Work nem interfaces artificiais; há apenas a separação que o problema atual exige.
- **Sem `float` para dinheiro.** `Decimal` no Python e `NUMERIC` no PostgreSQL.

## Como executar

Pré-requisitos: Python 3.12+, PostgreSQL e um banco criado.

```bash
# 1. Ambiente virtual
cd backend
python -m venv .venv
source .venv/bin/activate

# 2. Dependências
pip install -r requirements.txt

# 3. Configuração
cp .env.example .env
# edite o .env com a URL do seu banco e uma SECRET_KEY própria:
#   openssl rand -hex 32

# 4. Migrações
alembic upgrade head

# 5. Servidor
uvicorn app.main:app --reload
```

Acesse `http://localhost:8000/docs`.

### Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | String de conexão (`postgresql+psycopg://usuario:senha@host:5432/banco`) |
| `ALGORITHM` | Algoritmo de assinatura do JWT (ex.: `HS256`) |
| `SECRET_KEY` | Chave de assinatura; use no mínimo 32 bytes aleatórios |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do access token em minutos |
| `DUMMY_HASH` | Hash Argon2 descartável usado no login de e-mail inexistente |

O `DUMMY_HASH` precisa ser um hash Argon2 válido. Gere um com:

```bash
python -c "import secrets; from pwdlib import PasswordHash; print(PasswordHash.recommended().hash(secrets.token_urlsafe(32)))"
```

> O `.env` nunca é versionado. Apenas `.env.example` fica no repositório.

### Testando o fluxo manualmente

1. `POST /auth/register` com nome, e-mail, senha e papel.
2. Em `/docs`, clique em **Authorize** e faça login pelo formulário do OAuth2 (no campo `username`, informe o **e-mail**).
3. Chame `GET /user/me`.

## Roadmap

- [x] Modelagem de `users` e `posts` com migração Alembic
- [x] Cadastro com hash Argon2 e validação Pydantic
- [x] Login com JWT (OAuth2 Password Flow)
- [x] Dependência `get_current_user` e rota `GET /user/me`
- [ ] Proteger `GET /user/` e `DELETE /user/delete`; eliminar exposição de `password_hash`
- [ ] Autorização por papel (`require_contractor` / `require_provider`)
- [ ] CRUD de publicações com verificação de propriedade
- [ ] Testes automatizados (autenticação, autorização e regras de negócio)
- [ ] Integração do frontend com a API

## Sobre o desenvolvimento

Este projeto é desenvolvido como estudo de engenharia de software backend. As decisões são documentadas, as alternativas são comparadas e a complexidade relevante não é escondida. O código prioriza clareza e compreensão sobre automação: não há geradores de CRUD, repositórios genéricos ou camadas que existam apenas para parecer arquitetura.
