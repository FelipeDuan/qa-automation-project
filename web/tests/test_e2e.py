from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.checkout_page import CheckoutPage


class TestE2ESauceDemo:
    def test_complete_purchase_flow(self, driver):
        """Fluxo completo: login → adicionar produto → finalizar compra."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_count() == "1"
        inventory_page.go_to_cart()

        checkout_page = CheckoutPage(driver)
        checkout_page.proceed_to_checkout()
        checkout_page.fill_info("QA", "Tester", "12345")
        checkout_page.finish_purchase()

        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you" in confirmation

    def test_login_with_invalid_credentials(self, driver):
        """Valida mensagem de erro ao usar credenciais inválidas."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("wrong_user", "wrong_pass")
        error = login_page.get_error_message()
        assert "Username and password do not match" in error
