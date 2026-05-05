# 🚨 Problema Crítico: Popup "Aviso de Vazamento de Senha" do Chrome

## 📋 Contexto

Projeto de automação de testes com Selenium para o site SauceDemo (`https://www.saucedemo.com/`).

**Problema:** Após o login bem-sucedido com credenciais de teste (`standard_user` / `secret_sauce`), o Chrome exibe um popup de **AVISO DE VAZAMENTO DE DADOS** que **bloqueia** toda a automação subsequente.

### **Popup Exato:**
```
┌────────────────────────────────────────┐
│ ⚠️  Mude sua senha                     │
│                                        │
│ A senha que você usou foi encontrada   │
│ em um vazamento de dados. O            │
│ Gerenciador de senhas do Google        │
│ recomenda que você mude essa senha     │
│ imediatamente.                         │
│                                        │
│                          [    OK    ]  │
└────────────────────────────────────────┘
```

**OU em inglês:**
```
┌────────────────────────────────────────┐
│ ⚠️  Change your password               │
│                                        │
│ The password you used was found in a   │
│ data breach. Google Password Manager   │
│ recommends changing this password      │
│ immediately.                           │
│                                        │
│                          [    OK    ]  │
└────────────────────────────────────────┘
```

---

## ✅ **SOLUÇÃO IMPLEMENTADA** (ATUALIZAÇÃO)

### **Por que o popup aparece?**
A senha `secret_sauce` (usada no SauceDemo) foi encontrada em vazamentos de dados reais da internet. O Google Password Manager detecta isso e exibe um **aviso de segurança**, não um popup de salvar senha!

### **Estratégia da Solução:**

1. **Detectar o popup** procurando por texto-chave no HTML da página:
   - "Mude sua senha"
   - "vazamento de dados"
   - "Change your password"
   - "data breach"

2. **Se detectado**, procurar e clicar no botão "OK"

3. **Se NÃO detectado**, continuar normalmente

### **Implementação:**

```python
def dismiss_password_warning_popup(self):
    try:
        page_source = self.driver.page_source.lower()
        
        keywords = [
            "mude sua senha",
            "vazamento de dados",
            "change your password",
            "data breach",
            "gerenciador de senhas",
            "password manager"
        ]
        
        popup_detected = any(keyword in page_source for keyword in keywords)
        
        if popup_detected:
            print("[POPUP] ⚠️ Detected password warning popup")
            
            # Tenta vários seletores para encontrar o botão OK
            ok_button_selectors = [
                (By.XPATH, "//button[contains(text(), 'OK')]"),
                (By.XPATH, "//button[contains(text(), 'Ok')]"),
                (By.CSS_SELECTOR, "button.VfPpkd-LgbsSe"),
                # ... outros ...
            ]
            
            for selector_type, selector_value in ok_button_selectors:
                try:
                    ok_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    ok_button.click()
                    return True
                except:
                    continue
            
            # Fallback: pressiona ENTER
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            return True
        else:
            return False
    except:
        return False
```

### **Arquivo:** `web/pages/base_page.py`
### **Chamado em:** `web/pages/login_page.py` (após login)

### **Vantagens:**
✅ Não interfere com botões da aplicação (apenas se detectar o texto do popup)
✅ Múltiplos seletores (maior chance de sucesso)
✅ Funciona em PT-BR e EN-US
✅ Se não achar, não dá erro (graceful degradation)

---

## 🔍 Sintomas (Antes da Solução)

### Logs típicos:
```
[LOGIN] ✅ Login completed
[POPUP] ✅ Pressed ESC          ← DIZ que fechou, mas NÃO fechou
[INVENTORY] Clicking 'Add to Cart' button...
[INVENTORY] ❌ Cart badge did NOT appear after 30s
```

### Comportamento observado:
1. ✅ Login funciona perfeitamente
2. ❌ Popup "Salvar senha" aparece e **NÃO É FECHADO**
3. ❌ Todos os cliques subsequentes são **bloqueados pelo popup**
4. ✅ Se o usuário **MANUALMENTE** fecha o popup, os testes continuam normalmente
5. ❌ `Keys.ESCAPE` não funciona
6. ❌ `switch_to.alert.dismiss()` não funciona (não é um alert JavaScript nativo)

---

## 🧪 Informações Técnicas

### Ambiente:
- **OS:** Windows 11 (10.0.26200)
- **Python:** 3.14.0
- **Selenium:** 4.x
- **ChromeDriver:** 147.0.7727.138
- **Browser:** Chrome (versão correspondente)
- **Framework:** Pytest

### Stack trace típico:
```python
selenium.common.exceptions.TimeoutException: Message:
# Esperando 30s por elemento que nunca aparece porque popup bloqueia cliques
```

### Segundo erro relacionado:
```python
selenium.common.exceptions.StaleElementReferenceException:
stale element reference: stale element not found
# Quando adiciona múltiplos itens ao carrinho, o DOM é atualizado
```

---

## 🎯 Tentativas de Solução (TODAS FALHARAM)

### 1. ❌ Alert nativo
```python
self.driver.switch_to.alert.dismiss()
```
**Resultado:** Não funciona - popup não é um alert JavaScript

### 2. ❌ ESC key
```python
ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
```
**Resultado:** Código executa mas popup permanece visível

### 3. ❌ TAB + ENTER
```python
ActionChains(self.driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
```
**Resultado:** Não fecha o popup

### 4. ❌ Chrome options (já configurados)
```python
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
})
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
```
**Resultado:** Popup AINDA aparece

### 5. ❌ XPath selectors (removidos por serem perigosos)
```python
# Tentativa de clicar em botões com texto "Não", "Never", "Cancel"
# PROBLEMA: Pegava botões da aplicação (ex: botão Cancel do checkout!)
```
**Resultado:** Clicava em botões errados da aplicação

---

## 💡 Hipóteses

1. **Popup é overlay do Chrome, não do DOM**
   - Não é acessível via JavaScript/Selenium
   - Requer interação humana OU configuração de perfil do Chrome

2. **Popup só aparece em modo visual**
   - Pode NÃO aparecer em modo headless (precisa testar)

3. **Solução pode estar em Chrome Profile**
   - Criar um perfil customizado do Chrome sem password manager
   - Passar o profile para o driver

---

## 📝 Código Relevante

### Arquivos afetados:
- `web/pages/base_page.py` - Método `dismiss_password_popup()`
- `web/pages/login_page.py` - Chama `dismiss_password_popup()` após login
- `web/pages/inventory_page.py` - Cliques são bloqueados
- `web/utils/driver_factory.py` - Configuração do Chrome

### Método atual (NÃO FUNCIONA):
```python
def dismiss_password_popup(self):
    try:
        self.driver.switch_to.alert.dismiss()
        print("[POPUP] ✅ Dismissed alert")
        time.sleep(0.5)
        return True
    except:
        pass
    
    try:
        ActionChains(self.driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        print("[POPUP] ✅ Tried TAB + ENTER (dismiss password save)")
        time.sleep(0.5)
        return True
    except:
        pass
    
    try:
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        print("[POPUP] ✅ Pressed ESC")
        time.sleep(0.5)
        return True
    except:
        pass
    
    print("[POPUP] No popup found or could not dismiss")
    return False
```

---

## 🎯 Possíveis Soluções (NÃO TESTADAS)

### 1. Chrome User Profile
```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("user-data-dir=/path/to/chrome/profile")
chrome_options.add_argument("profile-directory=AutomationProfile")

driver = webdriver.Chrome(options=chrome_options)
```

### 2. Headless Mode (pode evitar o popup)
```python
chrome_options.add_argument("--headless")
```
**Testar se popup aparece em headless!**

### 3. Disable Save Password via Policy
```python
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_settings.auto_select_certificate": 2,
    "profile.password_manager_leak_detection": False,
})
```

### 4. ChromeDriver capabilities
```python
capabilities = {
    "goog:chromeOptions": {
        "excludeSwitches": ["enable-automation", "enable-logging"],
        "useAutomationExtension": False,
        "prefs": {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
    }
}
```

### 5. PyAutoGUI (última opção - usar automação de teclado do OS)
```python
import pyautogui
time.sleep(2)
pyautogui.press('tab')
pyautogui.press('enter')
```
**⚠️ CUIDADO:** Depende do layout da tela, muito frágil!

---

## 🧪 Como Reproduzir

### Modo Visual (popup APARECE):
```bash
cd qa-automation-project
source venv/bin/activate  # Windows: venv\Scripts\activate
pytest web/tests/test_e2e.py::TestE2ESauceDemo::test_complete_purchase_flow -v -s
```

**Você verá:**
1. Browser abre
2. Login acontece
3. **Popup "Salvar senha" aparece**
4. Teste fica travado esperando o cart badge aparecer (30s timeout)
5. Se você clicar manualmente no popup (Não/Never), teste continua

### Modo Headless (testar se popup NÃO aparece):
```bash
# Modificar temporariamente driver_factory.py:
# ANTES:
if os.getenv("CI", "false").lower() == "true":
    chrome_options.add_argument("--headless")

# DEPOIS:
chrome_options.add_argument("--headless")  # Sempre headless

# Rodar o teste:
pytest web/tests/test_e2e.py::TestE2ESauceDemo::test_complete_purchase_flow -v -s
```

---

## ❓ Perguntas para Resolver

1. **Como desabilitar COMPLETAMENTE o popup de senha do Chrome via Selenium?**
2. **O popup aparece em modo headless?** (Se não, usar headless resolve!)
3. **Existe uma flag do ChromeDriver que desabilita isso?**
4. **Usar um Chrome profile pré-configurado resolve?**
5. **Há alguma API nativa do Selenium para isso?**

---

## 🎯 Objetivo Final

**Testes E2E devem rodar 100% automatizados, SEM intervenção manual, tanto localmente quanto no CI/CD (GitHub Actions).**

Atualmente:
- ✅ 31 testes API: **100% passando**
- ❌ 7 testes Web: **2 falhando** (devido ao popup)
  - ✅ `test_remove_item_from_cart`: PASSA
  - ✅ `test_login_with_invalid_credentials`: PASSA
  - ✅ `test_login_with_locked_user`: PASSA
  - ✅ `test_login_with_empty_credentials`: PASSA
  - ✅ `test_checkout_with_missing_first_name`: PASSA
  - ❌ `test_complete_purchase_flow`: FALHA (popup bloqueia)
  - ❌ `test_purchase_multiple_products`: FALHA (popup + StaleElement)

---

## 📚 Referências

- [Selenium WebDriver Docs](https://www.selenium.dev/documentation/webdriver/)
- [ChromeDriver Capabilities](https://chromedriver.chromium.org/capabilities)
- [Chrome Command Line Switches](https://peter.sh/experiments/chromium-command-line-switches/)
- [StackOverflow: Disable Chrome Save Password](https://stackoverflow.com/questions/35032857/disable-chrome-save-your-password-popup)

---

## 🆘 Pedido de Ajuda

**Se você sabe como resolver isso, POR FAVOR me ajude com:**
1. Código Python/Selenium que **REALMENTE** fecha o popup
2. Flags do Chrome que **REALMENTE** desabilitam o popup
3. Workarounds confiáveis que funcionem em CI/CD

**Muito obrigado!** 🙏
