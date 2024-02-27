import firebase_admin
import pyrebase
import json
import requests

#from bson import json_util
from firebase_admin import credentials, auth
from utils import common, db, aws


def get_firebase_auth_id(email_id: str, password: str):
    secret_details = aws.get_secret_details()
    cred = credentials.Certificate(secret_details['firebase_details']['file_details'])
    # Check if the app is already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    try:
        auth_user = auth.create_user(email=email_id, password=password)
        if auth_user.uid is not None:
            pb = pyrebase.initialize_app(secret_details['firebase_details']['config_details'])
            user = pb.auth().sign_in_with_email_and_password(email_id, password)
            send_verification_email(user['idToken'])
            authentication_details = {
                "otterz_id": auth_user.uid,
                "user": {
                    "email_id": auth_user.email,
                    "email_verification": auth_user.email_verified,
                    "registration_status": user['registered']
                },
                "access_token": user['idToken'],
                "refresh_token": user['refreshToken'],
                "created_on": common.get_current_unix_timestamp(),
                "last_updated_on": common.get_current_unix_timestamp()
            }
            db.insert_record('authentications',authentication_details)
            user_details = {
                "otterz_id": auth_user.uid,
                "email_id": auth_user.email,
                "created_on": common.get_current_unix_timestamp(),
                "last_updated_on": common.get_current_unix_timestamp(),
                "verifications": {
                    "email": "N",
                    "phone": "N"
                },
                "services": {
                    "bookeeping_insights": "N",
                    "accept_payments": "N"
                }
            }
            db.insert_record('users',user_details)
            onboarding_details = {
                "otterz_id": auth_user.uid,
                "email_id": auth_user.email,
                "status":"Registered"
            }
            db.insert_record('onboarding_details',onboarding_details)
            return common.process_success_response(authentication_details)
        else:
            return common.process_error_response('OTZ422',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+"Unable To Get UID from Firebase while creating user")
    except auth.EmailAlreadyExistsError:
        return common.process_error_response('OTZ4003',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+"Unable To Get UID from Firebase while creating user")
    except Exception as e:
        if "malformed email address" in str(e).lower():
            return common.process_error_response('OTZ4001',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+"Invalid email pattern")
        elif "invalid_email" in str(e).lower():
            return common.process_error_response('OTZ4001',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+"Email doesnot exists")
        elif "invalid password" in str(e).lower():
            return common.process_error_response('OTZ4002',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+"Invalid password pattern")
        else:
            return common.process_error_response('OTZ500',"***************** Token API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+str(e))
       

def get_token_for_registered_user(email_id: str, password: str):
    authentication_details = user_details = {}
    try :
        secret_details = aws.get_secret_details()
        cursor = db.get_db_connection(secret_details['mongo_database'],'authentications').find_one({"user.email_id": email_id})
        if cursor and 'user' in cursor and cursor['user']['email_id'] == email_id :
            cred = credentials.Certificate(secret_details['firebase_details']['file_details'])
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            pb = pyrebase.initialize_app(secret_details['firebase_details']['config_details'])
            user = pb.auth().sign_in_with_email_and_password(email_id, password)
            user_details = auth.get_user_by_email(email_id, app=None)
            if 'idToken' in user :
                authentication_details = {
                    "otterz_id": cursor['otterz_id'],
                    "user": {
                        "email_id": email_id,
                        "email_verification": user_details.email_verified,
                        "registration_status": cursor['user']['registration_status']
                    },
                    "access_token": user['idToken'],
                    "refresh_token": user['refreshToken'],
                    "created_on": common.get_current_unix_timestamp(),
                    "last_updated_on": common.get_current_unix_timestamp()
                }
                db.update_record('authentications',{"user.email_id": email_id},authentication_details)
                user_details = {
                    "last_updated_on": common.get_current_unix_timestamp(),
                    "verifications": {
                        "email": 'Y' if user_details.email_verified else 'N',
                        "phone": "N"
                    }
                }
                db.update_record('users',{"otterz_id": cursor['otterz_id']},user_details)
                return common.process_success_response(authentication_details) 
    except Exception as e:
        if "invalid_login_credentials" in str(e).lower():
            return common.process_error_response('OTZ4000',"***************** Login API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : Invalid credentials")
        else :
            return common.process_error_response('OTZ500',"***************** Login API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : "+str(e) )
    return common.process_error_response('OTZ4000',"***************** Login API Error *****************************\nRequest Details:\nEmail : "+email_id+"\nPassword :"+password+"\nError : Unable to get details error")


def send_verification_email(token: str):
    secret_details = aws.get_secret_details()
    headers = {'Content-Type': 'application/json',}
    data='{"requestType":"VERIFY_EMAIL","idToken":"'+token+'"}'
    requests.post(secret_details['firebase_details']['email_verification_link'].format(secret_details['firebase_details']['config_details']['apiKey']), headers=headers, data=data)


def send_reset_password_email(email_id: str):
    secret_details = aws.get_secret_details()
    headers = {'Content-Type': 'application/json',}
    data='{"requestType":"PASSWORD_RESET","email":"'+email_id+'"}'
    requests.post(secret_details['firebase_details']['email_verification_link'].format(secret_details['firebase_details']['config_details']['apiKey']), headers=headers, data=data)
            

def verify_token_activation(token : str):
    try:
        secret_details = aws.get_secret_details()  
        cred = credentials.Certificate(secret_details['firebase_details']['file_details'])
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        user = auth.verify_id_token(token, app=None)
        if 'uid' in user :
            return {'otterz_id':user['uid'],'email_id':user['email']}
    except auth.ExpiredIdTokenError:
        return {'error':'token_expired'}
    except Exception as e:
        if "firebase ID token has incorrect" in str(e).lower():
            return {'error':str(e)}
        else :
            return {'error':str(e)}


def verify_user_details(email_id : str):
    secret_details = aws.get_secret_details()
    cred = credentials.Certificate(secret_details['firebase_details']['file_details'])
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    pb = pyrebase.initialize_app(secret_details['firebase_details']['config_details'])
    user_details = auth.get_user_by_email(email_id, app=None)
    user_details = {
        "verifications": {
            "email": 'Y' if user_details.email_verified else 'N',
            "phone": "N"
        }
    }
    db.update_record('users',{"email_id": email_id},user_details)