import json

# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Opening JSON file
f = open("data/MicheleSelvaggi_Publons_CV_20220606.json")

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list

journals_id = {
    "Journal of High Energy Physics": "1029-8479",
    "The European Physical Journal C": "1434-6052",
    "Physical Review Letters": "0031-9007",
    "Journal of Instrumentation": "1748-0221",
    "Physics Letters B": "0217-9849",
    "Physical Review D": "2470-0029",
    "The European Physical Journal Plus": "2190-5444",
    "Physical Review C": "2469-9993",
    "Journal of Physics G: Nuclear and Particle Physics": "0954-3899",
    "EPJ Web of Conferences": "2101-6275",
    "Nuclear Physics A": "0375-9474",
    "Journal of Physics: Conference Series": "1742-6588",
    "Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment": "0168-9002",
    "Nature": "0028-0836",
    "Science": "0036-8075",
}

phys_rev_d_pre2016 = "1550-7998"
phys_rev_c_pre2016 = "0556-2813"

journal_list = []

browser = webdriver.Firefox()
browser.get("https://loginmiur.cineca.it/front.php/login.html")
browser.find_element(By.ID, "username").send_keys("SLVMHL821")
browser.find_element(By.ID, "password").send_keys("Aapplicat0!")
browser.find_element(By.NAME, "Login").click()

## find missing pub mode (not filling anything)
find_missing = True
browser.find_element(by=By.LINK_TEXT, value="Pubblicazioni").click()

if find_missing:
    browser.find_element(by=By.LINK_TEXT, value="Articolo in rivista").click()

publications = data["records"]["publication"]["list"]
number_of_publications = len(publications)

# pub_list_indices = range(1, number_of_publications+1)
pub_list_indices = [
    662,
    755,
    785,
    893,
    1017,
    1038,
    1039,
    1040,
    1041,
    1042,
    1043,
    1044,
    1045,
    1046,
    1047,
    1048,
    1049,
    1050,
    1051,
    1052,
    1053,
    1054,
    1055,
    1056,
    1057,
    1058,
    1059,
    1060,
    1061,
    1062,
    1063,
    1064,
    1065,
    1066,
    1067,
    1068,
    1069,
    1070,
    1071,
    1072,
    1073,
    1074,
    1075,
    1076,
    1077,
    1078,
    1079,
    1080,
    1081,
    1082,
    1083,
    1084,
    1085,
    1086,
    1087,
    1088,
    1089,
    1090,
    1091,
    1092,
    1093,
    1094,
]

i = 0
for pub in publications:
    i += 1

    journal_name = pub["journal"]
    # if journal_name == "Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment":
    if journal_name not in journal_list:
        journal_list.append(journal_name)

    authors = pub["publication_authors"]["authors"]
    nauth = int(pub["publication_authors"]["count"])
    title = pub["title"]
    journal_id = journals_id[pub["journal"]]
    year = pub["publication_date"].split(" ")[1]

    if int(year) < 2016:
        if pub["journal"] == "Physical Review D":
            journal_id = phys_rev_d_pre2016
        if pub["journal"] == "Physical Review C":
            journal_id = phys_rev_c_pre2016

    doi = pub["doi"]

    many = False
    if "..." in authors:
        many = True

    # print(authors)

    authors = authors.replace(" ... ", "; ")
    authors = authors.replace("; ", ";")
    authors = authors.replace(",", "")
    authors = authors.replace(".", "")

    # print(authors)
    if "Selvaggi" not in authors:
        authors = "{};Selvaggi Michele".format(authors)

    author_list = authors.split(";")
    # print(author_list)
    author_string = ""

    for a in author_list:
        aname = a.split(" ")
        # print(aname)
        alast = aname[0]
        afirst = ""
        if len(aname) > 1:
            afirst = aname[1][0]
        # print(alast, afirst)
        author_string += "{} {}; ".format(alast, afirst)

    if many:
        author_string = "{}et al;".format(author_string)

    """here fill in values"""
    if i not in pub_list_indices:
        continue

    print(i, "--------------------------------------------------------------------")
    print(author_string, title, journal_id, year, doi)

    browser.get(
        "https://alessandria.cineca.it/index.php/home/edit/classificazione_id/262"
    )
    # browser.find_element(by=By.LINK_TEXT, value="Articolo in rivista").click()
    browser.find_element(By.ID, "autore").send_keys(author_string)
    browser.find_element(By.ID, "titolo").send_keys(title)

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
    ).send_keys(journal_id)

    # browser.find_element(By.ID, "cercaRiviste_cerca_issn").send_keys(journal_id)
    # browser.find_element(by=By.ID, value="cercaRiviste_cerca_issn").send_keys(journal_id)

    # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='SELEZIONA']"))).click()
    browser.find_element(By.CLASS_NAME, "bt-cerca").click()
    WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='SELEZIONA']"))
    ).click()

    # browser.switch_to.parent_frame()

    # wait = WebDriverWait(browser, 5)
    # element = wait.until(EC.presence_of_element_located((By.ID, 'E190325')))

    window_after = browser.window_handles[0]
    browser.switch_to.window(window_after)

    browser.find_element(By.ID, "anno_pubbl_anno").send_keys(year)
    browser.find_element(By.ID, "doi").send_keys(doi)
    browser.find_element(By.CLASS_NAME, "bt-submit").click()


# for j in journal_list:
#    print(j)
print("")
print("Total number of publications: ", number_of_publications)
print("Processed number of publications: ", len(pub_list_indices))


# Closing file
f.close()
