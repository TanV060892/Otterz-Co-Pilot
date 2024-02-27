from fastapi import APIRouter,Depends
from utils import token,common,aws,db

import requests

#api call starts from here
router = APIRouter()

'''
 * Get registered user details 
 * @route GET /api/plaid/token/link/otterz_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/plaid/token/link/{otterz_id}")
async def get_link_token(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            required_field_chk = common.check_required_fields_and_types({"client_name": str,"platform":str},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk  
            secret_details = aws.get_secret_details()            
            payload = {
                "client_id": secret_details['plaid']['client_id'],
                "secret": secret_details['plaid']['secret'],
                "client_name": token_details['request']['body']['client_name'],
                "language":"en",
                "country_codes":["US"],
                "user":{
                    "client_user_id":otterz_id
                },
                "products":["assets","transactions"]
            }
            if token_details['request']['body']['platform'].lower() == 'android' :
                payload['android_package_name'] = "co.otterz.app.dev"
            
            response = requests.post(secret_details['plaid']['link_token_url'], json=payload)
            if response.status_code == 200:
                return common.process_success_response(response.json())    
            else :
                return common.process_error_response(response.status_code,"**************** Plaid Error Occured ******************"+str(response)+"\nRequest Details:"+ str(token_details))            
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 
    


'''
 * PUT Update Public Token Details 
 * @route PUT /api/plaid/token/public
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.put("/plaid/token/public/{otterz_id}")
async def get_public_token(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            required_field_chk = common.check_required_fields_and_types({"public_token": str},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk 
            secret_details = aws.get_secret_details()  
            payload = {
                "client_id": secret_details['plaid']['client_id'],
                "secret": secret_details['plaid']['secret'],
                "public_token":token_details['request']['body']['public_token']
            }
            response = requests.post(secret_details['plaid']['access_token_url'], json=payload)
            if response.status_code == 200:
                data = response.json()
                token_details = {}
                token_details = {
                    "plaid":{
                        "access_token":data['access_token'],
                        "last_updated_on":common.get_current_unix_timestamp()
                    }
                }
                db.update_record('authentications',{"otterz_id":otterz_id},token_details)
                return common.process_success_response({"message":"Details Updated Successfully."})    
            else :
                return common.process_error_response(response.status_code,"**************** Plaid Error Occured ******************"+str(response)+"\nRequest Details:"+ str(token_details))     
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 
    

'''
 * Get plaid account details 
 * @route GET /api/plaid/accounts
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/plaid/accounts/{otterz_id}")
async def get_plaid_accounts(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            plaid_token = db.get_details_with_filter('authentications',{'otterz_id':otterz_id})
            if len(plaid_token) > 0 and 'plaid' in plaid_token[0]:
                secret_details = aws.get_secret_details()
                payload = {
                    "client_id": secret_details['plaid']['client_id'],
                    "secret": secret_details['plaid']['secret'],
                    "access_token": plaid_token[0]['plaid']['access_token']
                }
                response = requests.post(secret_details['plaid']['get_accounts_url'], json=payload)
                if response.status_code == 200:
                    return common.process_success_response(response.json())    
                else :
                    return common.process_error_response(response.status_code,"**************** Plaid Error Occured ******************"+str(response)+"\nRequest Details:"+ str(token_details)) 
            else :
                return common.process_error_response('OTZ4000',"")           
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 

