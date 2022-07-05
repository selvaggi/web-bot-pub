import json
import math

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
# Closing file
f.close()


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


browser = webdriver.Firefox()
browser.get("https://loginmiur.cineca.it/front.php/login.html")
browser.find_element(By.ID, "username").send_keys("SLVMHL821")
browser.find_element(By.ID, "password").send_keys("Aapplicat0!")
browser.find_element(By.NAME, "Login").click()

browser.find_element(by=By.LINK_TEXT, value="Pubblicazioni").click()
browser.find_element(by=By.LINK_TEXT, value="Articolo in rivista").click()


# create big string with dump of all possible sources
source = browser.page_source

publications = data["records"]["publication"]["list"]
number_of_publications = len(publications)
pub_per_page = 100
number_of_pages = int(math.ceil(number_of_publications / pub_per_page))

for k in range(2, number_of_pages + 1):
    addr = "https://alessandria.cineca.it/index.php/home/cerca/class/262/ordine/class?page={}".format(
        k
    )
    print(k)
    browser.get(addr)
    source += browser.page_source

i = 0
found = False

missing_list = []
duplicate_list = []

duplicate_dict = dict()

for pub in data["records"]["publication"]["list"]:
    i += 1

    journal_name = pub["journal"]
    authors = pub["publication_authors"]["authors"]
    nauth = int(pub["publication_authors"]["count"])
    title = pub["title"]
    journal_id = journals_id[pub["journal"]]
    year = pub["publication_date"].split(" ")[1]
    doi = pub["doi"]

    duplicate_dict["doi"] = 0

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

    if doi not in source:
        print(
            i,
            "--------------------------------------------------------------------",
        )
        print(author_string, title, journal_id, year, doi)
        missing_list.append(i)

    number_of_occurences = source.count(doi)
    if number_of_occurences > 1:
        print("duplicate: ", i, author_string, title, journal_id, year, doi)

list_items = "pub_list_indices = ["
for i in missing_list:
    if i != missing_list[-1]:
        list_items += "{}, ".format(i)
    else:
        list_items += "{}".format(i)

list_items += "]"
print("")
print(list_items)
