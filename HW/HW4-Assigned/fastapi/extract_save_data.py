import json
import datetime
import requests

from pydantic import BaseModel
from google.cloud import storage
from google.oauth2 import service_account
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from user_definition import *
from gemini_summarizer import return_gemini_summary
from meta_parser import retrieve_meta_career_qualification
from google_parser import retreive_google_career_qualification

app = FastAPI()


class SearchModel(BaseModel):
    # Query Parameters for '/search_and_save/jobs'
    job_title: str
    no_days_to_search: int = 1
    company_dict: dict


class GoogleSearch(BaseModel):
    url: str
    search_engine_id: str
    api_key: str
    no_days: int
    job_title: str
    company_dictionary: dict


class GcsStringUpload(BaseModel):
    service_account_key: str
    project_id: str
    bucket_name: str
    file_name: str
    data: str


def parse_google_search_results(search_results: dict,
                                job_list: list) -> None:
    """
    Extend job_list to be a list of dictionaries.
    Each dictionary should include title, link, snippet and date.
    title, link, and snippet are from search_results' "items".
    date is based on the snippet's "xx days ago".
    You can use the current date and xx days to calculate the date.

    Args:
        search_results (dict) : search request's response.json()
        job_list (list) : a list of dictionary with title, link,
                          snippet and date.

    """
    if "items" in search_results.keys():
        items = search_results.get("items")
        for item in items:
            if " days ago" in item["snippet"]:
                day_diff = int(item["snippet"].split(" days ago")[0])
            else:
                day_diff = 0
            date = datetime.date.today() - datetime.timedelta(days=day_diff)
            job_list.append({"title": item["title"],
                            "link": item["link"],
                             "snippet": item["snippet"],
                             "date": date.strftime('%Y-%m-%d')})


def call_google_search(search_param: GoogleSearch):
    """
    Refer to https://developers.google.com/custom-search/v1/reference/rest/v1/Search
    parameters should be properly assigned including
    key, cx, query, and dateRestrict, etc.
    If the search returns more than 100 matches, it should limit the matches
    to 100.
    """
    api_key = search_param["api_key"]
    search_engine_id = search_param["search_engine_id"]
    company_dictionary = search_param["company_dictionary"]
    no_days = search_param["no_days"]
    url = search_param["url"]
    job_title = search_param["job_title"]

    company_string = " OR site:".join(company_dictionary.values())
    query = f"{job_title} jobs on site:{company_string}"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        # d/w/m/y[number] : last [number] of days
        "dateRestrict": f"d{no_days}"
    }

    # Make the API request
    try:
        response = requests.get(url, params=params)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        no_results = int(response.json()["searchInformation"]["totalResults"])
        job_list = []
        # it can only return up to 100s.
        for i in range(0, min(no_results, 10), 10):
            params["start"] = i
            response = requests.get(url, params=params)

            search_results = response.json()
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            parse_google_search_results(search_results, job_list)
        return {"company_dict": company_dictionary,
                "job_title": job_title,
                "results": job_list}

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")
        return JSONResponse(
            status_code=response.status_code,
            content={
                "message": f"Error making API request: {e}"},
        )


def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """
    Access the bucket with service_account_key, and upload the object(blob)
    the the storage.
    It should return a dictionary of message.
    """
    credentials = service_account.Credentials.\
        from_service_account_file(gcs_upload_param["service_account_key"])
    client = storage.Client(project=gcs_upload_param["project_id"],
                            credentials=credentials)
    bucket = client.bucket(gcs_upload_param["bucket_name"])
    file = bucket.blob(gcs_upload_param["file_name"])
    blob_data = gcs_upload_param["data"]
    file.upload_from_string(blob_data,
                            content_type="application/json")
    return {"message": f"file {gcs_upload_param["file_name"]} has been uploaded\
            to {gcs_upload_param["bucket_name"]} successfully."}


def add_qualification(search_response):
    results = search_response["results"]
    for result in results:
        link = result["link"]
        if "metacareer" in link:
            qualification = retrieve_meta_career_qualification(link)
            result["qualification"] = qualification
            result["skills"] = return_gemini_summary(qualification)

        elif "google.com/about/careers" in link:
            qualification = retreive_google_career_qualification(link)
            result["qualification"] = qualification
            return_gemini_summary(qualification)
            result["skills"] = return_gemini_summary(qualification)


@app.post("/search_and_save/jobs")
def search_and_save_jobs(search_input: SearchModel):
    """
    This combines call_google_search() and save_to_gcs()
    to save the search results.
    """
    job_title = search_input.job_title
    no_days_to_search = search_input.no_days_to_search
    company_dict = search_input.company_dict
    data = {'url': google_api_url,
            'search_engine_id': search_engine_id,
            'api_key': api_key,
            'no_days': no_days_to_search,
            'job_title': job_title,
            'company_dictionary': company_dict}
    search_response = call_google_search(data)
    add_qualification(search_response)
    print(search_response)
    gcs_data = {'service_account_key': service_account_file_path,
                'project_id': project_id,
                'bucket_name': bucket_name,
                'file_name': f'{file_name_prefix}/{datetime.date.today()}.json',
                'data': json.dumps(search_response, indent=4),
                }
    save_response = save_to_gcs(gcs_data)
    return save_response
