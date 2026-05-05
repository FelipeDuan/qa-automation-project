import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage


@pytest.mark.e2e
class TestE2ESauceDemo:
    def test_complete_purchase_flow(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_count() == "1"
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        assert cart_page.get_cart_items_count() == 1
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("QA", "Tester", "12345")
        checkout_page.finish_purchase()

        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you" in confirmation.lower()

    def test_purchase_multiple_products(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.add_multiple_items_to_cart(3)
        assert inventory_page.get_cart_count() == "3"
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        assert cart_page.get_cart_items_count() == 3
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("Multi", "Product", "99999")
        checkout_page.finish_purchase()

        confirmation = checkout_page.get_confirmation_message()
        assert "Thank you" in confirmation.lower()

    def test_remove_item_from_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.add_first_item_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        assert cart_page.get_cart_items_count() == 1
        cart_page.remove_item()
        assert cart_page.is_cart_empty()


@pytest.mark.login
class TestLogin:
    def test_login_with_invalid_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("wrong_user", "wrong_pass")
        
        assert login_page.is_error_displayed()
        error = login_page.get_error_message()
        assert "Username and password do not match" in error

    def test_login_with_locked_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")
        
        assert login_page.is_error_displayed()
        error = login_page.get_error_message()
        assert "locked out" in error.lower()

    def test_login_with_empty_credentials(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "")
        
        assert login_page.is_error_displayed()
        error = login_page.get_error_message()
        assert "Username is required" in error


@pytest.mark.checkout
class TestCheckout:
    def test_checkout_with_missing_first_name(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.add_first_item_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("", "Tester", "12345")
        
        error = checkout_page.get_error_message()
        assert "First Name is required" in error
