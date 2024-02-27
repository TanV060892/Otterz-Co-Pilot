from fastapi import APIRouter,Depends
from utils import token,common,db,aws


#api call starts from here
router = APIRouter()

'''
 * Add business for otterz
 * @route POST /api/business
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/business")
def add_business_details(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :       
            required_field_chk = common.check_required_fields_and_types({"name": list},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk            
            if token_details['user']['is_owner'] == 'Y' :
                added_details = []
                for i in token_details['request']['body']['name'] :
                    #insert business details
                    business_details = {}
                    business_id = db.get_next_sequence_value("id")
                    business_details = {
                        "id": business_id,
                        "name": common.to_camel_case(i),
                        "owner" : {"otterz_id":token_details['user']['otterz_id'],"name":token_details['user']['first_name']+' '+token_details['user']['last_name'],"email":token_details['user']['email_id'],"role":"Admin","added_on":common.get_current_unix_timestamp()},
                        "created_by": token_details['user']['otterz_id'],
                        "created_on": common.get_current_unix_timestamp(),
                        "last_updated_on": common.get_current_unix_timestamp()
                    }                    
                    db.insert_record('businesses',business_details)
                    added_details.append(business_details)
                    #insert role and permissions
                    secret_details = aws.get_secret_details()
                    for i in secret_details['roles'] :
                        role_permission_details = {}
                        role_permission_details = {
                            "business_id":business_id,
                            "role":i,
                            "permissions": secret_details['permissions'][i]
                        }
                        db.insert_record('permissions',role_permission_details)
                return common.process_success_response(added_details)    
            else :
                return common.process_error_response('OTZ503',"***************** Permission Denied *****************************\nRequest Details:"+ str(token_details))             
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])       



'''
 * View all businesses for otterz
 * @route GET /api/business
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/business")
def get_business_details(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            return common.process_success_response(db.get_details_with_filter('businesses',{'owner.otterz_id':token_details['user']['otterz_id']}))             
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * View all businesses for otterz
 * @route GET /api/business/business_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/business/{business_id}")
def get_business_detail_from_id(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            return common.process_success_response(db.get_details_with_filter('businesses',{'id':int(business_id)}))             
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * View all users against business
 * @route GET /api/business/business_id/users
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/business/{business_id}/users")
def get_business_detail_from_id(business_id : str,token_details: dict = Depends(token.get_token_details)):
    response_details = []
    try :
        if(token_details['status']) :
            db_details = db.get_details_with_filter('businesses',{'id':int(business_id)})
            response_details.append(db_details[0]['owner'])
            if 'employees' in db_details[0] :
                for i in db_details[0]['employees'] :
                    response_details.append(i)
            return common.process_success_response(response_details)            
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * Link account with business
 * @route POST /api/business/business_id/accounts
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/business/accounts/link")
def link_account_with_business(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            required_field_chk = common.check_required_fields_and_types({"data": list},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk   
            for i in token_details['request']['body']['data'] :
                required_field_chk = common.check_required_fields_and_types({"business_id": str,"account_id":str},i) 
                if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                    return required_field_chk 
                existed_account_details = db.get_details_with_filter('accounts',{'business_id':i['business_id'],'account_id':i['account_id']})
                if len(existed_account_details) == 0 :
                    existed_account_details = {}
                    existed_account_details = {
                        "business_id":i['business_id'],
                        "account_id":i['account_id']
                    } 
                    db.insert_record('accounts',existed_account_details)
                else :
                    return common.process_error_response("OTZ409","")  
            return common.process_success_response({'message':'Accounts linked successfully'})
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * View all accounts linked against business
 * @route GET /api/business/business_id/accounts
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/business/{business_id}/accounts")
def get_business_detail_from_id(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            return common.process_success_response(db.get_details_with_filter('accounts',{'business_id':business_id}))            
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * Link user with business
 * @route PUT /api/business/business_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.put("/business/{business_id}")
def get_business_detail_from_id(otterz_id : str,business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            db_details = db.get_details_with_filter('users',{'otterz_id':otterz_id})
            return db_details          
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 

