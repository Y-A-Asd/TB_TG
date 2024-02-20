import pytest
from django.test import LiveServerTestCase
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from time import sleep

from core.models import User
from conftest import auth, api_client


@pytest.fixture(scope="class")
def chrome_driver(request):
    options = Options()
    # options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    yield
    driver.quit()


def test_home_page(chrome_driver):
    try:
        chrome_driver.get('http://localhost:8000/')
        chrome_driver.maximize_window()
        sleep(5)
        assert "TB_TG Shop" in chrome_driver.title
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")


@pytest.mark.django_db
@pytest.mark.usefixtures("chrome_driver")
class TestSelenium(LiveServerTestCase):

    def test_register_and_login(self):
        self.driver.get('http://localhost:8000/')
        self.driver.maximize_window()
        # sleep(5)
        # link = driver.find_element_by_link_text("ورود /ثبت نام")
        # link.click()
        wait = WebDriverWait(self.driver, 10)
        link = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login/']")))
        link.click()
        link = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/register/']")))
        link.click()

        phone_number_field = wait.until(expected_conditions.presence_of_element_located((By.ID, "phone_number")))
        print(phone_number_field)
        email_field = wait.until(expected_conditions.presence_of_element_located((By.ID, "email")))
        print(email_field)
        password_field = wait.until(expected_conditions.presence_of_element_located((By.ID, "password")))
        print(password_field)
        submit_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@value='submit']")))
        print(submit_button)

        phone_number_field.send_keys("09998880000")
        email_field.send_keys("test@example.com")
        password_field.send_keys("Password123Fardin")
        print(password_field)
        print(email_field)
        submit_button.click()
        sleep(3)
        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            assert alert_text == 'Your account is active now please login!'
            alert.accept()
        except:
            pytest.fail(f"Test failed: no alert get from register!")

        link = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login/']")))
        link.click()

        phone_number_field = wait.until(expected_conditions.presence_of_element_located((By.ID, "phone_number")))
        print(phone_number_field)
        password_field = wait.until(expected_conditions.presence_of_element_located((By.ID, "password")))
        print(password_field)
        submit_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@value='submit']")))
        print(submit_button)

        phone_number_field.send_keys("09998880000")
        password_field.send_keys("Password123Fardin")

        submit_button.click()
        sleep(5)

        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            assert alert_text == 'Token is valid. User is already logged in.'
            alert.accept()
        except:
            pytest.fail(f"Test failed: no alert get from login!")

        sleep(5)
        jwt_token = self.driver.execute_script("return localStorage.getItem('JWT')")
        print('jwt_token', jwt_token)
        authorization_header_value = f"JWT {jwt_token}"
        # self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders',
        #                               {'headers': {'Authorization': authorization_header_value}})
        # print(authorization_header_value)
        # sleep(2)
        # self.driver.get('http://localhost:8000/core/auth/users/')
        # sleep(20)
        # pytest.fail(f"Test failed: no alert get from login!")

    def test_product_filtering(self):
        self.driver.get('http://localhost:8000/')
        self.driver.maximize_window()
        # sleep(5)
        # link = driver.find_element_by_link_text("ورود /ثبت نام")
        # link.click()
        wait = WebDriverWait(self.driver, 10)
        link = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products/']")))
        link.click()

        best_sales = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//button[@value='best_sales']")))
        print(best_sales)
        sleep(2)
        best_sales.click()
        sleep(3)
        button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ترتیب: best_sales')]")))
        button.click()
        sleep(3)