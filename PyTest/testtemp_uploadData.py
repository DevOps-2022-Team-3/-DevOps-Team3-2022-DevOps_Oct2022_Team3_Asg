import selenium
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import time

def test_setUp():
    global driver
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

    global linkToReturnTo
    linkToReturnTo = "http://127.0.0.1:5221/Upload_Data"
    driver.get(linkToReturnTo)

################## Test navigation bar (Keep this for every page) ##################
def goToNavPage(pageLink):
    #Find and click Nav button
    uploadDataBtn = driver.find_element(by=By.ID, value=pageLink)
    uploadDataBtn.click()

def test_enterUploadData():
    driver.get(linkToReturnTo)
    goToNavPage("upload-data-btn")
    assert driver.title == "Upload Data"

def test_enterMatchStudent():
    driver.get(linkToReturnTo)
    goToNavPage("match-student-btn")
    assert driver.title == "Match Students"

def test_enterPrepareEmail():
    driver.get(linkToReturnTo)
    goToNavPage("prepare-email-btn")
    assert driver.title == "Prepare Email"

def test_enterSettings():
    driver.get(linkToReturnTo)
    goToNavPage("settings-btn")
    assert driver.title == "Settings"
################## Test navigation bar (Keep this for every page) ##################

def test_uploadStudentData():
    print()

def test_uploadCompanyData():
    print()

######## End Code (Keep this for every page) ########
def test_end():
    driver.close()
    driver.quit()
    print("Testing Done")
######## End Code (Keep this for every page) ########