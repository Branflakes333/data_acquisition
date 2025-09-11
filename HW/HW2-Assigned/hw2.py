import json

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd

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


if __name__ == '__main__':
    # Title should be comma separated strings of job titles in ascending order.
    # Company list on the side bar should include unique names
    # in ascending order.
    # The dataframe should be filtered based on the selection on the sidebar.
    # The dataframe should only include unique values.
    # The dataframe should have date, title, and link columns where link
    # should be a hyperlink.
    gcs_data = retrieve_data_from_gcs(service_account_file_path,
                                      project_id,
                                      bucket_name,
                                      file_name_prefix)
