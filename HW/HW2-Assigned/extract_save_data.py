import datetime
import json


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from google.cloud import storage
from pydantic import BaseModel
import requests

from user_definition import *

app = FastAPI()


class GoogleSearch(BaseModel):
    url: str  # GoogleAPI URLs Ex. "https://www.googleapis.com/customsearch/v1"
    search_engine_id: str  # Google API's customsearch engine id
    # GCP API Key (different from service account key
    # this is for custom search)
    api_key: str
    no_days: int  # For the search restuls
    job_title: str
    company_dictionary: dict


class GcsStringUpload(BaseModel):
    service_account_key: str
    project_id: str
    bucket_name: str
    file_name: str
    data: str


@app.post("/search/jobs")
def call_google_search(search_param: GoogleSearch):
    """
    Refer to:
    https://developers.google.com/custom-search/v1/reference/rest/v1/Search
    parameters should be properly assigned including
    key, cx, query, and dateRestrict, etc.
    If the search returns more than 100 matches, it should limit the matches
    to 100.
    """
    params = {
        "key": search_param.api_key,
        "cx": search_param.search_engine_id,
        "q": search_param,
        "num": 100  # Number of search results to return (max 10)
    }

    raw_results = requests.get(
        search_param.url, params=params).json().get("items", [])[:100]

    data = {
        'company_dict': search_param.company_dictionary,
        'job_title': search_param.job_title,
        'results': raw_results
    }

    return data


@app.put("/save_to_gcs")
def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """
    Access the bucket with service_account_key, and upload the object(blob)
    the the storage.
    It should return a dictionary of message.
    """
    # GCS Setup
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file_path)
    client = storage.Client(project=gcs_upload_param.project_id,
                            credentials=credentials)
    bucket = client.bucket(gcs_upload_param.bucket_name)
    file = bucket.blob(gcs_upload_param.file_name)
    # Upload
    file.upload_from_string(gcs_upload_param.data)
    return {"message": f"file {gcs_upload_param.file_name} has been uploaded\
            to {gcs_upload_param.bucket_name} successfully."}
