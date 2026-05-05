# Guia de Contribuição

## Como Adicionar Novos Testes

### Testes de API

#### 1. Criar ou estender um Service

Se precisar de novos endpoints, adicione métodos ao service existente:

```python
# api/services/pet_service.py
def new_endpoint(self, param):
    return self.get(f"/pet/new/{param}")
```

#### 2. Adicionar fixture se necessário

```python
# api/tests/conftest.py
@pytest.fixture
def new_payload(random_id):
    return {"id": random_id, "field": "value"}
```

#### 3. Criar teste

```python
# api/tests/test_pet.py
@pytest.mark.pet
def test_new_scenario(self, pet_service, pet_payload):
    response = pet_service.new_endpoint(pet_payload)
    assert response.status_code == 200
```

### Testes Web

#### 1. Adicionar locators

```python
# web/locators/locators.py
class NewPageLocators:
    ELEMENT = (By.ID, "element-id")
```

#### 2. Criar Page Object (se nova página)

```python
# web/pages/new_page.py
from web.pages.base_page import BasePage
from web.locators.locators import NewPageLocators

class NewPage(BasePage):
    def action(self):
        self.click(NewPageLocators.ELEMENT)
```

#### 3. Criar teste

```python
# web/tests/test_e2e.py
@pytest.mark.e2e
def test_new_flow(self, driver):
    page = NewPage(driver)
    page.action()
    assert page.get_text(Locator) == "Expected"
```

## Padrões de Código

### Nomenclatura

- **Classes**: PascalCase (`PetService`, `LoginPage`)
- **Funções**: snake_case (`get_pet`, `add_to_cart`)
- **Variáveis**: snake_case (`pet_payload`, `order_id`)
- **Constantes**: UPPER_CASE (`BASE_URL`, `TIMEOUT`)

### Testes

- Nomes descritivos: `test_add_pet_returns_200`
- Um assert por conceito (pode ter múltiplos asserts relacionados)
- Arrange-Act-Assert quando aplicável

```python
def test_example(self, service, payload):
    # Arrange (preparação já vem da fixture)
    
    # Act
    response = service.action(payload)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["field"] == payload["field"]
```

### Comentários

❌ **Evitar comentários óbvios:**

```python
# Get the user (BAD - óbvio)
user = user_service.get_user(username)
```

✅ **Comentários úteis:**

```python
# API retorna 200 mesmo com senha incorreta
response = user_service.login(user, "wrong_pass")
assert response.status_code == 200
```

## Markers do Pytest

Sempre adicione markers apropriados:

```python
@pytest.mark.smoke      # Testes críticos
@pytest.mark.negative   # Cenários de erro
@pytest.mark.pet        # Por serviço/domínio
@pytest.mark.e2e        # Fluxos completos
```

## Executar Testes Localmente

### Setup Inicial

```bash
# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de exemplo
cp .env.example .env
```

### Executar

```bash
# Todos os testes
pytest

# Apenas API
pytest api/tests/ -v

# Apenas Web
pytest web/tests/ -v

# Smoke tests
pytest -m smoke

# Com relatório
pytest --html=report.html
```

### Debugging

```bash
# Ver print statements
pytest -s

# Parar no primeiro erro
pytest -x

# Modo verbose
pytest -vv
```

## Checklist Antes de Commit

- [ ] Todos os testes passam localmente
- [ ] Código segue padrões do projeto
- [ ] Markers apropriados adicionados
- [ ] Sem comentários desnecessários
- [ ] Nomes descritivos
- [ ] IDs dinâmicos (não hardcoded)
- [ ] Sem credenciais no código
- [ ] Tratamento de erros adequado

## CI/CD

A pipeline roda automaticamente em:
- Push para qualquer branch
- Pull requests

Os dois jobs devem passar:
- ✅ api-tests
- ✅ web-tests

## Troubleshooting

### Testes Web falhando localmente

- Verificar se ChromeDriver está atualizado
- Tentar modo headless: `export CI=true`

### Testes API com timeout

- Verificar conexão com internet
- Aumentar timeout em `.env`: `REQUEST_TIMEOUT=20`

### Import errors

- Verificar PYTHONPATH
- Rodar de dentro do diretório raiz do projeto
