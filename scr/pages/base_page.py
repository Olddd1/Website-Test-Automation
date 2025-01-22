import time
from typing import List

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def find_element(self, locator) -> WebElement:
        """
        Находит элемент на странице с использованием явного ожидания.
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except:
            return None
    def find_elements(self, locator) -> List[WebElement]:
        """
        Находит все элементы на странице, соответствующие локатору.
        """
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except:
            return None
    
    def find_nested_element(self, parent_element, child_locator) -> WebElement:
        """
        Ищет вложенный элемент внутри родительского с использованием динамического ожидания.
        
        :param parent_element: WebElement - родительский элемент
        :param child_locator: tuple - локатор дочернего элемента (например, (By.CLASS_NAME, "child"))
        :return: WebElement - найденный дочерний элемент
        """
        try:
            child_element = self.wait.until(
                lambda driver: parent_element.find_element(*child_locator)
            )
            return child_element
        except:
            return None
    
    def click(self, locator):
        """
        Выполняет клик по элементу после его поиска.
        """
        self.find_element(locator).click()
        
    def input_text(self, locator, text):
        """
        Очищает поле ввода и вводит в него текст.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        
    def get_current_url(self) -> str:
        """
        Возвращает текущий URL страницы.
        """
        return self.driver.current_url
    
    def is_element_visible(self, locator, timeout=10) -> bool:
        """
        Проверяет видимость элемента на странице.
        
        :param locator: Кортеж (тип локатора, значение), например (By.ID, "example")
        :param timeout: Время ожидания в секундах
        :return: True если элемент видим, False если нет
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def current_position(self) -> int:
        """
        Получает текущую позицию вертикальной прокрутки страницы в пикселях.
        """
        return self.driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
    
    def scroll(self, pixels):
        """
        Прокручивает страницу на указанное количество пикселей.
        """
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def check_target_link(self, link: WebElement, url):
        """
        Проверяет ссылку, открывая её в новой вкладке.
        
        :param link: Элемент ссылки для проверки
        :param url: URL, который должен содержаться в открытой странице
        :return: True если URL совпадает, False если нет
        """
        ActionChains(self.driver).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
        
        if len(self.driver.window_handles) == 1:
            return False
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(0.5)
        result = url in self.driver.current_url
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        return result
    
    def click_by_coords(self, x, y):
        """
        Выполняет клик по указанным координатам.
        
        :param x: Координата по горизонтали
        :param y: Координата по вертикали
        """
        actions = ActionChains(self.driver)
        actions.move_by_offset(x, y).click().perform()
        actions.reset_actions()
        
    def click_checkbox(self, checkbox):
        """
        Программно устанавливает чекбокс в выбранное состояние.
        """
        self.driver.execute_script("arguments[0].checked = true;", checkbox)