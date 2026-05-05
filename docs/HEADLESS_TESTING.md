# 🖥️ Como Rodar Testes Web em Modo Headless (Local)

## 📋 O que é Headless?

**Headless** = Rodar o browser **SEM interface gráfica** (invisível).

**Por quê?**
- ✅ Mais rápido
- ✅ Consome menos recursos
- ✅ Necessário para CI/CD (GitHub Actions não tem interface gráfica)
- ✅ **Pode evitar popups do navegador!**

---

## 🎯 Como Ativar Headless Localmente

### Método 1: Variável de Ambiente (Recomendado)

**Vantagem:** Não precisa modificar o código!

#### Windows (PowerShell):
```powershell
$env:CI="true"
pytest web/tests/test_e2e.py -v -s
```

#### Windows (CMD):
```cmd
set CI=true
pytest web/tests/test_e2e.py -v -s
```

#### Linux/Mac:
```bash
export CI=true
pytest web/tests/test_e2e.py -v -s
```

---

### Método 2: Modificar Temporariamente o Código

**Arquivo:** `web/utils/driver_factory.py`

#### ANTES (modo visual local, headless apenas no CI):
```python
def create_driver():
    chrome_options = Options()

    if os.getenv("CI", "false").lower() == "true":  # ← Só headless no CI
        chrome_options.add_argument("--headless")

    # ... resto do código
```

#### DEPOIS (sempre headless):
```python
def create_driver():
    chrome_options = Options()

    # Força headless SEMPRE (para teste local)
    chrome_options.add_argument("--headless")  # ← ATIVE ESSA LINHA
    
    # if os.getenv("CI", "false").lower() == "true":  # ← COMENTE ESSA LINHA
    #     chrome_options.add_argument("--headless")

    # ... resto do código
```

**⚠️ IMPORTANTE:** Lembre-se de **REVERTER** depois de testar!

---

## 🧪 Comparação: Visual vs Headless

### Modo Visual (atual):
```bash
pytest web/tests/test_e2e.py -v -s
```
**O que acontece:**
- ✅ Chrome abre visualmente
- ✅ Você VÊ cada ação acontecendo
- ❌ **Popup "Salvar senha" APARECE e trava os testes**
- ❌ Mais lento
- ❌ Consome mais RAM

### Modo Headless:
```bash
# Windows PowerShell:
$env:CI="true"; pytest web/tests/test_e2e.py -v -s

# Ou modificar driver_factory.py conforme Método 2
pytest web/tests/test_e2e.py -v -s
```
**O que acontece:**
- ✅ Chrome roda em background (invisível)
- ❌ Você NÃO vê as ações
- ✅ **Popup de senha PROVAVELMENTE NÃO APARECE!** (precisa testar!)
- ✅ Mais rápido
- ✅ Consome menos RAM

---

## 📊 Experimento: Testar se Popup Aparece em Headless

### Passo 1: Rodar em modo Visual
```bash
pytest web/tests/test_e2e.py::TestE2ESauceDemo::test_complete_purchase_flow -v -s
```

**Resultado esperado:**
```
[LOGIN] ✅ Login completed
[POPUP] ✅ Pressed ESC         ← Diz que fechou mas não fechou
[INVENTORY] ❌ Cart badge did NOT appear after 30s
FAILED
```

---

### Passo 2: Rodar em modo Headless
```bash
# Windows PowerShell:
$env:CI="true"
pytest web/tests/test_e2e.py::TestE2ESauceDemo::test_complete_purchase_flow -v -s
```

**Resultado possível A (popup NÃO aparece em headless):**
```
[LOGIN] ✅ Login completed
[POPUP] No popup found or could not dismiss
[INVENTORY] ✅ Cart badge appeared!
[CART] ✅ Clicked cart link
PASSED ← SUCESSO!
```

**Resultado possível B (popup AINDA aparece):**
```
[LOGIN] ✅ Login completed
[POPUP] ✅ Pressed ESC
[INVENTORY] ❌ Cart badge did NOT appear after 30s
FAILED ← Problema persiste
```

---

## 🔧 Reverter para Modo Visual

### Se usou Método 1 (variável de ambiente):
```powershell
# Windows PowerShell:
Remove-Item Env:\CI

# Windows CMD:
set CI=

# Linux/Mac:
unset CI
```

### Se usou Método 2 (modificou código):
**Reverta as mudanças em `driver_factory.py`:**
```python
def create_driver():
    chrome_options = Options()

    if os.getenv("CI", "false").lower() == "true":
        chrome_options.add_argument("--headless")
    # ... resto do código
```

---

## 📝 Comparação Final

| Aspecto | Visual | Headless |
|---------|--------|----------|
| **Browser visível?** | ✅ Sim | ❌ Não |
| **Debug visual?** | ✅ Fácil | ❌ Difícil |
| **Popup aparece?** | ❌ SIM (problema!) | ❓ A testar |
| **Velocidade** | 🐢 Mais lento | 🚀 Mais rápido |
| **CI/CD** | ❌ Não funciona | ✅ Necessário |
| **Consumo RAM** | 💾 Alto | 💾 Baixo |

---

## 🎯 Próximos Passos

1. **Teste em headless** usando o comando acima
2. **Compare os resultados** (popup aparece ou não?)
3. **Se popup NÃO aparecer em headless:**
   - ✅ Problema resolvido!
   - ✅ CI/CD já funciona (GitHub Actions usa headless)
   - ✅ Localmente, escolha entre visual (debug) ou headless (velocidade)

4. **Se popup AINDA aparecer em headless:**
   - ❌ Problema persiste
   - ❌ Precisamos de outra solução (Chrome profile, flags diferentes, etc)

---

## 🆘 Comandos Rápidos

### Rodar TODOS os testes web em headless:
```bash
$env:CI="true"; pytest web/tests/ -v -s
```

### Rodar apenas 1 teste em headless:
```bash
$env:CI="true"; pytest web/tests/test_e2e.py::TestE2ESauceDemo::test_complete_purchase_flow -v -s
```

### Rodar testes API (não afetados):
```bash
pytest api/tests/ -v
```

### Rodar TUDO (API + Web) em headless:
```bash
$env:CI="true"; pytest -v
```

---

## 📚 Referências

- [Selenium Headless Chrome](https://www.selenium.dev/documentation/webdriver/browsers/chrome/#headless)
- [ChromeDriver Options](https://chromedriver.chromium.org/capabilities)
- [GitHub Actions Headless Browsers](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions)
