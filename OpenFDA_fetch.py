import requests
import sqlite3


API_KEY = "xmlDEL0okHlfnLCqKDM4Pj0LhxeE2u44lZ6dnh1O"

def get_recall_data(api_key, start_date, end_date, limit=5):
    """
    Retrieves food recall enforcement data from the OpenFDA API.
    
    Parameters:
      api_key (str): Your API key.
      start_date (str): The recall initiation start date in 'YYYYMMDD' format.
      end_date (str): The recall initiation end date in 'YYYYMMDD' format.
      limit (int): The maximum number of results to return (default is 5).
    
    Returns:
      list: A list of recall data records, or None if an error occurred.
    """
    base_url = "https://api.fda.gov/food/enforcement.json"
    
    # Build the search query based on the recall initiation date range.
    search_query = f"recall_initiation_date:[{start_date}+TO+{end_date}]"
    
    params = {
        "api_key": api_key,
        "search": search_query,
        "limit": limit
    }
    
    response = requests.get(base_url, params=params)
    
    if response.ok:
        data = response.json()
        return data.get("results", [])
    else:
        print("Error:", response.status_code, response.text)
        return None

def create_recall_table(conn, cur, data):
    pass


