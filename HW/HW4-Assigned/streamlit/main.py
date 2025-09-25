import streamlit as st

job_posting_page = st.Page(
    "hw4.py", title="Table View", icon=":material/table:")

pg = st.navigation([job_posting_page])
st.set_page_config(page_title="Career Dashboard",
                   page_icon=":material/interactive_space:")
pg.run()
