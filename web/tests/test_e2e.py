import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage


@pytest.mark.e2e
class TestE2ESauceDemo:
    def test_complete_purchase_flow(self, driver):
        print("\n[TEST] Starting complete purchase flow...")
        
        login_page = LoginPage(driver)
        login_page.open()
        print("[TEST] Page opened")
        
        login_page.login("standard_user", "secret_sauce")
        print("[TEST] Login completed")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        print("[TEST] Inventory page loaded")
        
        inventory_page.add_first_item_to_cart()
        print("[TEST] Item added to cart")
        
        cart_count = inventory_page.get_cart_count()
        print(f"[TEST] Cart count: {cart_count}")
        assert cart_count == "1"
        
        inventory_page.go_to_cart()
        print("[TEST] Navigated to cart")

        cart_page = CartPage(driver)
        items_count = cart_page.get_cart_items_count()
        print(f"[TEST] Cart items count: {items_count}")
        assert items_count == 1
        
        cart_page.proceed_to_checkout()
        print("[TEST] Proceeded to checkout")

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("QA", "Tester", "12345")
        print("[TEST] Filled checkout info")
        
        checkout_page.finish_purchase()
        print("[TEST] Finished purchase")

        confirmation = checkout_page.get_confirmation_message()
        print(f"[TEST] Confirmation message: {confirmation}")
        assert "thank you" in confirmation.lower()
        print("[TEST] ✅ Test passed!")

    def test_purchase_multiple_products(self, driver):
        print("\n[TEST] Starting multiple products purchase...")
        
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        print("[TEST] Login completed")

        inventory_page = InventoryPage(driver)
        print("[TEST] Adding 3 items to cart...")
        inventory_page.add_multiple_items_to_cart(3)
        
        cart_count = inventory_page.get_cart_count()
        print(f"[TEST] Expected: 3, Got: {cart_count}")
        assert cart_count == "3", f"Cart count mismatch: expected 3, got {cart_count}"
        
        inventory_page.go_to_cart()
        print("[TEST] Navigated to cart")

        cart_page = CartPage(driver)
        items_count = cart_page.get_cart_items_count()
        print(f"[TEST] Cart page shows {items_count} items")
        assert items_count == 3
        
        cart_page.proceed_to_checkout()
        print("[TEST] Proceeded to checkout")

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("Multi", "Product", "99999")
        print("[TEST] Filled info")
        
        checkout_page.finish_purchase()
        print("[TEST] Finished purchase")

        confirmation = checkout_page.get_confirmation_message()
        print(f"[TEST] Confirmation: {confirmation}")
        assert "thank you" in confirmation.lower()
        print("[TEST] ✅ Test passed!")

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
