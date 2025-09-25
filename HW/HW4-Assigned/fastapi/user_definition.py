import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../../../.env")

project_id = os.getenv('PROJECT_ID')
bucket_name = os.getenv('GCP_BUCKET_NAME')
service_account_file_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
api_key = os.getenv('API_KEY')
gemini_key = os.getenv("GEMINI_API_KEY")

search_engine_id = os.getenv('SEARCH_ENGINE_ID')
api_server_url = os.getenv('API_SERVICE_URL')
file_name_prefix = 'jobs_search_hw4'
google_api_url = 'https://www.googleapis.com/customsearch/v1'
