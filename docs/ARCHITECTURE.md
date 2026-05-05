# Arquitetura do Projeto

## Visão Geral

Este projeto implementa automação de testes seguindo princípios de **Clean Code**, **SOLID** e **Design Patterns** reconhecidos pela indústria.

## Princípios Arquiteturais

### 1. Separação de Responsabilidades (SRP)

Cada módulo tem uma responsabilidade única e bem definida:

- **Services**: Encapsulam a lógica de comunicação com APIs
- **Pages**: Representam páginas web e suas ações (Page Object Model)
- **Locators**: Centralizam seletores web
- **Tests**: Contêm apenas cenários de teste e assertions

### 2. Open/Closed Principle (OCP)

Classes são abertas para extensão e fechadas para modificação:

- `BasePage` e `BaseClient` fornecem comportamento base
- Classes específicas herdam e estendem funcionalidade
- Não é necessário modificar classes base para adicionar novos testes

### 3. Dependency Inversion Principle (DIP)

- Testes dependem de abstrações (fixtures do pytest), não de implementações concretas
- Services dependem de `BaseClient`, permitindo fácil substituição
- Configurações vêm de variáveis de ambiente, não hardcoded

## Design Patterns Implementados

### Page Object Model (POM)

**Problema**: Código duplicado, difícil manutenção, baixa legibilidade.

**Solução**: Separar representação de páginas da lógica de testes.

```
BasePage (comportamento comum)
    ├── LoginPage
    ├── InventoryPage
    ├── CartPage
    └── CheckoutPage
```

**Benefícios**:
- DRY: Reutilização de código
- Manutenção: Alterações em um lugar só
- Legibilidade: Testes expressivos

### Service Layer Pattern

**Problema**: Testes fazendo chamadas HTTP diretas, duplicação de lógica.

**Solução**: Camada de serviços que encapsula comunicação com APIs.

```
BaseClient (lógica HTTP comum)
    ├── PetService
    ├── UserService
    └── StoreService
```

**Benefícios**:
- Abstração de complexidade HTTP
- Tratamento centralizado de erros
- Fácil teste e mock

### Factory Pattern

**Problema**: Configuração complexa do WebDriver.

**Solução**: `driver_factory.py` cria instâncias configuradas.

**Benefícios**:
- Configuração centralizada
- Adaptação automática ao ambiente (CI/CD)
- Fácil modificação

## Estrutura de Diretórios

```
qa-automation-project/
│
├── api/                        # Testes de API
│   ├── client/                 # Camada HTTP base
│   │   └── base_client.py      # Cliente HTTP reutilizável
│   ├── services/               # Serviços por domínio
│   │   ├── pet_service.py
│   │   ├── user_service.py
│   │   └── store_service.py
│   ├── tests/                  # Testes organizados por serviço
│   │   ├── conftest.py         # Fixtures compartilhadas
│   │   ├── test_pet.py
│   │   ├── test_user.py
│   │   └── test_store.py
│   └── utils/                  # Utilitários e configurações
│       └── config.py
│
├── web/                        # Testes Web
│   ├── pages/                  # Page Objects
│   │   ├── base_page.py        # Comportamento comum
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── locators/               # Seletores centralizados
│   │   └── locators.py
│   ├── tests/                  # Testes E2E
│   │   ├── conftest.py
│   │   └── test_e2e.py
│   └── utils/                  # Utilitários web
│       └── driver_factory.py
│
├── docs/                       # Documentação técnica
├── .github/workflows/          # CI/CD
└── pytest.ini                  # Configuração de testes
```

## Tratamento de Erros

### API

- **Timeout**: Configurável via variável de ambiente
- **ConnectionError**: Capturado e reportado claramente
- **RequestException**: Tratamento genérico para falhas HTTP

### Web

- **Explicit Waits**: WebDriverWait em todas as interações
- **Element Visibility**: Verificação antes de interagir
- **Timeout Configurável**: Via `WebDriverWait(driver, timeout)`

## Ambiente e Configuração

### Variáveis de Ambiente

Todas as configurações sensíveis e específicas de ambiente são externalizadas:

```env
API_BASE_URL=https://petstore.swagger.io/v2
REQUEST_TIMEOUT=10
WEB_BASE_URL=https://www.saucedemo.com/
WEB_TIMEOUT=10
```

### Detecção de Ambiente CI/CD

O código detecta automaticamente se está rodando em CI:

```python
if os.getenv("CI", "false").lower() == "true":
    chrome_options.add_argument("--headless")
```

## Estratégia de Testes

### Categorização com Markers

```python
@pytest.mark.smoke      # Testes críticos
@pytest.mark.negative   # Cenários de erro
@pytest.mark.e2e        # Fluxos completos
```

### Isolamento de Testes

- **IDs Dinâmicos**: Evita conflitos entre testes
- **Fixtures**: Preparação e limpeza automática
- **Stateless**: Cada teste é independente

### Cobertura

**API**:
- CRUD completo (Create, Read, Update, Delete)
- Busca e filtros
- Cenários negativos (404, 400, 500)
- Validação de schema
- Performance (response time)

**Web**:
- Fluxos E2E completos
- Validações de erro
- Múltiplos cenários de usuário
- Remoção de itens
- Validações de formulário

## Boas Práticas Implementadas

1. **DRY (Don't Repeat Yourself)**: Código reutilizável
2. **KISS (Keep It Simple, Stupid)**: Simplicidade sobre complexidade
3. **YAGNI (You Aren't Gonna Need It)**: Apenas o necessário
4. **Legibilidade**: Nomes claros, estrutura lógica
5. **Manutenibilidade**: Fácil de modificar e estender
6. **Testabilidade**: Fixtures, mocks, isolamento

## Escalabilidade

### Adicionar Novos Testes de API

1. Criar novo service em `api/services/`
2. Herdar de `BaseClient`
3. Adicionar fixture em `conftest.py`
4. Criar arquivo `test_*.py` correspondente

### Adicionar Novas Pages

1. Criar classe em `web/pages/`
2. Herdar de `BasePage`
3. Adicionar locators em `locators.py`
4. Usar no teste

### Performance

- Testes paralelos: `pytest -n auto` (requer pytest-xdist)
- Markers permitem execução seletiva: `pytest -m smoke`
- CI/CD roda jobs em paralelo
