# Decisões Arquiteturais

Documentação das principais decisões técnicas e suas justificativas.

## 1. Python como Linguagem

**Decisão**: Usar Python 3.10+

**Razões**:
- Simplicidade e legibilidade (zen do Python)
- Ecossistema rico para testes (pytest, selenium, requests)
- Rápido desenvolvimento
- Amplamente usado em QA

**Alternativas Consideradas**: Java (mais verboso, requer mais boilerplate)

---

## 2. Pytest ao invés de Unittest

**Decisão**: Pytest como framework de testes

**Razões**:
- Sintaxe mais limpa (assert simples ao invés de self.assertEqual)
- Sistema de fixtures poderoso
- Plugins extensivos (pytest-html, pytest-xdist)
- Markers para categorização
- Melhor relatório de falhas

**Alternativas Consideradas**: 
- unittest (builtin, mas mais verboso)
- robot framework (menos flexível)

---

## 3. Page Object Model (POM)

**Decisão**: Implementar POM completo para testes Web

**Razões**:
- Separação clara entre testes e implementação de páginas
- Reusabilidade de código
- Manutenibilidade (mudanças em um único lugar)
- Legibilidade dos testes
- Padrão da indústria

**Exemplo do problema resolvido**:

❌ **Sem POM** (código duplicado, difícil manutenção):
```python
def test_login():
    driver.find_element(By.ID, "user-name").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "login-button").click()

def test_login_error():
    driver.find_element(By.ID, "user-name").send_keys("wrong")
    driver.find_element(By.ID, "password").send_keys("wrong")
    driver.find_element(By.ID, "login-button").click()
```

✅ **Com POM** (reutilizável, legível):
```python
def test_login():
    login_page.login("user", "pass")

def test_login_error():
    login_page.login("wrong", "wrong")
```

---

## 4. Service Layer para API

**Decisão**: Criar camada de services entre testes e HTTP client

**Razões**:
- Abstração de complexidade HTTP
- Reutilização de lógica de requisições
- Tratamento centralizado de erros
- Facilita testes e mocks
- Separação de responsabilidades

**Exemplo**:

❌ **Sem Service Layer**:
```python
def test_get_pet():
    response = requests.get(f"{BASE_URL}/pet/123")
    assert response.status_code == 200
```

✅ **Com Service Layer**:
```python
def test_get_pet(pet_service):
    response = pet_service.get_pet(123)
    assert response.status_code == 200
```

---

## 5. Explicit Waits > Implicit Waits

**Decisão**: Usar apenas explicit waits (WebDriverWait)

**Razões**:
- Mais controle sobre condições específicas
- Evita timeouts desnecessários
- Melhor performance
- Mensagens de erro mais claras
- Não conflita com explicit waits (problema conhecido)

**Implementação**:
```python
# BasePage encapsula todos os waits
def click(self, locator):
    self.wait.until(EC.element_to_be_clickable(locator)).click()
```

---

## 6. IDs Dinâmicos nos Testes

**Decisão**: Gerar IDs aleatórios para cada execução

**Razões**:
- Evita conflitos entre execuções paralelas
- Permite rodar testes múltiplas vezes sem cleanup
- Simula melhor cenários reais (dados únicos)
- Facilita debugging (cada run tem IDs únicos)

**Implementação**:
```python
@pytest.fixture
def random_id():
    return random.randint(100000, 999999)
```

---

## 7. Variáveis de Ambiente

**Decisão**: Externalizar todas as configurações

**Razões**:
- Não hardcode URLs (facilita troca de ambientes)
- Segurança (não commitar credenciais)
- Flexibilidade (configurar sem alterar código)
- Padrão 12-factor app

**Configurações Externalizadas**:
- API_BASE_URL
- WEB_BASE_URL
- REQUEST_TIMEOUT
- WEB_TIMEOUT
- CI flag

---

## 8. Separação API e Web no CI/CD

**Decisão**: Jobs separados para API e Web

**Razões**:
- Paralelização (execução mais rápida)
- Isolamento de falhas (um não bloqueia outro)
- Logs mais limpos
- Escalabilidade (adicionar mais jobs facilmente)

---

## 9. Pytest Markers

**Decisão**: Categorizar testes com markers

**Razões**:
- Execução seletiva (smoke, negative)
- Organização lógica
- CI/CD pode rodar subsets
- Facilita manutenção

**Markers Definidos**:
- smoke: Testes críticos
- negative: Cenários de erro
- pet/user/store: Por domínio
- e2e/login/checkout: Por fluxo

---

## 10. Sem Docker neste Projeto

**Decisão**: Não usar Docker Compose

**Razões**:
- APIs e sites são externos (Petstore, SauceDemo)
- Não há aplicação própria para containerizar
- Adicionar Docker seria over-engineering
- CI já roda em containers (GitHub Actions)

**Quando Docker seria útil**:
- Se tivéssemos API própria para subir
- Se precisássemos de banco de dados local
- Se tivéssemos múltiplos serviços interdependentes

---

## 11. Tratamento de Erros no BaseClient

**Decisão**: Capturar e relevantar exceções com mensagens claras

**Razões**:
- Diagnóstico mais rápido de falhas
- Diferencia timeout de connection error
- Facilita debugging
- Testes podem validar tipos de erro específicos

**Implementação**:
```python
try:
    response = self.session.request(method, url, **kwargs)
except Timeout:
    raise TimeoutError(f"Request to {url} timed out")
except ConnectionError:
    raise ConnectionError(f"Failed to connect to {url}")
```

---

## 12. Estrutura de Diretórios

**Decisão**: Separar `api/` e `web/` no nível raiz

**Razões**:
- Clara separação de responsabilidades
- Fácil navegação
- Permite executar testes separadamente
- Escalável (adicionar mobile/ no futuro)

**Alternativas Consideradas**:
- Tudo em `tests/` (menos organizado)
- Por feature (dificulta separação API/Web)

---

## 13. BasePage e BaseClient

**Decisão**: Classes base com comportamento comum

**Razões**:
- DRY (Don't Repeat Yourself)
- Open/Closed Principle (aberto para extensão)
- Consistência (todas as pages usam mesmos waits)
- Facilita mudanças globais

---

## 14. Pytest HTML Report

**Decisão**: Incluir pytest-html nos requirements

**Razões**:
- Relatórios visuais para stakeholders
- Histórico de execuções
- Facilita apresentação de resultados
- Sem custo adicional

---

## Lições Aprendidas

### O que funcionou bem:
- ✅ POM tornou manutenção trivial
- ✅ Fixtures do pytest reduziram boilerplate
- ✅ Markers permitiram execução seletiva
- ✅ IDs dinâmicos eliminaram conflitos

### O que mudaria:
- ⚠️ Adicionar retry em testes flaky (API externa pode falhar)
- ⚠️ Implementar logging estruturado
- ⚠️ Adicionar screenshots em falhas web
