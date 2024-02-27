import os
import bugsnag
from utils.aws import get_secret_details

def log_error_details(error_message : str):
    secret_details = get_secret_details()
    bugsnag.configure(
        api_key=secret_details['bugsnag_logging']['key'], project_root=secret_details['bugsnag_logging']['app_path'],
        release_stage=os.environ["ENVIRONMENT"],
    )
    bugsnag.notify(Exception(error_message))