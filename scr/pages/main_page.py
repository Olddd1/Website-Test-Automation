import time
from pages.base_page import BasePage

from selenium.webdriver.common.by import By


class MainPage(BasePage):
    HEADER = (By.CSS_SELECTOR, "header#t-header")
    FOOTER = (By.CSS_SELECTOR, "footer#t-footer")
    ERROR_POPUP = (By.ID, "tilda-popup-for-error")
    BUTTON_DOWN = (By.XPATH, '//*[@id="rec548245415"]/div/div/div[6]/a')
    BUTTON_UP = (By.CSS_SELECTOR, "button.t890__arrow")
    POPUPS = (By.XPATH, "//a[starts-with(@href, '#popup')]")
    
    FORM_IN_BODY = (By.XPATH, "//*[@class='t-form__inputsbox' and not(ancestor::header)]")
    FORM_BUTTON = (By.TAG_NAME, "button")
    FORM_NAME_INPUT = (By.NAME, "Name")
    FORM_PHONE_INPUT = (By.NAME, "tildaspec-phone-part[]")
    FORM_CHECKBOX = (By.NAME, "Checkbox")
    FORM_CAPTCHA = (By.ID, "captchaIframeBox")
    
    HEADER_MAIN_LINK = (By.XPATH, '//*[@id="nav592090633"]/div/div[2]/div/a')
    HEADER_BUY_LINK = (By.XPATH, '//*[@id="nav592090633"]/div/div[3]/nav/ul/li[1]/a')
    HEADER_AGENT_LINK = (By.XPATH, '//*[@id="nav592090633"]/div/div[3]/nav/ul/li[3]/a')
    HEADER_SUPPLIERS_LINK = (By.XPATH, '//*[@id="nav592090633"]/div/div[3]/nav/ul/li[2]/a')
    
    SCROLL_DISTANCE = 1500
    WAITING_TIME = 0.5
    
    def is_header_visible(self) -> bool:
        """
        Проверяет видимость шапки на странице.
        
        :return: True если шапка видима, False если нет
        """
        return self.is_element_visible(self.HEADER)

    def is_footer_visible(self) -> tuple[bool, str]:
        """
        Проверяет видимость подвала на странице.
        
        :return: Кортеж (статус успеха, сообщение)
        """
        if self.is_element_visible(self.FOOTER):
            return True, "OK"
        return False, "Подвал отсутствует"
    
    def is_error_popup_visible(self) -> bool:
        """
        Проверяет видимость всплывающего окна с ошибкой.
        
        :return: True если окно с ошибкой видимо, False если нет
        """
        return self.is_element_visible(self.ERROR_POPUP)
    
    def check_header_links(self) -> tuple[bool, str]:
        """
        Проверяет корректность работы всех ссылок в шапке.
        
        :return: Кортеж (статус успеха, сообщение)
        """
        if not self.is_header_visible():
            return False, "шапка отсутствует"
            
        links_to_check = [
            (self.HEADER_MAIN_LINK, "https://dircont.com/", "не работает ссылка на главную"),
            (self.HEADER_BUY_LINK, "https://dircont.com/buy", "не работает ссылка на страницу покупателям"),
            (self.HEADER_AGENT_LINK, "https://dircont.com/agent", "не работает ссылка на страницу агентам"),
            (self.HEADER_SUPPLIERS_LINK, "https://dircont.com/suppliers", "не работает ссылка на страницу поставвщикам")
        ]
        
        for locator, url, error_msg in links_to_check:
            element = self.find_element(locator)
            if element and not self.check_target_link(element, url):
                return False, error_msg
                
        return True, "OK"

    def check_button_down(self) -> tuple[bool, str]:
        """
        Проверяет функциональность кнопки прокрутки вниз.
        
        :return: Кортеж (статус успеха, сообщение)
        """
        if not self.is_element_visible(self.BUTTON_DOWN):
            return False, "кнопка отсутствует"
            
        initial_position = self.current_position()
        self.click(self.BUTTON_DOWN)
        time.sleep(self.WAITING_TIME)
        if initial_position == self.current_position():
            return False, "кнопка вниз не работает"
        return True, "OK"

    def check_button_up(self) -> tuple[bool, str]:
        """
        Проверяет функциональность кнопки прокрутки вверх.
        
        :return: Кортеж (статус успеха, сообщение)
        """
        initial_position = self.current_position()
        if initial_position == 0:
            self.scroll(self.SCROLL_DISTANCE)
            time.sleep(self.WAITING_TIME)
            
        if not self.is_element_visible(self.BUTTON_UP):
            return False, "кнопка вверх не работает"
            
        self.click(self.BUTTON_UP)
        time.sleep(self.WAITING_TIME * 2)
        
        return (True, "OK") if self.current_position() == 0 else (False, "кнопка вверх не работает")

    def check_popup(self, popup_link) -> tuple[bool, str]:
        """
        Проверяет функциональность отдельного всплывающего окна.
        
        :param popup_link: WebElement ссылки на всплывающее окно
        :return: Кортеж (статус успеха, сообщение)
        """
        popup_id = popup_link.get_attribute("href").split('#')[1]
        popup_locator = (By.CSS_SELECTOR, f'[data-tooltip-hook="#{popup_id}"]')
        
        time.sleep(self.WAITING_TIME)
        popup = self.find_element(popup_locator)
        
        if not popup or not popup.is_displayed():
            return False, f"ошибка с popup {popup_link}"
            
        self.click_by_coords(20, 20)
        time.sleep(self.WAITING_TIME)
        
        return True, "OK"

    def check_popups(self) -> tuple[bool, str]:
        """
        Проверяет функциональность всех всплывающих окон на странице.
        
        :return: Кортеж (статус успеха, сообщение)
        """
        popups = self.find_popups()
        if not popups:
            return False, "попапы не найдены"
            
        for popup_link in popups:
            if not (popup_link.is_displayed() and popup_link.is_enabled()):
                continue
                
            self.driver.execute_script("arguments[0].scrollIntoView(true);", popup_link)
            time.sleep(self.WAITING_TIME)
            self.driver.execute_script("arguments[0].click();", popup_link)
            
            success, message = self.check_popup(popup_link)
            if not success:
                return False, message
            time.sleep(self.WAITING_TIME)
                
        return True, "OK"
    
    def find_popups(self):
        return self.find_elements(self.POPUPS)
    
    def check_body_form(self):        
        form = self.find_element(self.FORM_IN_BODY)
        return self.check_form(form)
    
    def check_form(self, form):
        submit_button = self.find_nested_element(form, self.FORM_BUTTON)
        name_input = self.find_nested_element(form, self.FORM_NAME_INPUT)
        phone_input = self.find_nested_element(form, self.FORM_PHONE_INPUT)
        checkbox = self.find_nested_element(form, self.FORM_CHECKBOX)
        
        if not self.check_error_popup(submit_button):
            return False, "не отображается ошибка при пустой форме"
        
        name_input.clear()
        name_input.send_keys("test")
        
        if not self.check_error_popup(submit_button):
            return False, "не отображается ошибка при пустом номере"
        
        name_input.clear()
        name_input.send_keys("test")
        
        phone_input.clear()
        phone_input.send_keys("999")
        
        if not self.check_error_popup(submit_button):
            return False, "не отображается ошибка при коротком номере"
        
        name_input.clear()
        name_input.send_keys("test")
        
        phone_input.clear()
        phone_input.send_keys("9999999999")
        
        if not self.check_error_popup(submit_button):
            return False, "не отображается ошибка при неотмеченном чекбоксе"
        
        name_input.clear()
        name_input.send_keys("test")
        
        phone_input.clear()
        phone_input.send_keys("9999999999")
        
        self.click_checkbox(checkbox)

        submit_button.click()
        
        time.sleep(self.WAITING_TIME)
                
        if self.is_element_visible(self.FORM_CAPTCHA, 3) or self.is_element_visible(self.FORM_SUCCESS_POPUP, 3):
            return True, "OK"
        
        return False, "не отображаеьтся попап об успешной отправки заявки"
        
    def check_error_popup(self, button):
        time.sleep(self.WAITING_TIME * 2)
        
        button.click()
        
        time.sleep(self.WAITING_TIME)
        
        return self.is_error_popup_visible()
    