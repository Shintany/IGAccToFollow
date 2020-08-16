from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

class InstaBot:
    def __init__(self, username,  password, account):
        if (username == '' or password == ''): raise Exception("username or password string is empty")

        self.username = username
        self.password = password
        self.workingAccount = account
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://instagram.com")
        sleep(2)

    def LogIn(self):
        # Credentials
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
        sleep(2)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()

        # Save credientials pop-up
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()

        # Activate notifications pop-up
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()

    def GoToWorkingAccountPage(self):
        self.driver.get("https://instagram.com/" + self.workingAccount + "/")

    def GoToAccountPage(self, username):
        self.driver.get("https://instagram.com/" + username + "/")

    def GetAccountPageFollowing(self):
        self.driver.find_element_by_xpath("//a[@href=\"/{}/following/\"]".format(self.workingAccount)).click()

        # TODO: The app might still change in future. If timeout exception happens again, just change the path of the elements below. 
        self.MakeDriverWait("/html/body/div[4]/div/div/div[2]")
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            try:
                ht = self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
            except StaleElementReferenceException:
                continue
        self.MakeDriverWait('a', "tag_name")
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.MakeDriverWait("/html/body/div[4]/div/div/div[1]/div/div[2]/button")
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return names
        sleep(2)

    def GetAccountFollowersAmount(self, username):
        self.GoToAccountPage(username)
        try:
            amount = self.driver.find_element_by_xpath("//a[@href=\"/{}/followers/\"]".format(username)).find_element_by_tag_name('span').get_attribute("title")
            return amount
        except NoSuchElementException:
            return 0

    def GoToHomePage(self):
        self.driver.find_element_by_xpath("//a[@href=\"/\"]").click()

    def IsAttributePresent(element, attr):
        value = element.get_attribute(attr)
        if value == '' : return false
        return true

    def MakeDriverWait(self, element_to_locate, by='xpath'):
        wait = WebDriverWait(self.driver, 20)
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, element_to_locate)))
        elif by == 'class_name':
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, element_to_locate)))
        elif by == 'tag_name':
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, element_to_locate)))

    def quit(self):
        sleep(3)
        self.driver.quit()