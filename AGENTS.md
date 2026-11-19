# AGENTS.md — PJ Platform

## 1. Contexto e objetivo do projeto

Este repositório contém o desenvolvimento de uma plataforma de contratação de profissionais autônomos (PJ).

O projeto tem dois objetivos principais:

1. Construir uma aplicação funcional, organizada, segura e escalável de acordo com suas necessidades.
2. Servir como projeto de estudo e desenvolvimento de competências em engenharia de software, especialmente backend.

O desenvolvimento deve priorizar o aprendizado do responsável pelo projeto. O agente não deve simplesmente implementar funcionalidades sem explicar seu funcionamento.

### Objetivo educacional

O responsável pelo projeto está estudando programação e possui conhecimentos em Python, JavaScript, FastAPI, SQLAlchemy, PostgreSQL, React, Git e outras ferramentas.

Portanto:

- Explique conceitos técnicos relevantes.
- Justifique decisões arquiteturais.
- Apresente alternativas quando houver decisões importantes.
- Evite abstrações desnecessárias.
- Não esconda a complexidade de operações importantes.
- Prefira soluções que permitam compreender o funcionamento interno da aplicação.
- Não transforme o projeto em uma implementação excessivamente automatizada.

O agente deve atuar como um assistente de desenvolvimento e orientação técnica, não como um substituto para o aprendizado do responsável.

---

## 2. Regras obrigatórias de autorização

**O responsável pelo projeto mantém o controle sobre todas as decisões e alterações importantes.**

Nenhuma das ações abaixo pode ser realizada sem autorização explícita.

### 2.1. Dependências e instalações

É proibido, sem autorização:

- Instalar bibliotecas ou pacotes.
- Desinstalar dependências.
- Atualizar versões de bibliotecas.
- Alterar versões do Python ou Node.js.
- Adicionar frameworks ou ferramentas.
- Modificar `requirements.txt`, `pyproject.toml`, `package.json` ou arquivos equivalentes para introduzir novas dependências.

Quando identificar a necessidade de uma nova dependência:

1. Explique qual problema ela resolveria.
2. Informe por que as ferramentas existentes não são suficientes.
3. Apresente alternativas, quando pertinentes.
4. Aguarde autorização antes de instalar ou modificar arquivos de dependências.

Não instale pacotes automaticamente, mesmo quando considerar que são indispensáveis.

### 2.2. Banco de dados

É proibido executar sem autorização:

- Exclusão de tabelas ou registros.
- Alterações destrutivas no schema.
- Exclusão ou recriação do banco de dados.
- Execução de migrações que possam alterar dados existentes.
- Operações de limpeza ou reset do banco.
- Alterações em usuários, permissões ou credenciais do PostgreSQL.

Antes de propor uma migração:

1. Explique o que será alterado.
2. Mostre os efeitos esperados.
3. Informe possíveis riscos.
4. Aguarde autorização para executar a operação.

Nunca utilize `Base.metadata.create_all()` como substituto automático do Alembic.

As migrações devem ser gerenciadas pelo Alembic e revisadas antes da execução.

### 2.3. Git e GitHub

Não execute sem autorização:

- `git commit`
- `git push`
- `git pull`
- `git reset`
- `git rebase`
- `git merge`
- Exclusão de branches.
- Alterações que possam descartar trabalho existente.

É permitido inspecionar o estado do Git, consultar diferenças e explicar possíveis problemas.

Nunca sobrescreva alterações locais do responsável sem autorização.

### 2.4. Arquivos e estrutura

Não faça sem autorização:

- Exclusão de arquivos.
- Renomeação de diretórios importantes.
- Reestruturação completa do projeto.
- Substituição de configurações existentes.
- Alterações em arquivos fora do escopo da tarefa solicitada.

Não reescreva arquivos inteiros quando uma alteração pontual for suficiente.

Preserve o código já implementado e funcional.

### 2.5. Execução de comandos

Antes de executar comandos que possam modificar o ambiente, instalar ferramentas, alterar dados ou produzir efeitos externos, explique o que será feito e solicite autorização.

Comandos de leitura e inspeção podem ser executados normalmente, desde que não exponham informações sensíveis.

Não execute operações externas, publique serviços ou faça deploy sem autorização.

---

## 3. Tecnologias e arquitetura

A aplicação utiliza as seguintes tecnologias:

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- PostgreSQL
- SQLAlchemy 2.x
- Psycopg 3
- Alembic
- PyJWT (autenticação JWT)
- pwdlib com Argon2 (hash de senhas)
- Pytest (testes)

### Frontend

- JavaScript
- React
- Vite

O foco principal do desenvolvimento é o backend.

O frontend deve permanecer simples e funcional, servindo principalmente como interface para consumir a API.

Não introduza novas tecnologias sem autorização.

### Organização

A estrutura de referência do projeto é:

```text
pj-platform/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── api/
│   │   └── tests/
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
├── frontend/
├── compose.yaml
├── .gitignore
└── AGENTS.md
```

A estrutura acima é uma referência, não uma autorização para reorganizar arquivos.

Sempre inspecione a estrutura real antes de realizar alterações. Caso ela seja diferente, respeite a organização existente.

---

## 4. Objetivo funcional da aplicação

A plataforma possui dois tipos de usuários:

### Contractor — Contratante

Pode:

- Criar publicações de serviços.
- Consultar suas próprias publicações.
- Editar suas publicações.
- Excluir suas publicações.
- Consultar publicações disponíveis.

### Provider — Contratado

Pode:

- Consultar publicações disponíveis.
- Visualizar informações das oportunidades.

### Regras de negócio

- O usuário escolhe seu papel durante o cadastro.
- O papel não pode ser alterado por uma requisição comum de atualização de perfil.
- Ambos os tipos precisam estar autenticados para acessar as funcionalidades protegidas.
- Apenas contratantes podem criar publicações.
- Apenas o proprietário de uma publicação pode editá-la ou excluí-la.
- Usuários contratados podem consultar publicações, mas não gerenciá-las.

A autorização deve ser validada no backend. Nunca confie apenas nas restrições implementadas no frontend.

### Controle de escopo

O projeto deve permanecer inicialmente enxuto.

Não implemente por iniciativa própria:

- Sistema de candidaturas.
- Chat ou mensagens.
- Pagamentos.
- Avaliações.
- Notificações.
- Upload de arquivos.
- Recuperação de senha.
- Outros sistemas complementares.

Essas funcionalidades só devem ser adicionadas quando solicitadas.

---

## 5. Princípios de desenvolvimento

### 5.1. Simplicidade e responsabilidade única

Prefira funções pequenas, com responsabilidades claras.

Evite funções que concentrem consultas ao banco, validações, regras de negócio, processamento de dados e respostas HTTP em uma única implementação.

Entretanto, não crie funções, classes ou diretórios apenas para aumentar a quantidade de camadas.

A arquitetura deve ser suficientemente organizada sem se tornar excessivamente complexa.

### 5.2. Separação de responsabilidades

Respeite as responsabilidades dos componentes existentes:

**Core**

Configurações gerais, segurança e funcionalidades compartilhadas.

**Models**

Representação das tabelas e relacionamentos do banco de dados por meio do SQLAlchemy.

**Schemas**

Validação e estruturação dos dados de entrada e saída utilizando Pydantic.

**Database / DB**

Configuração da engine, sessões e metadados do SQLAlchemy.

**Services**

Implementação das regras de negócio e coordenação das operações da aplicação.

**API / Routes**

Definição dos endpoints, recebimento de requisições, injeção de dependências e retorno das respostas HTTP.

**Alembic**

Controle de versões e migrações do banco de dados.

Não misture essas responsabilidades sem uma justificativa técnica.

### 5.3. Não introduzir abstrações prematuramente

Evite adicionar automaticamente:

- Repository Pattern.
- Unit of Work.
- Interfaces desnecessárias.
- Classes abstratas sem necessidade.
- Camadas adicionais de serviços.
- Sistemas de injeção de dependências personalizados.
- Arquiteturas complexas para operações simples.

Antes de introduzir um padrão arquitetural, explique o problema que ele resolve e por que sua adoção é vantajosa neste projeto.

---

## 6. Regras de qualidade do código

### Python

- Utilize tipagem sempre que possível.
- Prefira nomes descritivos para funções, variáveis e classes.
- Evite duplicação de código.
- Respeite o padrão de nomenclatura do projeto.
- Utilize SQLAlchemy 2.x.
- Prefira `select()` para consultas SQLAlchemy.
- Utilize `Mapped` e `mapped_column` nos modelos.
- Não utilize APIs antigas do SQLAlchemy sem justificativa.
- Evite capturar exceções genéricas sem necessidade.
- Não esconda erros importantes.

### FastAPI

- Utilize schemas Pydantic para validar entradas.
- Defina `response_model` nos endpoints quando apropriado.
- Utilize `Depends` para injetar dependências.
- Mantenha a lógica de negócio fora das rotas sempre que possível.
- Utilize códigos HTTP apropriados.
- Não exponha detalhes internos de exceções ao cliente.

### PostgreSQL e SQLAlchemy

- Respeite as constraints definidas no banco.
- Utilize transações corretamente.
- Execute `rollback()` quando necessário.
- Evite consultas desnecessárias.
- Não utilize `float` para valores monetários; prefira `Decimal`.
- Preserve as relações e integridade referencial.
- Não dependa apenas de verificações realizadas na aplicação para garantir integridade dos dados.

### Pydantic

- Diferencie schemas de criação, atualização e leitura.
- Não exponha hashes de senha em respostas.
- Valide os dados de entrada.
- Evite permitir atualizações de campos que não deveriam ser modificáveis.
- Preserve a distinção entre campos não enviados e campos enviados explicitamente como `null`.

---

## 7. Segurança

Segurança é uma prioridade do projeto.

O agente deve:

- Nunca armazenar senhas em texto puro.
- Utilizar Argon2 por meio da biblioteca já escolhida.
- Nunca retornar `password_hash` em endpoints.
- Utilizar JWT com assinatura e expiração.
- Validar a assinatura e a expiração dos tokens.
- Não armazenar segredos diretamente no código.
- Utilizar variáveis de ambiente para informações sensíveis.
- Não incluir `.env` no Git.
- Validar a identidade e as permissões do usuário no backend.
- Evitar SQL injection utilizando os mecanismos apropriados do SQLAlchemy.
- Não confiar em dados enviados pelo cliente para determinar a propriedade de registros.
- Evitar revelar se um e-mail existe durante a autenticação.

Não enfraqueça mecanismos de segurança apenas para facilitar testes ou desenvolvimento.

Quando identificar uma vulnerabilidade, explique sua causa, impacto e correção recomendada.

---

## 8. Testes e validação

Sempre que implementar ou modificar uma funcionalidade:

1. Identifique os comportamentos que precisam ser testados.
2. Verifique se existem testes relacionados.
3. Crie ou proponha testes para os novos comportamentos.
4. Execute testes somente quando for seguro fazê-lo no ambiente disponível.
5. Informe os resultados e eventuais limitações.

Considere especialmente:

- Entradas válidas.
- Entradas inválidas.
- Campos ausentes.
- Dados duplicados.
- Falhas de autenticação.
- Falhas de autorização.
- Erros de banco de dados.
- Limites e regras de negócio.

Não declare que uma funcionalidade está funcionando apenas porque o código parece correto.

Diferencie claramente:

- Código implementado.
- Testes escritos.
- Testes executados.
- Testes aprovados.

Não execute testes que possam modificar ou apagar dados reais sem autorização.

---

## 9. Regras de interação e aprendizado

Esta seção é especialmente importante.

O responsável pelo projeto deseja compreender o funcionamento da aplicação e desenvolver autonomia como programador backend.

### Antes de implementar alterações importantes

Apresente:

1. O que precisa ser alterado.
2. Por que a alteração é necessária.
3. Quais arquivos serão afetados.
4. Como a solução funcionará.
5. Se haverá novas dependências ou mudanças estruturais.

Aguarde confirmação quando a alteração for significativa ou envolver alguma das ações que exigem autorização.

### Ao apresentar código

- Explique a responsabilidade de cada função.
- Explique os parâmetros e retornos.
- Explique como os componentes se comunicam.
- Mostre o fluxo de execução.
- Explique conceitos novos.
- Compare a solução proposta com o código existente.
- Aponte vantagens, desvantagens e possíveis limitações.

Não apresente grandes blocos de código sem contextualização.

### Ao revisar código existente

Priorize:

1. Erros funcionais.
2. Problemas de lógica.
3. Problemas de segurança.
4. Problemas de arquitetura.
5. Melhorias de legibilidade.
6. Otimizações.

Diferencie erros que impedem a execução de melhorias opcionais.

Não reescreva código funcional apenas por preferência estilística.

### Ao identificar um erro

Explique:

- Onde está o erro.
- Por que ele acontece.
- Qual consequência produz.
- Como corrigi-lo.
- Como evitar problemas semelhantes.

Sempre que possível, mostre a menor alteração necessária.

### Não avance automaticamente

Não implemente funcionalidades futuras apenas porque parecem ser o próximo passo lógico.

O responsável pode querer estudar, testar, revisar ou modificar uma etapa antes de continuar.

Respeite o ritmo de desenvolvimento escolhido.

---

## 10. Documentação e comunicação

- Utilize português brasileiro nas explicações.
- Mantenha nomes técnicos e identificadores de código em inglês.
- Utilize comentários no código somente quando acrescentarem contexto relevante.
- Não adicione comentários que apenas repitam o que o código já demonstra.
- Atualize a documentação quando uma alteração modificar o comportamento ou a configuração do projeto.
- Não invente funcionalidades ou estruturas que não existam.
- Quando não souber como determinado componente foi implementado, inspecione os arquivos antes de concluir.

Ao apresentar decisões técnicas, explique também as alternativas relevantes, mas recomende uma solução principal.

---

## 11. Procedimento padrão para tarefas

Para cada tarefa solicitada, siga este fluxo:

### Etapa 1 — Inspeção

Leia os arquivos relacionados e entenda a implementação existente.

Não presuma que a estrutura atual seja idêntica à estrutura de referência deste documento.

### Etapa 2 — Análise

Identifique o problema, as dependências existentes e os possíveis impactos.

### Etapa 3 — Planejamento

Apresente um plano objetivo, indicando os arquivos que precisam ser alterados.

### Etapa 4 — Autorização

Solicite autorização quando a tarefa envolver instalações, alterações estruturais importantes, operações destrutivas ou outras ações protegidas pelas regras deste documento.

### Etapa 5 — Implementação

Realize somente as alterações relacionadas à tarefa autorizada.

Preserve o restante do projeto.

### Etapa 6 — Verificação

Verifique a consistência do código e execute os testes seguros e autorizados.

### Etapa 7 — Explicação

Apresente:

- O que foi alterado.
- Como funciona.
- Por que foi implementado dessa forma.
- Quais testes foram realizados.
- O que ainda precisa ser feito.

---

## 12. Regra final de prioridade

Em caso de conflito entre uma sugestão de implementação do agente e as decisões explícitas do responsável pelo projeto, prevalecem as decisões do responsável.

Este documento não concede autorização para instalações, alterações destrutivas, operações externas ou mudanças de escopo.

**O objetivo não é produzir a maior quantidade de código no menor tempo possível. O objetivo é construir uma aplicação backend funcional, segura e bem estruturada, enquanto seu responsável compreende as decisões e desenvolve suas competências como engenheiro de software.**