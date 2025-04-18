import sqlite3
import json

def fetch_recalls_by_region_month(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT
          CASE
            WHEN state IN ('ME','NH','VT','MA','RI','CT','NY','NJ','PA') THEN 'East'
            WHEN state IN ('OH','MI','IN','IL','WI','MN','IA','MO','ND','SD','NE','KS') THEN 'Midwest'
            WHEN state IN ('DE','MD','DC','VA','WV','NC','SC','GA','FL','KY','TN','MS','AL','OK','TX','AR','LA') THEN 'Central'
            ELSE 'West'
          END AS region,

          CASE recall_initiation_month
            WHEN 12 THEN 'Winter' WHEN 1 THEN 'Winter'  WHEN 2 THEN 'Winter'
            WHEN 3  THEN 'Spring' WHEN 4 THEN 'Spring' WHEN 5 THEN 'Spring'
            WHEN 6  THEN 'Summer' WHEN 7 THEN 'Summer' WHEN 8 THEN 'Summer'
            WHEN 9  THEN 'Fall'   WHEN 10 THEN 'Fall'   WHEN 11 THEN 'Fall'
          END AS season,

          COUNT(*) AS recall_count
        FROM food_recalls
        GROUP BY region, season
        ORDER BY
          region,
          CASE recall_initiation_month
            WHEN 12 THEN 1 WHEN 1 THEN 1 WHEN 2 THEN 1
            WHEN 3  THEN 2 WHEN 4 THEN 2 WHEN 5 THEN 2
            WHEN 6  THEN 3 WHEN 7 THEN 3 WHEN 8 THEN 3
            WHEN 9  THEN 4 WHEN 10 THEN 4 WHEN 11 THEN 4
          END;
    """)
    
    rows = cur.fetchall()
    conn.close()

    recalls = {}
    for region, season, count in rows:
        if region not in recalls:
            recalls[region] = {}
        recalls[region][season] = count

    print(recalls)
    return recalls

def write_recalls_to_json(data, filename='recalls_by_region.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data written to {filename}")

def main():
     data = fetch_recalls_by_region_month('A2N.db')
     write_recalls_to_json(data)

if __name__ == "__main__":
        main()
