import pytz
import re
import json

from datetime import datetime,timedelta
from fastapi.responses import JSONResponse
from utils import errors,logger

def check_required_fields_and_types(field_types, body):
    type_errors = []
    for field, expected_type in field_types.items():
        if field not in body:
            type_errors.append({"message": field + " is required", "code": "OTZ422"})
        elif not isinstance(body[field], expected_type):
            type_errors.append({"message": field + " should be of type " + str(expected_type), "code": "OTZ422"})    
    if type_errors:
        return {"status": False, "errors": type_errors}
    else:
        return True


def process_success_response(response_to_send : dict):
    return JSONResponse(status_code=200, content={"status": True, "data": response_to_send})

def process_error_response(error_code : str,error_message : str):
    if error_message != '' :
        logger.log_error_details(error_message) 
    return errors.process_error_response(error_code)

def to_camel_case(input_string: str):
    words = input_string.replace("_", " ").replace("-", " ").split()
    return ' '.join(word.title() for word in words)

def to_first_upper_case(input_string: str):
    return input_string.capitalize()

def convert_to_dict(json_str: str):
    data_dict = json.loads(json_str)
    return data_dict


def convert_to_dict_from_list(ip_list_value: list):
    json_data = json.dumps(ip_list_value)
    return json_data


def read_content_from_file(file_path):
    with open(file_path, "r") as file_details:
       return file_details.read()


def get_current_time():
    tz = pytz.utc
    current_time = datetime.now(tz)
    return current_time.strftime("%d-%m-%Y %H:%M:%S")

def get_current_unix_timestamp():
    tz = pytz.utc
    current_time = datetime.now(tz)
    return int(current_time.timestamp())

def get_current_date():
    tz = pytz.utc
    current_time = datetime.now(tz)
    return current_time.strftime("%d-%m-%Y")

def get_date_from_specific_day_of_today(days : int)-> str:
    tz = pytz.utc
    current_time = datetime.now(tz)
    target_date = current_time - timedelta(days=days)
    formatted_date = target_date.strftime("%d-%m-%Y")
    return formatted_date

def remove_all_special_characters(ip_string: str) -> str:
    string = ip_string.replace(' ', '-')
    return re.sub(r'[^A-Za-z0-9]', '', string)