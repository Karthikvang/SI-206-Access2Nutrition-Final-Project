import sqlite3

def fetch_recalls_by_region_month(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT
        CASE
            WHEN state IN ('ME','NH','VT','MA','RI','CT','NY','NJ','PA') THEN 'Northeast'
            WHEN state IN ('OH','MI','IN','IL','WI','MN','IA','MO','ND','SD','NE','KS') THEN 'Midwest'
            WHEN state IN ('DE','MD','DC','VA','WV','NC','SC','GA','FL','KY','TN','MS','AL','OK','TX','AR','LA') THEN 'South'
            ELSE 'West'
        END AS region,
        CASE substr(recall_initiation_date,5,2)
            WHEN '12' THEN 'Winter' WHEN '01' THEN 'Winter' WHEN '02' THEN 'Winter'
            WHEN '03' THEN 'Spring' WHEN '04' THEN 'Spring' WHEN '05' THEN 'Spring'
            WHEN '06' THEN 'Summer' WHEN '07' THEN 'Summer' WHEN '08' THEN 'Summer'
            WHEN '09' THEN 'Fall'   WHEN '10' THEN 'Fall'   WHEN '11' THEN 'Fall'
        END AS season,
        COUNT(*) AS recall_count
        FROM food_recalls
        GROUP BY region, season
        ORDER BY region,
        CASE season
            WHEN 'Winter' THEN 1
            WHEN 'Spring' THEN 2
            WHEN 'Summer' THEN 3
            WHEN 'Fall'   THEN 4
        END;
    """)
    
    rows = cur.fetchall()
    conn.close()

    recalls = {}
    for region, season, count in rows:
        if region not in recalls:
            recalls[region] = {}
        recalls[region][season] = count

    return recalls


