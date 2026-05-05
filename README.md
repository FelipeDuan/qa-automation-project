# QA Automation Project

Projeto de automação de testes com cobertura de **API (Swagger Petstore)** e **Web (SauceDemo)**, integrado a pipeline de CI/CD via GitHub Actions.

Arquitetura baseada em separação de responsabilidades seguindo princípios do SOLID.

---

## 📁 Estrutura do Projeto

```
qa-automation-project/
├── api/
│   ├── client/          # BaseClient: camada HTTP reutilizável
│   ├── services/        # PetService, UserService, StoreService
│   ├── tests/           # Testes de API com pytest
│   └── utils/           # Configurações (BASE_URL)
├── web/
│   ├── pages/           # Page Object Model: BasePage, LoginPage, etc.
│   ├── locators/        # Seletores centralizados
│   ├── tests/           # Testes E2E com Selenium
│   └── utils/           # DriverFactory (gerencia headless no CI)
├── .github/workflows/
│   └── ci.yml           # Pipeline GitHub Actions
├── requirements.txt
└── README.md
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Pytest | Framework de testes |
| Selenium | Automação web |
| Requests | Testes de API |
| WebDriver Manager | Download automático do ChromeDriver |
| GitHub Actions | CI/CD pipeline |

---

## ⚙️ Como Instalar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/qa-automation-project.git
cd qa-automation-project

# Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Como Executar

**Testes de API:**
```bash
pytest api/tests/ -v
```

**Testes Web:**
```bash
pytest web/tests/ -v
```

**Tudo junto:**
```bash
pytest -v
```

> Os testes web rodam em modo headless automaticamente no CI/CD (variável `CI=true`).

---

## 🔄 CI/CD

A pipeline roda automaticamente a cada `push` ou `pull_request`:

1. **api-tests** — instala dependências e executa `pytest api/tests/`
2. **web-tests** — instala dependências e executa `pytest web/tests/` com `CI=true` (headless)

Acesse a aba **Actions** do seu repositório para ver os resultados.

---

## ✅ Cenários Cobertos

**API - Petstore:**
- Pet: criar, buscar, atualizar, deletar, buscar por status
- User: criar, buscar, login, atualizar, deletar
- Store: inventário, criar pedido, buscar pedido, deletar pedido

**Web - SauceDemo:**
- Fluxo E2E completo: login → adicionar produto → checkout → confirmação
- Login com credenciais inválidas (validação de erro)
