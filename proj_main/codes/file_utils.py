
import os
import json

def load_stored_etag(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f).get('ETag')
    return None

def store_etag(file_path, etag):
    with open(file_path, 'w') as f:
        json.dump({'ETag': etag}, f)
