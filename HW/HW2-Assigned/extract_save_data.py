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
    Refer to https://developers.google.com/custom-search/v1/reference/rest/v1/Search
    parameters should be properly assigned including
    key, cx, query, and dateRestrict, etc.
    If the search returns more than 100 matches, it should limit the matches 
    to 100.
    """


@app.put("/save_to_gcs")
def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """
    Access the bucket with service_account_key, and upload the object(blob)
    the the storage.
    It should return a dictionary of message.
    """

    return {"message": f"file {gcs_upload_param.file_name} has been uploaded\
            to {gcs_upload_param.bucket_name} successfully."}
