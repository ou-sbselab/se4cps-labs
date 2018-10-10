# Modification of https://cloud.google.com/bigquery/create-simple-app-api
# to report size of github repo db

import uuid
from google.cloud import bigquery

def query():
    client = bigquery.Client()
    query_job = client.query( """
        #standardSQL
        SELECT sum(size_bytes) FROM `bigquery-public-data.github_repos.__TABLES__`
        """ )

    results = query_job.result()
    for row in results:
      print row

if __name__ == '__main__':
    query()
