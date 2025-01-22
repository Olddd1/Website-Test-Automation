import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")  # Безголовый режим
    # options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver  

    driver.quit()
    
@pytest.fixture
def driver_maximized(driver):
    driver.maximize_window()
    yield driver
    driver.quit()
    
@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)  