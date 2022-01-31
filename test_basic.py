import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Locators(unittest.TestCase):
    baseUrl = "https://www.lcwaikiki.com/tr-TR/TR"
    CLOSE_COOKIE = (By.CLASS_NAME, "cookie__dismiss")
    MENU = (By.LINK_TEXT, "ERKEK")
    SUB_MENU = (By.LINK_TEXT, "Kazak")
    PRODUCT = (By.CLASS_NAME, "product-card__product-info")
    SIZE = (By.LINK_TEXT, "L")
    ADD_TO_CART_BUTTON = (By.LINK_TEXT, "SEPETE EKLE")
    CART_ITEM_COUNT = (By.ID, "spanCart")
    HOME_PAGE_LOGO = (By.CLASS_NAME, "header-logo")

    def setUp(self):
        option = Options()
        option.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
        self.driver.maximize_window()
        self.driver.get(self.baseUrl)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(15)

    def test_steps(self):
        # LCW Sitesine gidin.
        assert self.baseUrl == self.driver.current_url
        self.driver.find_element(*self.CLOSE_COOKIE).click()

        # Herhangi bir kategori sayfasına gidin.
        erkek = self.driver.find_element(*self.MENU)
        hover = ActionChains(self.driver).move_to_element(erkek)
        hover.perform()
        self.driver.find_element(*self.SUB_MENU).click()
        assert "Kazak" == self.driver.title.split("-")[0]

        # Herhangi bir ürün sayfasına gidin.
        self.driver.find_elements(*self.PRODUCT)[3].click()
        assert "urun" in self.driver.current_url

        # Ürünü sepete ekleyin.
        self.driver.find_element(*self.SIZE).click()
        self.driver.find_element(*self.ADD_TO_CART_BUTTON).click()
        assert "1" == self.wait.until(EC.visibility_of_element_located(self.CART_ITEM_COUNT)).text

        # Sepet sayfasına gidin.
        self.driver.find_element(*self.CART_ITEM_COUNT).click()
        assert "Sepetim" == self.driver.title.split(" ")[0]

        # Anasayfaya geri dönün.
        self.driver.find_element(*self.HOME_PAGE_LOGO).click()
        assert self.baseUrl == self.driver.current_url

    def tearDown(self):
        self.driver.close()
