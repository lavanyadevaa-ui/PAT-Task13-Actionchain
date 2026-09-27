import pytest
from selenium import webdriver

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_drag_and_drop_positive(setup):
    driver = setup
    driver.get("https://jqueryui.com/droppable/")

    # Switch into the iframe containing the draggable/droppable elements
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))

    source = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "draggable"))
    )
    target = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "droppable"))
    )

    ActionChains(driver).drag_and_drop(source, target).perform()

    # Validate that drop was successful
    assert "Dropped!" in target.text


def test_drag_and_drop_negative(setup):
    driver = setup
    driver.get("https://jqueryui.com/droppable/")
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))

    source = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "draggable"))
    )
    target = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "droppable"))
    )

    # Drag slightly away from the target (e.g., 50px right, 0px down)
    ActionChains(driver).drag_and_drop_by_offset(source, 50, 0).perform()

    # Validate that drop did NOT succeed
    assert "Dropped!" not in target.text
