
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link_cineca = "https://loginmiur.cineca.it/front.php/login.html"
link_form = "https://asn21.cineca.it/user/auto-auth?UANAUTH=amCapc%2FUjYZONV6GD7avh8XC%2BNDZgfdKNd9T3BulMk5OdeN0O0REeRaPhfC%2FLLxOF54m1NQb8WBgxkVrUAYjwRJ2PPz8eiQ2kH5XfeC6moQDqG7ipcYlmgI83dh%2BpQbF2axoFlLg72vDO%2Bm4uzHtLbpdxRKbNBnFxXbmzVOCVEuBdlr%2BUZBPcxTDfziJVpAq&target=private_dispatch"
link_pubs = "https://alessandria.cineca.it/index.php/"
link_pubs = "https://alessandria.cineca.it/index.php/home/cerca/class/262/ordine/class"

options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get("https://loginmiur.cineca.it/front.php/login.html")
# browser.get(link_pubs)

# click on Log in with

browser.find_element(By.ID, "username").send_keys("SLVMHL821")
browser.find_element(By.ID, "password").send_keys("Applicat0-")
browser.find_element(By.NAME, "Login").click()


## link per l'applicazione
# browser.get("")

# browser.get("https://asn21.cineca.it/user/auto-auth?UANAUTH=amCapc%2FUjYZONV6GD7avh8XC%2BNDZgfdKNd9T3BulMk5OdeN0O0REeRaPhfC%2FLLxOF54m1NQb8WBgxkVrUAYjwRJ2PPz8eiQ2kH5XfeC6moQDqG7ipcYlmgI83dh%2BpQbF2axoFlLg72vDO%2Bm4uzHtLbpdxRKbNBnFxXbmzVOCVEuBdlr%2BUZBPcxTDfziJVpAq&target=private_dispatch")


browser.find_element(by=By.LINK_TEXT, value="Pubblicazioni").click()
browser.find_element(by=By.LINK_TEXT, value="Articolo in rivista").click()


for i in range(5):
    browser.find_element(By.CLASS_NAME, "bt-elimina").click()
    browser.find_element(By.CLASS_NAME, "bt-elimina").click()
