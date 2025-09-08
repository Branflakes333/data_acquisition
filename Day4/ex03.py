import datetime
import json
import os
import requests

from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import storage


def store_to_gcs(service_account_key: str,
                 project_id: str,
                 bucket_name: str,
                 file_name: str,
                 data: str) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    file = bucket.blob(file_name)
    file.upload_from_string(data)


def get_json_response(url: str, api_key: str):
    header = {'X-Api-Key': api_key}
    response = requests.get(url, headers=header)
    return response.json()


if __name__ == '__main__':
    load_dotenv(
        dotenv_path='/Users/brandonminer/usf/data_aquisition/.env')
    data_gov_api_key = os.getenv("DATA_GOV_API_KEY")
    genai_api_key = os.getenv("GCP_GENAI_API_KEY")
    service_account_key = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    file_name = f"sf_police_report/{datetime.date.today()}.json"
    url = 'https://data.sfgov.org/resource/wg3w-h783'
    data = get_json_response(url, data_gov_api_key)
    store_to_gcs(service_account_key,
                 project_id,
                 bucket_name,
                 file_name,
                 json.dumps(data, indent=4))
