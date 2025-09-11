import datetime
from io import BytesIO
import pickle
from urllib.parse import urlparse

import pytest
import pandas as pd
from streamlit.testing.v1 import AppTest

import hw1


@pytest.fixture
def sample_data():
    """Fixture to provide sample job listing data."""
    return [
        {
            "title": "Data Scientist | Meta",
            "link": "https://www.metacareers.com/jobs/123",
            "snippet": "Analyze data at Meta.",
            "date": datetime.date(2025, 8, 15),
        },
        {
            "title": "Data Scientist | Meta",
            "link": "https://www.metacareers.com/jobs/123",
            "snippet": "Analyze data at Meta.",
            "date": datetime.date(2025, 8, 15),
        },
        {
            "title": "ML Engineer | Google",
            "link": "https://www.google.com/about/careers/applications/jobs/456",
            "snippet": "Develop ML models at Google.",
            "date": datetime.date(2025, 8, 13),
        },
    ]


@pytest.fixture
def pickle_data(sample_data):
    """Fixture to provide sample pickled job listing data."""
    return BytesIO(pickle.dumps(sample_data))


def test_retrieve_data_from_urls():
    """Test the retrieve_data_from_urls function."""
    data = hw1.retrieve_data_from_urls(["https://storage.googleapis.com"
                                        "/msds692-hw1-public/job_list.pkl"])
    assert isinstance(data, list)
    assert len(data) == 97


def test_filter_by_company_meta_only(monkeypatch):
    # Sample input data
    data = pd.DataFrame([
        {"title": "Meta role",
         "link": "https://www.metacareers.com/jobs/123"},
        {"title": "Google role",
         "link": "https://www.google.com/about/careers/applications/jobs/456"},
    ])

    company_dict = {
        "Meta": "https://www.metacareers.com/jobs",
        "Google": "https://www.google.com/about/careers/applications/jobs",
    }

    # Decide which checkboxes are "checked"
    checkbox_responses = {
        "Meta": True,
        "Google": False,
    }

    def fake_checkbox(label, value=True, key=None):
        return checkbox_responses[label]

    monkeypatch.setattr(hw1.st, "checkbox", fake_checkbox)

    filtered_df = hw1.filter_by_company(data, company_dict)

    assert len(filtered_df) == 1
    assert "metacareers" in filtered_df.iloc[0]["link"]


def test_dataframe_renders_when_no_companies_selected(monkeypatch):
    # Patch requests.get so the app loads some data
    sample_data = [
        {"title": "Meta role",
         "link": "https://www.metacareers.com/jobs/123",
         "date": "2025-08-15"},
        {"title": "Google role",
         "link": "https://www.google.com/about/careers/applications/jobs/456",
         "date": "2025-08-13"},
    ]
    monkeypatch.setattr(hw1,
                        "retrieve_data_from_urls",
                        lambda urls: sample_data)

    # Force all checkboxes unchecked
    monkeypatch.setattr(hw1.st, "checkbox", lambda *a, **k: False)

    at = AppTest.from_file("main.py").run()

    assert len(at.dataframe) == 1
    df = at.dataframe[0].value
    assert df.empty


def test_streamlit_layout(pickle_data, monkeypatch):
    """Test the Streamlit app layout."""
    def mock_get(url):
        class MockResponse:
            def __init__(self, content):
                self.content = content
        return MockResponse(pickle_data.getvalue())

    monkeypatch.setattr("requests.get", mock_get)

    link_column_used = {}
    original_LinkColumn = hw1.st.column_config.LinkColumn
    def mock_LinkColumn(*args, **kwargs):
        link_column_used["used"] = True
        return original_LinkColumn(*args, **kwargs)

    monkeypatch.setattr(hw1.st.column_config, "LinkColumn", mock_LinkColumn)

    # set checkboxes to simulate user selecting only "Meta"
    monkeypatch.setattr(hw1.st,
                        "checkbox",
                        lambda label,
                        **kwargs: label == "Meta")

    at = AppTest.from_file("main.py").run()

    # Title
    assert at.title[0].value == "Data Scientist Job Listings"

    # Sidebar
    sidebar_texts = [w.value for w in at.sidebar.markdown]
    assert "Filter by Company" in sidebar_texts

    # DataFrame
    assert len(at.dataframe) > 0
    df = at.dataframe[0].value
    assert isinstance(df, pd.DataFrame)
    assert {"date", "title", "link"} == set(df.columns)
    assert all("metacareers.com" in link for link in df["link"])
    for link in df["link"]:
        parsed = urlparse(link)
        assert parsed.scheme in ("http", "https")
        assert parsed.netloc

    # Confirm that LinkColumn was used
    assert link_column_used.get("used") is True