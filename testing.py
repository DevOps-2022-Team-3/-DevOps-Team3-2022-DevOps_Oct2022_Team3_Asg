import selenium
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

def test_enterUploadData():
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5221/Main")

    # Check correct page
    #assert driver.title == "Main"

    driver.implicitly_wait(3)

    #Find and click Upload Data button
    uploadDataBtn = driver.find_element(by=By.ID, value="upload_data_btn")
    uploadDataBtn.click()

    assert driver.title == "Upload Data"

    driver.quit()