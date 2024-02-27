import boto3
import os
import json

from botocore.exceptions import NoCredentialsError

# Module-level variable to store the cached secret details
_cached_secret_details = None

def get_secret_details():        
    global _cached_secret_details
    if _cached_secret_details is not None:
        return _cached_secret_details
    try:
        client = boto3.client("secretsmanager", region_name="us-east-1",aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
        response = client.list_secrets()
        response = client.get_secret_value(SecretId=os.environ.get("ENVIRONMENT"))
        secret_details = json.loads(response['SecretString'])
        # Cache the secret details
        _cached_secret_details = secret_details
        return secret_details
    except NoCredentialsError:
        return {"error":"AWS credentials not available."}
    except Exception as e:
        return {"error":str(e)}
    

def send_email(sender, recipient, subject, body_text, body_html):
    ses_client = boto3.client("ses", region_name="us-east-1",aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
    message = {
        'Subject': {'Data': subject},
        'Body': {
            'Text': {'Data': body_text},
            'Html': {'Data': body_html}
        }
    }
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message=message
        )
        return {"message_id":response['MessageId'],"message":"Mail Sent Successfully"}    
    except Exception as e:
        return {"error":str(e)}
    