# From https://cloud.google.com/bigquery/create-simple-app-api#bigquery-simple-app-build-service-python

import uuid
from google.cloud import bigquery

def query_shakespeare():
  client = bigquery.Client()
  query_job = client.run_async_query(str(uuid.uuid4()), """
  #standardSQL
  SELECT corpus AS title, COUNT(*) AS unique_words
  FROM `publicdata.samples.shakespeare`
  GROUP BY title
  ORDER BY unique_words DESC
  LIMIT 10""")

  query_job.begin()
  query_job.result() # Wait for completion
 
  destination_table = query_job.destination
  destination_table.reload()
  for row in destination_table.fetch_data():
    print row


if __name__ == "__main__":
  query_shakespeare()
