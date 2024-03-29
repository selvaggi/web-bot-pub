import requests
import json
from utils import *
import pandas as pd

new_dicts = []

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


journals_id = {
   
    'Phys. Lett. B': "0217-9849", 
    'Phys.Lett.B': "0217-9849", 
    'JHEP': "1029-8479", 
    'Phys.Rev.Lett.': "0031-9007", 
    'Phys. Rev. Lett.': "0031-9007", 
    'JINST': "1748-0221", 
    'Eur.Phys.J.C': "1434-6052", 
    'Eur. Phys. J. C': "1434-6052", 
    'Eur. Phys. J. ST': "1951-6355", 
    'Eur.Phys.J.ST': "1951-6355", 
    'PoS': "1824-8039", 
    'Phys. Rev. D': "2470-0029", 
    'Phys.Rev.D': "2470-0029", 
    'Rev. Phys.': "2405-4283", 
    'Rev.Phys.': "2405-4283", 
    'J.Phys.Conf.Ser.': "1742-6596", 
    'J. Phys. Conf. Ser.': "1742-6596", 
    'J. Phys. G': "1361-6471", 
    'J. Phys. G': "1361-6471", 
    'Nucl. Instrum. Meth. A': "0168-9002", 
    'Nucl.Instrum.Meth.A': "0168-9002", 
    'Eur.Phys.J.Plus': "2190-5444",
    'Eur. Phys. J. Plus': "2190-5444",
    'EPJ Web Conf.': "2101-6275",
    'Phys.Rev.C':"2469-9993",
    'Phys. Rev. C':"2469-9993",
}


# Open the JSON file and load its content into a Python dictionary
with open("data/WoS_data.json", 'r') as file:
    wos = json.load(file)  

publist_wos = wos["records"]["publication"]["list"]
print(len(publist_wos))

n_processed = 0
#for page in range(1, 26):
for page in range(1, 26):
   # Replace 'your_api_url_here' with the actual API URL you want to call
    api_url = f"https://inspirehep.net/api/literature?sort=mostcited&size=50&page={page}&q=a%20M.Selvaggi.1"
    api_url = f"https://inspirehep.net/api/literature?size=50&page={page}&q=a%20M.Selvaggi.1"

    print(f"requesting api for page {page} ... ")
    # Make the HTTP GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the JSON response to a dictionary
        data = response.json()

        # Print the dictionary nicely formatted
        # print(json.dumps(data, indent=4, sort_keys=True))

        # print(data.keys())

        for i, entry in enumerate(data["hits"]["hits"]):
            
            n_processed += 1
            entry["metadata"]

            print("")
            print(" new entry ")
            id = entry["id"]
            
            
            ## DOI
            doi = None
            
            if "dois" in entry["metadata"]:
                if len(entry["metadata"]["dois"]) > 0:
                    doi = entry["metadata"]["dois"][0]["value"]
            else:
                print(f"api call: {api_url}, entry = {i}, id = {id} has no dois keys")   
                
            ## Title
            title = None
            if len(entry["metadata"]["titles"]) == 0:
                print(f"api call: {api_url}, entry = {i} has no title, skipping ... ")
            else:
                
                for t in entry["metadata"]["titles"]:
                    if "title" in t:
                        title = t["title"]
                        break
                                   
            ## Title
            journal = None
            iisn = None
            if "journal_title_variants" in entry["metadata"]:    
                if len(entry["metadata"]["journal_title_variants"]) > 0:
                    for j in entry["metadata"]["journal_title_variants"]:
                        if j in journals_id.keys():
                            iisn = journals_id[j]
                            journal = j
                            break
               
                      
            ## Scopus unique_id
            scopus_id = None
            if doi is not None:
                scopus_id = get_scopus_id(doi)
                
            ### get WoS unique ID
            wos_id = None
            if doi is not None:
                wos_id = find_ut_by_doi(publist_wos, doi)
                
            ## publication info
            date = None
            if "publication_info" in entry["metadata"]:
                if len(entry["metadata"]["publication_info"]) > 0:
                    if "year" in entry["metadata"]["publication_info"][0]:
                        date = entry["metadata"]["publication_info"][0]["year"]

            ## arxiv number
            arxiv = None
            if "arxiv_eprints" in entry["metadata"]:
                for d in entry["metadata"]["arxiv_eprints"]:
                    if "value" in d:
                        arxiv = d["value"]
                        break
                   
            ##find link 
            url = None
            if "documents" in entry["metadata"]:
                for d in entry["metadata"]["documents"]:
                    if "source" in d:
                        if d["source"] == "SCOAP3":
                            if "url" in d:
                                url = d["url"]
                                break
            
            if url is None:
                if "documents" in entry["metadata"]:
                    for d in entry["metadata"]["documents"]:
                        #print(d.keys())
                        if "url" in d:
                            url = d["url"]
                            break
            
            if url is None:
                print("   --> could not find open access, try arXiv ... ")
                if arxiv is not None:
                    url = f"https://arxiv.org/pdf/{arxiv}.pdf"                 
                    
            if url is None:
                print(f"api call: {api_url}, entry = {i}, doi: {doi} ")
                print("   --> could REALLY not find ANY link, SKIPPING ... ")
                
                
            ## get authors
            authors = ""
            if "authors" in entry["metadata"]:
                for a in entry["metadata"]["authors"]:
                    if "last_name" in a and "first_name" in a:
                        last = a["last_name"].upper()
                        first = a["first_name"].upper()[0]
                        authors += f"{last} {first}; "
                         
                         
                                                                               
            new_dict = {
                "doi": doi,
                "title": title,
                "journal": journal,  
                "iisn": iisn,
                "scopus_id": scopus_id,
                "wos_id": wos_id,
                "date": date,
                "url": url,
                "arxiv": arxiv,
                "authors": authors
            }
            
            # Append the new dictionary to the list
            
            #if not contains_none(new_dict):
            new_dicts.append(new_dict)

    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")




print("")
print(f"{n_processed} entries processed")

n = len(new_dicts)
#print(json.dumps(new_dicts, indent=4, sort_keys=True))
# Save the list of dictionaries to a JSON file

with open("skimmed_data.json", "w") as json_file:
    json.dump(new_dicts, json_file, indent=4)

print(f"{n} entries stored to skimmed_data.json")

print("")

none_sublists = extract_none_sublists(new_dicts)
for key, none_list in none_sublists.items():                    
    if none_list:  # Only print keys with non-empty lists
        print("")        
        print(f"Key '{key}' has {len(none_list)} dictionaries with weird values values.")
        print("")
        filtered_dict_list = []
        for d in none_list:
            # If the key has the value to remove, create a copy without the key
            d_copy = {k: v for k, v in d.items() if k != "authors"}
            filtered_dict_list.append(d_copy)
            
            
        df = pd.DataFrame(filtered_dict_list)
        # Adjust display options
        pd.set_option('display.max_colwidth', 20)  # Adjust the width as needed
        pd.set_option('display.max_columns', None)  # Ensure all columns are shown
        pd.set_option('display.width', 200)  # Adjust the total width to fit your terminal or output window

        # Print the DataFrame
        print(df.to_string(index=False))



