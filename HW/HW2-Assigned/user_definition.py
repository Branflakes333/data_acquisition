import os

from dotenv import load_dotenv

# Load environment variables from .env file
# TODO : Make sure to you have .env with the provided env names
load_dotenv(override=True)
project_id = os.getenv('PROJECT_ID')
bucket_name = os.getenv('GCP_BUCKET_NAME')
service_account_file_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
api_key = os.getenv('API_KEY')  # THIS IS FOR GCP CUSTOM SEARCH.
search_engine_id = os.getenv('SEARCH_ENGINE_ID')
api_server_url = os.getenv('API_SERVICE_URL')

file_name_prefix = 'jobs_search'
google_api_url = 'https://www.googleapis.com/customsearch/v1'
no_days_to_search = 60
role_name = 'Data Scientist'
company_dictionary = {"Meta": "https://www.metacareers.com/jobs",
                      "Microsoft": "https://careers.microsoft.com/",
                      "Google": "https://www.google.com/about/"
                      "careers/applications/jobs"}
