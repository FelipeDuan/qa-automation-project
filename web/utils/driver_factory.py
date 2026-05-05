import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    chrome_options = Options()

    if os.getenv("CI", "false").lower() == "true":
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # TODAS as flags possíveis para desabilitar password manager
    chrome_options.add_argument("--disable-password-manager-reauthentication")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Prefs agressivos
    chrome_options.add_experimental_option("prefs", {
        # Password Manager
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        
        # Autofill
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        
        # Notifications & Popups
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        
        # Downloads
        "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
        
        # Segurança (desabilita avisos de segurança)
        "safebrowsing.enabled": False,
        "profile.default_content_setting_values.automatic_downloads": 1,
    })
    
    # Desabilita automação detectada
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
