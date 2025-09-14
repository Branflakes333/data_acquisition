import requests
import json
import io

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd
import pickle

from user_definition import *


def retrieve_data_from_gcs(service_account_key: str,
                           project_id: str,
                           bucket_name: str,
                           file_name_prefix: str
                           ) -> dict:
    """
    Retrieve file contents from all files starting with 'file_name_prefix'
    in "bucket_name" and returns a dictionary including "results",
    "job_titles", and"company_dict"

    Args:
        service_account_key (str) : path of service account key file(.json)
        project_id (str) : GCP Project ID where bucket is located
        bucket_name (str) : bucket name
        file_name_prefix (str) : prefix of files to retrieve data.
                                 (Ex."job_search/")

    Returns:
        dict: in a following format
            {"results": a list including "results" from all the files
                        starting with file_name_prefix,
             "job_titles": a list including unique "job_title"s
                           from all the files starting with file_name_prefix,
             "company_dict": a dictionary including all "company_dict"s
                            from all the files starting with file_name_prefix
            }
    """
    # GCS Accessing
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    blobs = client.list_blobs(bucket_name, prefix=file_name_prefix)

    # Get dict of data
    data = dict()
    for blob in blobs:
        data.update(blob.json)
    return data


def reorder(f):
    def wrapper(*args, **kwargs):
        df = f(*args, **kwargs)
        cols = ['date', 'title', 'link']
        try:
            return df[cols]
        except KeyError:
            return df
    return wrapper


@reorder
def filter_by_company(data: pd.DataFrame, company_dictionary: dict)\
        -> pd.DataFrame:
    """
    For the given data (data frame) and company_dictionary,
    create checkboxes (default checked) and return a new dataframe
    which only includes data being checked. If no boxes are checked,
    return an empty DataFrame with the same columns.
    """

    selected = []
    for company, link in company_dictionary.items():
        with st.sidebar:
            if st.checkbox(company, key=company, value=True):
                selected.append(link)

    if not selected:
        return data.iloc[0:0]  # return empty

    pattern = "|".join(selected)
    return data[data['link'].str.contains(pattern, case=False, na=False)]


if __name__ == '__main__':
    # Title should be comma separated strings of job titles in ascending order.
    # Company list on the side bar should include unique names
    # in ascending order.
    # The dataframe should be filtered based on the selection on the sidebar.
    # The dataframe should only include unique values.
    # The dataframe should have date, title, and link columns where link
    # should be a hyperlink.
    # gcs_data = retrieve_data_from_gcs(service_account_file_path,
    #                                   project_id,
    #                                   bucket_name,
    #                                   file_name_prefix)
    st.subheader("Title")
    st.title(f"{role_name} Job Listings")
    st.subheader("Data Frame")

    with st.sidebar:
        st.title("Sidebar")
        st.write("Filter by Company")

    # Base data
    gcs_data = pd.DataFrame(retrieve_data_from_gcs(
        service_account_key=service_account_file_path,
        project_id=project_id,
        bucket_name=bucket_name,
        file_name_prefix=file_name_prefix
    ))

    st.dataframe(
        filter_by_company(gcs_data, company_dictionary),
        hide_index=True,
        column_config={
            "date": st.column_config.DatetimeColumn("Date", width=60),
            "title": st.column_config.TextColumn("Title", width="large"),
            "link": st.column_config.LinkColumn("Link", width="medium"),
        }
    )
