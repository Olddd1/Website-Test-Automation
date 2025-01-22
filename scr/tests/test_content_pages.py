import pytest
from pages import MainPage

@pytest.mark.parametrize("url", [
    "https://dircont.com",
])
def test_content_pages(driver_maximized, wait, url):
    driver_maximized.get(url)
    page = MainPage(driver_maximized, wait)
    result, message = page.check_button_down()
    assert result, message
    result, message = page.check_button_up()
    assert result, message
    result, message = page.check_header_links()
    assert result, message
    result, message = page.check_popups()
    assert result, message
    result, message = page.is_footer_visible()
    assert result, message
    result, message = page.check_body_form()
    assert result, message