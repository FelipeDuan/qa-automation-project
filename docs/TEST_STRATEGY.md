# Estratégia de Testes

## Objetivo

Garantir qualidade através de testes automatizados que cobrem cenários críticos, fluxos principais e casos de erro.

## Pirâmide de Testes

```
        /\
       /  \      E2E Web (menor quantidade, maior valor)
      /____\
     /      \    API Tests (maioria, rápidos)
    /________\   Unit Tests (não aplicável neste projeto)
```

## Tipos de Testes Implementados

### 1. Testes de API (Swagger Petstore)

**Escopo**: Cobertura completa dos endpoints principais

#### Pet Service
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Busca por status (available, sold, pending)
- ✅ Validação de schema de resposta
- ✅ Cenários negativos (pet inexistente, dados inválidos)
- ✅ Performance (response time < 2s)

#### User Service
- ✅ CRUD completo
- ✅ Login de usuário
- ✅ Cenários negativos (usuário inexistente, senha incorreta)
- ✅ Validação de campos obrigatórios

#### Store Service
- ✅ Inventário
- ✅ Criar, buscar e deletar pedidos
- ✅ Ciclo de vida completo do pedido
- ✅ Cenários negativos (pedido inexistente, dados inválidos)
- ✅ Performance

### 2. Testes Web (SauceDemo)

**Escopo**: Fluxos E2E e validações de interface

#### Login
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Login com usuário bloqueado
- ✅ Validação de campos vazios

#### Compra E2E
- ✅ Fluxo completo: login → adicionar produto → checkout → confirmação
- ✅ Múltiplos produtos no carrinho
- ✅ Remoção de item do carrinho
- ✅ Validação de campos obrigatórios no checkout

## Categorização de Testes

### Markers do Pytest

```python
@pytest.mark.smoke      # Testes críticos (happy path)
@pytest.mark.negative   # Cenários de erro e exceção
@pytest.mark.e2e        # Fluxos completos ponta a ponta
@pytest.mark.pet        # Testes do Pet Service
@pytest.mark.user       # Testes do User Service
@pytest.mark.store      # Testes do Store Service
@pytest.mark.login      # Testes de login
@pytest.mark.checkout   # Testes de checkout
```

### Como Executar

```bash
# Todos os testes
pytest

# Apenas smoke tests
pytest -m smoke

# Testes negativos
pytest -m negative

# Testes de API
pytest api/tests/

# Testes Web
pytest web/tests/

# Teste específico
pytest api/tests/test_pet.py::TestPetCRUD::test_add_pet_returns_200

# Com relatório HTML
pytest --html=report.html
```

## Cenários de Teste

### API - Cenários Positivos

| Serviço | Cenário | Validações |
|---------|---------|------------|
| Pet | Criar pet | Status 200, campos corretos, schema válido |
| Pet | Buscar pet por ID | Status 200, dados correspondem |
| Pet | Atualizar pet | Status 200, status atualizado |
| Pet | Deletar pet | Status 200 |
| Pet | Buscar por status | Status 200, lista retornada |
| User | Criar usuário | Status 200, resposta adequada |
| User | Buscar usuário | Status 200, dados correspondem |
| User | Login | Status 200, mensagem de sucesso |
| User | Atualizar usuário | Status 200 |
| User | Deletar usuário | Status 200 |
| Store | Inventário | Status 200, dict com contadores |
| Store | Criar pedido | Status 200, campos corretos |
| Store | Buscar pedido | Status 200, dados correspondem |
| Store | Deletar pedido | Status 200 |

### API - Cenários Negativos

| Serviço | Cenário | Validação Esperada |
|---------|---------|-------------------|
| Pet | Buscar pet inexistente | Status 404 |
| Pet | Criar pet sem campos obrigatórios | Status 400/500 |
| Pet | Deletar pet inexistente | Status 404 |
| User | Buscar usuário inexistente | Status 404 |
| User | Login com senha incorreta | Status 200/400 |
| User | Deletar usuário inexistente | Status 404 |
| Store | Buscar pedido inexistente | Status 404 |
| Store | Deletar pedido inexistente | Status 404 |
| Store | Criar pedido com dados inválidos | Status 400/500 |

### Web - Cenários E2E

| Fluxo | Passos | Validação Final |
|-------|--------|----------------|
| Compra simples | Login → Adicionar 1 produto → Checkout → Finalizar | "Thank you for your order" |
| Compra múltipla | Login → Adicionar 3 produtos → Checkout → Finalizar | "Thank you for your order" |
| Remover item | Login → Adicionar produto → Ir ao carrinho → Remover | Carrinho vazio |

### Web - Cenários de Erro

| Cenário | Ação | Validação |
|---------|------|-----------|
| Login inválido | Credenciais incorretas | Mensagem de erro exibida |
| Usuário bloqueado | Login com locked_out_user | Erro "locked out" |
| Campos vazios | Login sem preencher | Erro "Username is required" |
| Checkout sem nome | Prosseguir sem first name | Erro "First Name is required" |

## Validações Implementadas

### API
- ✅ Status codes corretos (200, 404, 400, 500)
- ✅ Headers (Content-Type)
- ✅ Estrutura da resposta (campos obrigatórios)
- ✅ Tipos de dados (list, dict, int, str)
- ✅ Valores específicos (IDs, status, nomes)
- ✅ Response time (< 2 segundos)

### Web
- ✅ Elementos visíveis na tela
- ✅ Textos de confirmação
- ✅ Mensagens de erro
- ✅ Contadores de carrinho
- ✅ Navegação entre páginas

## Isolamento e Cleanup

### Estratégia de IDs Dinâmicos

Para evitar conflitos entre testes, todos os IDs são gerados dinamicamente:

```python
@pytest.fixture
def random_id():
    return random.randint(100000, 999999)
```

### Fixtures do Pytest

- **Preparação**: Criação de payloads com dados únicos
- **Limpeza**: Driver fecha automaticamente após cada teste
- **Reutilização**: Services instanciados uma vez por teste

## Performance

### Targets

- **API**: Response time < 2 segundos
- **Web**: Testes completos em < 60 segundos (local)
- **CI/CD**: Pipeline completa em < 5 minutos

### Otimizações

- Explicit waits ao invés de implicit waits
- Testes API rodando em paralelo (diferentes jobs no CI)
- Headless mode no CI

## Manutenção

### Quando Testes Quebram

1. **Mudança na API**: Atualizar apenas o Service correspondente
2. **Mudança no HTML**: Atualizar apenas o Locator
3. **Mudança no fluxo**: Atualizar Page Object ou teste específico

### Adicionando Novos Testes

1. Identificar tipo (API/Web, positivo/negativo)
2. Adicionar marker apropriado
3. Seguir padrão existente
4. Garantir isolamento (IDs únicos, cleanup)

## Coverage Report

Para gerar relatório de cobertura:

```bash
pytest --html=report.html --self-contained-html
```

## Critérios de Aceitação

Um teste é considerado bem-sucedido quando:

1. ✅ Passa consistentemente (não flaky)
2. ✅ É independente (não depende de ordem)
3. ✅ É rápido (API < 2s, Web E2E < 30s)
4. ✅ É legível (nome descritivo, assertions claras)
5. ✅ Falha pelo motivo certo (não por timeout/flakiness)

## Integração Contínua

A pipeline executa:

1. **api-tests**: Todos os testes de API em paralelo
2. **web-tests**: Todos os testes Web em headless

Testes devem passar em ambos os jobs para merge.
