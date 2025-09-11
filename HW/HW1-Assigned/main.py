import streamlit as st 

job_posting_page = st.Page("hw1.py", title="Career Preparation", icon=":material/table:")

pg = st.navigation([job_posting_page])
st.set_page_config(page_title="Job Listing Dashboard", page_icon=":material/interactive_space:")
pg.run()
