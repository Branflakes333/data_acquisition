import datetime
import json
import os

from dotenv import load_dotenv
import requests

from user_definition import *

load_dotenv()

data = {'url': google_api_url,
        'search_engine_id': search_engine_id,
        'api_key': api_key,
        'no_days': no_days_to_search,
        'job_title': role_name,
        'company_dictionary': company_dictionary}
search_response = requests.post(f'{api_server_url}/search/jobs', json=data)
print(
    f"search_response status: {search_response.status_code}")

data = {'service_account_key': service_account_file_path,
        'project_id': project_id,
        'bucket_name': bucket_name,
        'file_name': f'jobs_search/{datetime.date.today()}.json',
        'data': json.dumps(search_response.json(), indent=4),
        }
upload_response = requests.put(f'{api_server_url}/save_to_gcs', json=data)
print(f"upload_response status: {upload_response.status_code}")
