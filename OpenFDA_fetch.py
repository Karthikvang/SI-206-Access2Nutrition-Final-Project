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
    search_query = f"recall_initiation_date:[{start_date} TO {end_date}]"
    
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

def create_recall_table(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_recalls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recall_number TEXT,
            reason_for_recall TEXT,
            status TEXT,
            recalling_firm TEXT,
            product_description TEXT,
            recall_initiation_date TEXT,
            state TEXT,
            distribution_pattern TEXT,
            report_date TEXT,
            voluntary_mandated TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def insert_recall_data(db, data):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    for record in data:
        cur.execute("""
            INSERT INTO food_recalls (
                recall_number, reason_for_recall, status, recalling_firm,
                product_description, recall_initiation_date, state,
                distribution_pattern, report_date, voluntary_mandated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get("recall_number"),
            record.get("reason_for_recall"),
            record.get("status"),
            record.get("recalling_firm"),
            record.get("product_description"),
            record.get("recall_initiation_date"),
            record.get("state"),
            record.get("distribution_pattern"),
            record.get("report_date"),
            record.get("voluntary_mandated")
        ))
    
    conn.commit()
    conn.close()

def main():
        create_recall_table("A2N.db")

        summer_data = get_recall_data(API_KEY, "20240630", "20240708", limit=25)
        if summer_data:
            insert_recall_data("A2N.db", summer_data)
    
        winter_data = get_recall_data(API_KEY, "20241222", "20241228", limit=25)
        if winter_data:
            insert_recall_data("A2N.db", winter_data)

if __name__ == "__main__":
        main()
