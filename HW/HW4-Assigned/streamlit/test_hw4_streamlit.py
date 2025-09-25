import re
import pytest
from playwright.sync_api import Page, expect

# Adjust this to wherever your Streamlit app runs
APP_URL = "http://localhost"


@pytest.mark.parametrize("url", [APP_URL])
def test_skills_column(page: Page, url: str):
    page.goto(url)

    page.wait_for_selector("canvas")

    table = page.locator('table')
    expect(table).to_contain_text("skills")

    # Get all header cells
    headers = table.locator("thead tr th").all_inner_texts()
    assert "skills" in [h.lower().strip()
                        for h in headers], "skills column not found in table"
    # page.get_by_role("columnheader", name="skills", exact=True).click()
    # Find index of skills column
    skills_idx = [i for i, h in enumerate(
        headers) if h.lower().strip() == "skills"][0]
    assert skills_idx == 2

    rows = table.locator("tbody tr")
    for i in range(rows.count()):
        cell_text = rows.nth(i).locator("td").nth(
            skills_idx).inner_text().strip()
        if (len(cell_text) > 0):
            # Assert comma-separated strings (at least one comma or single value)
            # .+? : at least one of any character
            assert re.match(r"^.+?(,\s*.+?)*$", cell_text), \
                f"Row {i} has invalid skills format: '{cell_text}'"
