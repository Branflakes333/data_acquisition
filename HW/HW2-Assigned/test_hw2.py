import json

from fastapi.testclient import TestClient
from google.oauth2 import service_account
from google.cloud import storage

from extract_save_data import app
from hw2 import retrieve_data_from_gcs
from user_definition import *

# -------------------------
# FASTAPI TESTS
# -------------------------

client = TestClient(app)


def delete_gcs_items(bucket_name, prefix):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file_path)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    for blob in blobs:
        if blob.name.startswith(prefix):
            blob.delete()


def test_search_jobs_success():
    """Test /search/jobs endpoint returns expected format"""
    data = {'url': google_api_url,
            'search_engine_id': search_engine_id,
            'api_key': api_key,
            'no_days': 3,
            'job_title': "engineer",
            'company_dictionary': company_dictionary}
    response = client.post("/search/jobs", json=data)
    assert response.status_code == 200
    data = response.json()

    assert "company_dict" in data
    assert "job_title" in data
    assert "results" in data
    assert isinstance(data["results"], list)
    assert all("title" in job for job in data["results"])


def test_save_to_gcs_success():
    """Test /save_to_gcs uploads correctly"""
    prefix = "pytest_upload_to_gcs"
    delete_gcs_items(bucket_name,
                     "pytest_upload_to_gcs")
    param = {
        "service_account_key": service_account_file_path,
        "project_id": project_id,
        "bucket_name": bucket_name,
        "file_name": prefix + "_1.json",
        "data": json.dumps({"company_dict": company_dictionary,
                            "job_title": "Scientist",
                            "results": [
                                {"title": "data scientist",
                                 "link": "https://careers.microsoft.com/",
                                 "snippet": "...",
                                 "date": "2025-09-03"},
                                {"title": "data scientist",
                                 "link": "https://www.metacareers.com/jobs",
                                 "snippet": "...",
                                 "date": "2025-09-01"}]})
    }
    response = client.put("/save_to_gcs", json=param)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "uploaded" in data["message"]

    param["job_title"] = "Engineer"
    param["file_name"] = prefix + "_2.json"
    param["data"] = json.dumps({"company_dict": company_dictionary,
                                "job_title": "Engineer",
                               "results": [
                                {"title": "Engineer",
                                 "link": "https://careers.microsoft.com/something",
                                 "snippet": "...",
                                    "date": "2025-09-03"}]})
    response = client.put("/save_to_gcs", json=param)
    assert response.status_code == 200


# -------------------------
# STREAMLIT HELPER TESTS
# -------------------------


def test_retrieve_data_from_gcs(monkeypatch, tmp_path):
    """Test retrieving job postings from GCS"""
    output = retrieve_data_from_gcs(service_account_file_path,
                                    project_id,
                                    bucket_name,
                                    "pytest_upload_to_gcs")
    assert "results" in output
    assert "job_titles" in output
    assert "company_dict" in output
    assert len(output["results"]) == 3
    # Alphabetical order
    assert ["Engineer", "Scientist"] == output["job_titles"]


# -------------------------
# CODE QUALITY
# -------------------------


def test_hw2_pep8():
    """Ensure code passes pycodestyle with fewer than 5 issues"""
    import subprocess
    result = subprocess.run(
        ["pycodestyle", "hw2.py"],
        capture_output=True,
        text=True
    )
    errors = result.stdout.strip().splitlines()
    assert len(errors) < 5, f"Too many PEP8 issues:\n{errors}"


def test_fastapi_pep8():
    """Ensure code passes pycodestyle with fewer than 5 issues"""
    import subprocess
    result = subprocess.run(
        ["pycodestyle", "extract_save_data.py"],
        capture_output=True,
        text=True
    )
    errors = result.stdout.strip().splitlines()
    assert len(errors) < 5, f"Too many PEP8 issues:\n{errors}"
