import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BritishTelecom:

    def __init__(self, header, arg1, arg2, storage, arg3, arg4, final_cost):
        self.final_cost = final_cost
        self.header = header
        self.arg1 = arg1
        self.arg2 = arg2
        self.storage = storage
        self.arg3 = arg3
        self.arg4 = arg4
    def launchBrowser(self):
        """Launching a firefox browser using executable path"""
        opt1 = webdriver.FirefoxOptions()
        self.br_driver = webdriver.Firefox(service=FirefoxService(executable_path='.\geckodriver.exe'))
        self.br_driver.get("https://www.bt.com/")
        self.br_driver.maximize_window()
        self.br_driver.set_page_load_timeout(60)
    def accept_alert(self):
        """ Handling popup alert using frames"""
        self.launchBrowser()
        time.sleep(3)
        frame = self.br_driver.find_element(By.XPATH, '//iframe[@class="truste_popframe"]')
        self.br_driver.switch_to.frame(frame)
        time.sleep(2)
        self.br_driver.find_element(By.XPATH, '//div[@class="pdynamicbutton"]/a[@class="call"]').click()
        time.sleep(2)
        self.br_driver.switch_to.default_content()
    def mouse_hover(self, by_locator):
        """ mouse hover action by using action chains class"""
        WebDriverWait(self.br_driver, 10).until(EC.visibility_of_element_located(by_locator))
        act_chains = ActionChains(self.br_driver)
        element = self.br_driver.find_element(*by_locator)
        act_chains.move_to_element(element).click().perform()
    def scrollele(self, by_locator):
        """ scrolling to the defined element"""
        element = self.br_driver.find_element(*by_locator)
        self.br_driver.execute_script("return arguments[0].scrollIntoView();", element)
    def verifyMobileBanner(self):
        """ Hovering to the mobile menu and clicking on mobile phones button"""
        self.accept_alert()
        time.sleep(2)
        mobileBtn = By.XPATH, '//a[@data-di-id="di-id-7c56fcc8-3103e56f"]'
        self.mouse_hover(mobileBtn)
        time.sleep(2)
        self.br_driver.find_element(By.LINK_TEXT, "Mobile phones").click()
        time.sleep(2)
        btn = By.XPATH, '//a[@class="bt-btn bt-btn-primary mt-2 mb-12"]'
        self.scrollele(btn)
        self.bannersCount = self.br_driver.find_elements(By.XPATH, '//div[@class="flexpay-card_card_wrapper__Antym"]')
        print(len(self.bannersCount))
        assert int(len(self.bannersCount)) >= 3
    def verifyPageTitle(self):
        """ Verifying page title """
        self.verifyMobileBanner()
        simOnlyBtn = By.XPATH, '//a[@class="bt-btn bt-btn-primary"]'
        self.scrollele(simOnlyBtn)
        time.sleep(2)
        self.br_driver.find_element(By.LINK_TEXT, "View SIM only deals").click()
        time.sleep(3)
        title = self.br_driver.title
        print("Title of the page is ", title)
        return title
    def validateData(self):
        """ Using dynamic relative xpath, validating the UI part from user inputs"""
        self.verifyPageTitle()
        time.sleep(2)
        btn2 = By.XPATH, '//div[@class="simo-card-ee_product_card_wrapper__25TU6 mt-10"][2]/div[1]'
        self.scrollele(btn2)
        time.sleep(2)
        try:
            data1 = self.br_driver.find_elements(By.XPATH, '//div[contains(text(), "' + str(self.header) +'")]/parent::div//span[text()="' + str(self.arg1) + '" and "' + str(self.arg2) + '"]/following-sibling::div[text()="' + str(self.storage) + '"]/following-sibling::span[text()="' + str(self.arg3) + '"]//parent::div//following-sibling::div/span[text()="' + str(self.arg1) + '" and "' + str(self.arg4) + '"]/following-sibling::div[@class="simo-card-ee_pricing__3fYly"]')
            if len(data1) < 0:
                assert False, "No Banners available"
            containers = []
            for element in range(len(data1)):
                data2 = self.br_driver.find_elements(By.XPATH, '//div[contains(text(), "' + str(self.header) +'")]/parent::div//span[text()="' + str(self.arg1) + '" and "' + str(self.arg2) + '"]/following-sibling::div[text()="' + str(self.storage) + '"]/following-sibling::span[text()="' + str(self.arg3) + '"]//parent::div//following-sibling::div/span[text()="' + str(self.arg1) + '" and "' + str(self.arg4) + '"]/following-sibling::div[@class="simo-card-ee_pricing__3fYly"]')
                print("values of banner amounts ", data2[element].text)
                cost_value = data2[element].text
                if cost_value.__contains__(self.final_cost):
                    containers.append(1)
                else:
                    containers.append(0)
            if containers.count(1) < 1:
                assert False, "Banners with £18.90 are not available"
            else:
                assert True, "Banners with £18.90 are available"
        except(AssertionError):
            print("No Banner available in UI")
    def closeBrowser(self):
        """ Closing the browser after all operations done"""
        self.validateData()
        self.br_driver.quit()

obj = BritishTelecom("30% off and double data", "was ", "125GB", "250GB", "Essential Plan", "£27", "£18.90")
obj.closeBrowser()



#//div[contains(text(), "30% off and double data")]/parent::div//span[text()="125GB" and @class="simo-card-ee_was_data__37BKi"]
#//span[text()="125GB" and @class="simo-card-ee_was_data__37BKi"]/ancestor::div/div[text()="30% off and double data"]
#//div[contains(text(), "30% off and double data")]/parent::div//span[text()="Essential Plan"]
#//div[contains(text(), "30% off and double data")]/parent::div//span[text()="Essential Plan"]//parent::div//following-sibling::div/span[text()="was " and "£25"]/following-sibling::div[@class="simo-card-ee_pricing__3fYly"]



