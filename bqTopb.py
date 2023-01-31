#!/usr/bin/env python

import apache_beam as beam
import base64
from datetime import date
from google.cloud.pubsub import PublisherClient
import logging
import io
import json

class Publish(beam.DoFn):
    def __init__(self,project,topic_name):
        self.project_id = project
        self.topic_id = topic_name

    def setup(self):
        self.publisher_client = PublisherClient()
        self.topic_path = self.publisher_client.topic_path(
            project=self.project_id, topic=self.topic_id
        )
    
    def process(self,data):
        datastr = json.dumps(data, indent=4, sort_keys=True, default=str)
        print(datastr)
        self.publisher_client.publish(self.topic_path,str.encode(datastr,"utf-8"))

PROJECT='<project_id>'
BUCKET='my-test-bu123'

def run():
   argv = [
      '--project={0}'.format(PROJECT),
      '--job_name=bqtopbtopic',
      '--save_main_session',
      '--staging_location=gs://{0}/staging/'.format(BUCKET),
      '--temp_location=gs://{0}/staging/'.format(BUCKET),
      '--region=europe-west2',
      '--runner=DirectRunner'
   ]

   p = beam.Pipeline(argv=argv)

   query = "select date,confirmed_cases,geo_id,country_territory_code from `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide` where geo_id='TD'"

   # find all lines that contain the searchTerm
   (p
      | 'Read from Bigquery' >> beam.io.ReadFromBigQuery(query=query,use_standard_sql=True)
      | 'publish' >> beam.ParDo(Publish(PROJECT,"bqtopb"))
   )

   p.run()

if __name__ == '__main__':
   run()
