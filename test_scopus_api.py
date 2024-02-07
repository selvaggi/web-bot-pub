
import requests

def get_scopus_id(doi, api_key):
    """
    Retrieve the Scopus ID (EID) for a given DOI.

    Parameters:
    doi (str): The DOI of the document.
    api_key (str): Your Scopus API key.

    Returns:
    str: The Scopus EID if found, None otherwise.
    """
    base_url = 'https://api.elsevier.com/content/search/scopus'
    query = f'DOI({doi})'
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    params = {'query': query}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON response
        data = response.json()
        # Check if any results were found
        if data.get('search-results', {}).get('entry'):
            # Extract the first result's EID (assuming the DOI is unique)
            scopus_id = data['search-results']['entry'][0].get('eid')
            return scopus_id
        else:
            print("No results found for the given DOI.")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage
api_key = 'dc305301704bd81eb8a2c2222793c224'  # Replace with your actual Scopus API key
doi = '10.1007/JHEP02(2014)057'  # Example DOI
scopus_id = get_scopus_id(doi, api_key)
if scopus_id:
    print(f"Scopus EID: {scopus_id}")
else:
    print("Scopus EID could not be retrieved.")

