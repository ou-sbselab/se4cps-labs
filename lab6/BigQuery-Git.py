# Modification of https://cloud.google.com/bigquery/create-simple-app-api
# to check for FIXME or TODO in GitHub

import uuid
from google.cloud import bigquery

def query():
    client = bigquery.Client()
    query_job = client.query( """
      SELECT SUM(copies) FROM `bigquery-public-data.github_repos.sample_contents` WHERE NOT binary AND (content LIKE '%FIXME%' OR content LIKE '%TODO%')
        """ )

    results = query_job.result()
    for row in results:
      print row


if __name__ == '__main__':
    query()
