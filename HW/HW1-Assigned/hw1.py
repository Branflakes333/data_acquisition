import io
import requests

import pandas as pd
import pickle
import streamlit as st

from user_definition import *


def retrieve_data_from_urls(url_list: list) -> list:
    """
    Read data from url_list and return
    a list of unique dictionaries
    which includes all the data from url in url_list.
    """
    data = []
    for url in url_list:
        d = pickle.load(io.BytesIO(requests.get(url).content))
        data.extend(d)
    data = [dict(t) for t in {tuple(d.items()) for d in data}]
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


# Everyhing below is ran each checkbox instance
st.subheader("Title")
st.title(f"{role_name} Job Listings")
st.subheader("Data Frame")

with st.sidebar:
    st.title("Sidebar")
    st.write("Filter by Company")

# Base data
data = pd.DataFrame(retrieve_data_from_urls(url_list))


st.dataframe(
    filter_by_company(data, company_dictionary),
    hide_index=True,
    column_config={
        "date": st.column_config.DatetimeColumn("Date", width=60),
        "title": st.column_config.TextColumn("Title", width="large"),
        "link": st.column_config.LinkColumn("Link", width="medium"),
    }
)
