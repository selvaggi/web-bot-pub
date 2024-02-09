import requests
import json
from utils import *
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os

# executable_path='/home/michele/Programs/geckodriver'
# service = Service(executable_path=executable_path)

# Create a Firefox browser instance with the specified geckodriver
# browser = webdriver.Firefox(service=service)

# Open the JSON file and load its content into a Python dictionary
with open("skimmed_data.json", "r") as file:
    pubs = json.load(file)

fill = True

if fill:
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    browser.get("https://loginmiur.cineca.it/front.php/login.html")
    browser.find_element(By.ID, "username").send_keys("SLVMHL821")
    browser.find_element(By.ID, "password").send_keys("Applicat0-")
    browser.find_element(By.NAME, "Login").click()
    browser.find_element(by=By.LINK_TEXT, value="Pubblicazioni").click()

publications = pubs
number_of_publications = len(publications)
print(number_of_publications)

nmax = 9999
nmin = 1181
if fill:
    nmax = 9999

ncount = 0
for i, pub in enumerate(publications):
    if i < nmin:
        continue
    if i > nmax:
        break
    
    if i == 1029:
        continue

    if pub["scopus_id"] is None and pub["wos_id"] is None:
        continue

    if not pub["doi"]:
        continue

    if not pub["date"]:
        continue

    if not pub["url"]:
        continue

    if int(pub["date"]) < 2016:
        if pub["journal"] == "Phys. Rev. D" or pub["journal"] == "Phys.Rev.D":
            pub["iisn"] = "1550-7998"
        if pub["journal"] == "Phys. Rev. C" or pub["journal"] == "Phys.Rev.C":
            pub["iisn"] = "0556-2813"

    if (
        pub["doi"] == "10.1038/s41586-022-04892-x"
        or pub["doi"] == "10.1038/nature14474"
    ):
        pub["journal"] = "Nature"
        pub["iisn"] = "0028-0836"

    if (
        pub["doi"] == "10.1038/nphys3005"
        or pub["doi"] == "10.1038/s41567-022-01682-0"
    ):
        pub["journal"] = "Nature Physics"
        pub["iisn"] = "1745-2473"
        
    if (
        pub["doi"] == "10.1007/s41781-020-00041-z"
    ):
        pub["journal"] = "Comput.Softw.Big Sci."
        pub["iisn"] = "2510-2036"   
    
    
    if (
        pub["doi"] == "10.1088/2632-2153/ab9023"
    ):
        pub["journal"] = "Mach.Learn.Sci.Tech. 1"
        pub["iisn"] = "2632-2153"   

    if (
        pub["doi"] == "10.1126/science.1230816"
    ):
        pub["journal"] = "Science"
        pub["iisn"] = "0036-8075"   
   

    if fill:
        # time.sleep(5)  # Wait for 5 seconds
        print(i, "--------------------------------------------------------------------")
        print(
            pub["doi"],
            pub["journal"],
            pub["scopus_id"],
            pub["wos_id"],
            pub["date"],
            pub["url"],
        )
        browser.get(
            "https://alessandria.cineca.it/index.php/home/edit/classificazione_id/262"
        )
        # time.sleep(5)  # Wait for 5 seconds
        # browser.find_element(by=By.LINK_TEXT, value="Articolo in rivista").click()

        if len(pub["authors"]) > 200:
            pub["authors"] = "SELVAGGI M; ET AL"
        browser.find_element(By.ID, "autore").send_keys(pub["authors"])
        print(pub["authors"])
        browser.find_element(By.ID, "titolo").send_keys(pub["title"])
        print(pub["title"])

        # text exists in page
        browser.find_element(By.CLASS_NAME, "bt-cerca").click()
        # wait = WebDriverWait(browser, 10)

        widget = browser.find_element(
            By.XPATH, "//iframe[@class='ui-dialog-content ui-widget-content']"
        )
        browser.switch_to.frame(widget)
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-dialog ui-widget ui-widget-content ui-corner-all')))
        # element = wait.until(EC.presence_of_element_located((By.ID, 'cercaRiviste_cerca_issn')))
        # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='ANNULLA']"))).click(
        # element = wait.until(EC.visibility_of_element_located((By.ID, 'cercaRiviste_cerca_issn')))

        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, "cercaRiviste_cerca_issn"))
        ).send_keys(pub["iisn"])

        # browser.find_element(By.ID, "cercaRiviste_cerca_issn").send_keys(journal_id)
        # browser.find_element(by=By.ID, value="cercaRiviste_cerca_issn").send_keys(journal_id)

        # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='SELEZIONA']"))).click()
        browser.find_element(By.CLASS_NAME, "bt-cerca").click()
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='SELEZIONA']"))
        ).click()
        print(pub["iisn"])

        # browser.switch_to.parent_frame()

        # wait = WebDriverWait(browser, 5)
        # element = wait.until(EC.presence_of_element_located((By.ID, 'E190325')))

        window_after = browser.window_handles[0]
        browser.switch_to.window(window_after)

        browser.find_element(By.ID, "anno_pubbl_anno").send_keys(pub["date"])
        print(pub["date"])
        browser.find_element(By.ID, "doi").send_keys(pub["doi"])
        print(pub["doi"])
        # browser.find_element(By.CLASS_NAME, "bt-submit").click()

        # time.sleep(10)
        print(pub["scopus_id"])
        print(pub["wos_id"])
        if pub["scopus_id"] is not None:
            select_element = Select(
                browser.find_element(By.ID, "codici_esterni_0_sistema_esterno_id")
            )
            select_element.select_by_value("1")

            # Enter "text" into the input field
            input_element = browser.find_element(By.ID, "codici_esterni_0_codice")
            input_element.send_keys(pub["scopus_id"])

            browser.find_element(By.NAME, "conferma").click()

            if pub["wos_id"] is not None:
                select_element = Select(
                    browser.find_element(By.ID, "codici_esterni_1_sistema_esterno_id")
                )
                select_element.select_by_value("2")

                # Enter "text" into the input field
                input_element = browser.find_element(By.ID, "codici_esterni_1_codice")
                input_element.send_keys(pub["wos_id"])
                browser.find_element(By.NAME, "conferma").click()
        else:
            select_element = Select(
                browser.find_element(By.ID, "codici_esterni_0_sistema_esterno_id")
            )
            select_element.select_by_value("2")

            # Enter "text" into the input field
            input_element = browser.find_element(By.ID, "codici_esterni_0_codice")
            input_element.send_keys(pub["wos_id"])
            browser.find_element(By.NAME, "conferma").click()

        print(pub["url"])

        browser.find_element(By.ID, "url").send_keys(pub["url"])

        ## now download and upload file

        doi_str = pub["doi"].replace("/", "__")
        doi_str = doi_str.replace("(", "__")
        doi_str = doi_str.replace(")", "__")

        pdf_path = os.path.join(os.getcwd(), f"{doi_str}.pdf")
        curl_cmd = f"curl -L -o {pdf_path} {pub['url']}"
        print(curl_cmd)
        os.system(curl_cmd)

        time.sleep(2)
        allegati_link = browser.find_element(By.LINK_TEXT, "Allegati")
        allegati_link.click()

        # Path to your PDF file
        max_size_mb = 5
        reduce_pdf_size(pdf_path, pdf_path, max_size_mb)
        # Find the <input type="file"> element using the newer method and send the file path to it
        file_input = browser.find_element(
            By.CSS_SELECTOR, "input[type='file'][name='file']"
        )
        file_input.send_keys(pdf_path)
        time.sleep(5)
        os.system(f"rm {pdf_path} ")

# button_upload = browser.find_element(By.NAME, "Carica file")
# button_upload.click()

print(ncount)
