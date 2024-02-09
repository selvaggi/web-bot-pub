def format_authors(input_str):
    # Splitting the input string into individual entries based on the semicolon separator
    entries = input_str.split(";")

    # Initialize an empty list to hold formatted names
    formatted_names = []

    for entry in entries:
        # Removing leading and trailing whitespaces and line breaks
        cleaned_entry = " ".join(entry.strip().split())

        # Extracting the name, which is before the first '('
        name_part = cleaned_entry.split("(")[0].strip()

        # Splitting the name into first name and last name
        name_parts = name_part.split()
        first_name = name_parts[0]
        last_name = name_parts[-1]

        # Formatting the name as "LAST NAME First Initial"
        formatted_name = f"{last_name.upper()} {first_name[0].upper()}"

        formatted_names.append(formatted_name)

    # Joining the formatted names with a comma
    return ", ".join(formatted_names)


def contains_none(d):
    # Iterate through all values in the dictionary
    for key, value in d.items():
        if value is None and key not in [
            "arxiv",
        ]:
            # If any value is None, return True
            print(f"this entry has empty key: {key}")
            return True
    # If the loop completes without finding None, return False
    return False


import requests


def get_scopus_id(doi):

    api_key = "dc305301704bd81eb8a2c2222793c224"
    """
    Retrieve the Scopus ID (EID) for a given DOI.

    Parameters:
    doi (str): The DOI of the document.
    api_key (str): Your Scopus API key.

    Returns:
    str: The Scopus EID if found, None otherwise.
    """
    base_url = "https://api.elsevier.com/content/search/scopus"
    query = f"DOI({doi})"
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/json"}
    params = {"query": query}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON response
        data = response.json()
        # Check if any results were found
        if data.get("search-results", {}).get("entry"):
            # Extract the first result's EID (assuming the DOI is unique)
            scopus_id = data["search-results"]["entry"][0].get("eid")
            return scopus_id
        else:
            print("No results found for the given DOI.")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def extract_none_sublists(dict_list):
    """
    Extract sublists of dictionaries for each key where the value is None.

    Parameters:
    dict_list (list): A list of dictionaries to process.

    Returns:
    dict: A dictionary where each key corresponds to a list of dictionaries
          that have None for that particular key.
    """
    # Initialize a dictionary to hold the results
    none_lists = {}

    # Initialize the result dict with empty lists for each key
    if len(dict_list) == 0:
        return none_lists
    for key in dict_list[0].keys():
        none_lists[key] = []

    # Iterate through each dictionary in the list
    for item in dict_list:
        # Check each key-value pair in the dictionary
        for key, value in item.items():

            if key == "authors":
                if "SELVAGGI M" not in value:
                    none_lists[key].append(item)
            # If the value is None, append the dictionary to the corresponding list
            elif value is None:
                none_lists[key].append(item)

    return none_lists


def find_ut_by_doi(pub_list, doi):
    """
    Search for a DOI in a list of dictionaries and return the value of the 'ut' key if found.

    Parameters:
    pub_list (list): A list of dictionaries, each representing a publication.
    doi (str): The DOI to search for.

    Returns:
    The value of the 'ut' key for the dictionary that matches the DOI, or None if not found.
    """
    
    for pub in pub_list:
        # Check if the current dictionary has a matching 'doi' and a 'ut' key
        if pub.get("doi") == doi.upper() or pub.get("doi") == doi.lower() :
            print(doi, pub.get("ut"))
            # Return the value of 'ut' if found, else None
            return pub.get("ut")
    # Return None if no matching DOI is found or 'ut' key does not exist in the matching dict
    return None


from PyPDF2 import PdfReader, PdfWriter
import os

def reduce_pdf_size(pdf_path, output_path, size_limit_mb=10):
    # Check the initial size of the PDF
    
    ## convert in bytes
    size_limit=size_limit_mb*1024*1024
    initial_size = os.path.getsize(pdf_path)
    if initial_size <= size_limit:
        print("PDF is already under the size limit.")
        return pdf_path
    
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    for remove_pages in range(1, total_pages):
        writer = PdfWriter()
        
        # Add pages except the last 'remove_pages' number of pages
        for page_num in range(total_pages - remove_pages):
            writer.add_page(reader.pages[page_num])
        
        # Save to a temporary file to check size
        temp_output_path = output_path.rsplit('.', 1)[0] + '_temp.pdf'
        with open(temp_output_path, 'wb') as f_out:
            writer.write(f_out)
        
        # Check if the file size is within the limit now
        if os.path.getsize(temp_output_path) <= size_limit:
            os.rename(temp_output_path, output_path)
            print(f"Reduced PDF size to under {size_limit} bytes by removing {remove_pages} pages.")
            return output_path
        else:
            os.remove(temp_output_path)  # Clean up temp file
    
    print("Unable to reduce the PDF size under the limit by removing pages.")
    return None