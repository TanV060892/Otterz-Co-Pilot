from fastapi import Request,Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from utils import common,auth,aws,db
from models import VUser


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl="authorize"
)

async def get_request_details(request: Request):
    request_data = {
            "url": str(request.url),
            "main_path": str(request.url.path),
            "method": request.method,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "body": {},
    }    
    try:
        body_bytes = await request.body()
        if body_bytes:
            request_data['body'] = common.convert_to_dict(body_bytes)
    except Exception as e:            
            request_data['body'] = {'errro':str(e)}
    return {"status":True,"request":request_data}
    

async def get_token_details(request: Request,token: str = Depends(oauth2_scheme)):
    request_data = {
            "url": str(request.url),
            "main_path": str(request.url.path),
            "method": request.method,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "body": {},
    }    
    try:
        body_bytes = await request.body()
        if body_bytes:
            request_data['body'] = common.convert_to_dict(body_bytes)
    except Exception as e:            
            request_data['body'] = {'errro':str(e)}
    token_details =  auth.verify_token_activation(token)
    if 'otterz_id' in token_details :
       return {"status":True,"access_token": token,"request":request_data,"user":get_user_details(token_details['otterz_id'])}
    elif 'error' in token_details and token_details['error'] == 'token_expired':
       return {"status":False,"error_code": 'OTZT401',"error_message":"***************** Token Expired Error *****************************\nRequest Details:"+str(request_data)}
    else :
       return {"status":False,"error_code": 'OTZT422',"error_message":"***************** Other Exceptional Error *****************************\nRequest Details:"+str(request_data)}
    

def get_user_details(otterz_id : str):
    result = {}
    secret_details = aws.get_secret_details()
    cursor = db.get_db_connection(secret_details['mongo_database'],'users').find_one({"otterz_id": otterz_id})
    if cursor:  
        return VUser(
            otterz_id=cursor.get('otterz_id', ''),
            first_name=cursor.get('first_name', ''),
            last_name=cursor.get('last_name', ''),
            email_id=cursor.get('email_id', ''),
            phone_no=cursor.get('phone_no', ''),
            uuid=cursor.get('uuid', ''),
            country=cursor.get('country', ''),
            created_on=cursor.get('created_on', ''), 
            last_updated_on=cursor.get('last_updated_on', ''), 
            is_owner=cursor.get('is_owner', 'N'),
            verifications={'email':cursor['verifications']['email'],'phone':cursor['verifications']['phone']},
            services={'bookeeping_insights':cursor['services']['bookeeping_insights'],'accept_payments':cursor['services']['accept_payments']}
        ).dict()
    return result