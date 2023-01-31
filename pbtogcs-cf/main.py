import base64
from google.cloud import storage
import json
import time

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
#     pubsub_message = base64.b64decode((event['data']).decode('utf-8'))
    pubsub_message = base64.b64decode(event['data'])
    print(pubsub_message)
    curr_time = round(time.time()*1000)
    filename = str(curr_time)+".json"
    print(filename)
    bucket_name = 'pbtogcs_bucket'
    bucket = storage.Client().get_bucket(bucket_name)
    # 'chosen-path-to-object/{name-of-object}'
    blob = bucket.blob('output/'+filename)
    blob.upload_from_string(data=pubsub_message,content_type='application/json')  
