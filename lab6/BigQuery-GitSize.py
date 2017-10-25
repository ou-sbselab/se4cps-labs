# Modification of https://cloud.google.com/bigquery/create-simple-app-api
# to report size of github repo db

import uuid
from google.cloud import bigquery

def query():
    client = bigquery.Client()
    query_job = client.run_async_query(str(uuid.uuid4()), """
        #standardSQL
        SELECT sum(size_bytes) FROM `bigquery-public-data.github_repos.__TABLES__`
        """)

    query_job.begin()
    query_job.result()  # Wait for job to complete.

    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)


if __name__ == '__main__':
    query()
