# QA Automation Project

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-success)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue)]()
[![Pytest](https://img.shields.io/badge/Pytest-7.4+-green)]()
[![Selenium](https://img.shields.io/badge/Selenium-4.15+-orange)]()

Projeto de automação de testes profissional com cobertura completa de **API (Swagger Petstore)** e **Web (SauceDemo)**, integrado a pipeline de CI/CD via GitHub Actions.

Arquitetura baseada em **Clean Code**, **SOLID** e **Design Patterns** reconhecidos pela indústria.

---

## 🎯 Características

- ✅ Cobertura completa de APIs (CRUD + cenários negativos)
- ✅ Testes E2E web com Page Object Model
- ✅ IDs dinâmicos (sem conflitos entre testes)
- ✅ Tratamento robusto de erros
- ✅ Explicit waits (sem flakiness)
- ✅ Pytest markers (execução seletiva)
- ✅ CI/CD com jobs paralelos
- ✅ Documentação técnica completa
- ✅ Variáveis de ambiente
- ✅ Código limpo (sem comentários óbvios)

---

## 📁 Estrutura do Projeto

```
qa-automation-project/
├── api/
│   ├── client/          # BaseClient: camada HTTP com tratamento de erros
│   ├── services/        # PetService, UserService, StoreService
│   ├── tests/           # Testes organizados com markers
│   └── utils/           # Configurações via variáveis de ambiente
├── web/
│   ├── pages/           # Page Object Model completo
│   ├── locators/        # Seletores centralizados
│   ├── tests/           # Testes E2E categorizados
│   └── utils/           # DriverFactory (auto-detecta CI)
├── docs/
│   ├── ARCHITECTURE.md   # Decisões arquiteturais
│   ├── TEST_STRATEGY.md  # Estratégia de testes
│   ├── CONTRIBUTING.md   # Guia para contribuir
│   └── DECISIONS.md      # ADRs (Architecture Decision Records)
├── .github/workflows/
│   └── ci.yml           # Pipeline com jobs paralelos
├── pytest.ini           # Configuração e markers
├── requirements.txt     # Dependências versionadas
├── .env.example         # Template de variáveis
└── README.md
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso | Versão |
|------------|-----|--------|
| Python | Linguagem principal | 3.10+ |
| Pytest | Framework de testes | 7.4+ |
| Selenium | Automação web | 4.15+ |
| Requests | Testes de API | 2.31+ |
| WebDriver Manager | Gerenciamento do ChromeDriver | 4.0+ |
| python-dotenv | Variáveis de ambiente | 1.0+ |
| pytest-html | Relatórios visuais | 4.1+ |
| GitHub Actions | CI/CD pipeline | - |

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/qa-automation-project.git
cd qa-automation-project
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente (opcional)

```bash
cp .env.example .env
# Edite .env conforme necessário
```

---

## ▶️ Execução

### Todos os testes

```bash
pytest -v
```

### Por categoria

```bash
# Apenas testes de API
pytest api/tests/ -v

# Apenas testes Web
pytest web/tests/ -v

# Smoke tests (cenários críticos)
pytest -m smoke -v

# Testes negativos
pytest -m negative -v

# Por serviço específico
pytest -m pet -v
pytest -m user -v
pytest -m store -v
```

### Com relatório HTML

```bash
pytest --html=report.html --self-contained-html
```

### Modo headless (Web)

```bash
export CI=true  # Linux/Mac
set CI=true     # Windows
pytest web/tests/ -v
```

---

## 🔄 CI/CD

A pipeline executa automaticamente em cada **push** ou **pull_request**:

### Jobs Paralelos

1. **api-tests**
   - Instala dependências
   - Executa todos os testes de API
   - Valida Pet, User e Store services

2. **web-tests**
   - Instala dependências
   - Executa testes E2E em modo headless
   - Valida fluxos completos de compra e login

### Status

Acesse a aba **Actions** para ver resultados detalhados.

---

## ✅ Cobertura de Testes

### API - Swagger Petstore

#### Pet Service
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Busca por status (available, sold, pending)
- ✅ Validação de schema e campos obrigatórios
- ✅ Cenários negativos (404, 400, dados inválidos)
- ✅ Validação de performance (< 2s)

#### User Service
- ✅ CRUD completo
- ✅ Login de usuário
- ✅ Validação de credenciais
- ✅ Cenários negativos (usuário inexistente, senha incorreta)
- ✅ Validação de campos

#### Store Service
- ✅ Consulta de inventário
- ✅ Criar, buscar e deletar pedidos
- ✅ Ciclo de vida completo do pedido
- ✅ Cenários negativos (pedido inexistente, dados inválidos)
- ✅ Validação de performance

**Total: 30+ testes de API**

### Web - SauceDemo

#### Login
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Login com usuário bloqueado (locked_out_user)
- ✅ Validação de campos obrigatórios

#### Fluxos E2E
- ✅ Compra completa: login → adicionar produto → checkout → confirmação
- ✅ Múltiplos produtos no carrinho
- ✅ Remoção de item do carrinho
- ✅ Validação de campos do checkout

**Total: 8+ testes E2E**

---

## 📊 Pytest Markers

```python
@pytest.mark.smoke      # Testes críticos (happy path)
@pytest.mark.negative   # Cenários de erro
@pytest.mark.pet        # Testes do Pet Service
@pytest.mark.user       # Testes do User Service
@pytest.mark.store      # Testes do Store Service
@pytest.mark.e2e        # Fluxos E2E completos
@pytest.mark.login      # Testes de login
@pytest.mark.checkout   # Testes de checkout
```

---

## 🏗️ Design Patterns

### Page Object Model (POM)

Separação entre representação de páginas e lógica de testes.

```python
# Teste legível e manutenível
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("user", "pass")
    assert inventory_page.is_loaded()
```

### Service Layer Pattern

Camada de abstração sobre chamadas HTTP.

```python
# Reutilizável e testável
def test_get_pet(pet_service):
    response = pet_service.get_pet(123)
    assert response.status_code == 200
```

### Factory Pattern

Criação padronizada de WebDriver.

```python
# Configuração centralizada
driver = create_driver()  # Auto-detecta CI e configura headless
```

---

## 🔒 Boas Práticas Implementadas

- **Clean Code**: Nomes descritivos, sem comentários óbvios
- **SOLID**: Separação de responsabilidades, classes abertas para extensão
- **DRY**: Código reutilizável (BasePage, BaseClient)
- **KISS**: Simplicidade sobre complexidade
- **Explicit Waits**: Sem flakiness, timeouts controlados
- **IDs Dinâmicos**: Testes isolados e paralelos
- **Tratamento de Erros**: Mensagens claras e úteis
- **Variáveis de Ambiente**: Configuração externalizada

---

## 📚 Documentação

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Decisões arquiteturais e design patterns
- [TEST_STRATEGY.md](docs/TEST_STRATEGY.md) - Estratégia e cobertura de testes
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Guia para contribuir
- [DECISIONS.md](docs/DECISIONS.md) - ADRs e lições aprendidas
- [BUGFIX.md](docs/BUGFIX.md) - Correção do bug crítico de TimeoutException
- [CHANGELOG.md](docs/CHANGELOG.md) - Histórico completo de mudanças

---

## 🤝 Como Contribuir

1. Leia [CONTRIBUTING.md](docs/CONTRIBUTING.md)
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona nova feature'`
4. Push para a branch: `git push origin feature/nova-feature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é para fins educacionais.

---

## 👤 Autor

Desenvolvido como projeto de avaliação da disciplina de Qualidade de Software.
