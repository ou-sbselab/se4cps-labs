# Code from https://cloud.google.com/bigquery/create-simple-app-api

import uuid
from google.cloud import bigquery

def query_shakespeare():
    client = bigquery.Client()
    query_job = client.query("""
        #standardSQL
        SELECT corpus AS title, COUNT(*) AS unique_words
        FROM `publicdata.samples.shakespeare`
        GROUP BY title
        ORDER BY unique_words DESC
        LIMIT 10""")

    results = query_job.result()
    for row in results:
      print "{} : {} unique words".format(row.title, row.unique_words)

if __name__ == '__main__':
    query_shakespeare()
