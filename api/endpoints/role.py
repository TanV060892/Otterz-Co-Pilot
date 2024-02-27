from fastapi import APIRouter,Depends
from utils import token,common,db


#api call starts from here
router = APIRouter()

'''
 * Get system provided permissions details against role  
 * @route GET /api/role/permissions/business_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 503 - Invalid Grant Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/role/permissions/{business_id}")
def get_role_details(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            if token_details['user']['is_owner'] == 'Y' :
                return common.process_success_response(db.get_details_with_filter('permissions',{'business_id':int(business_id)}))
            else :
                return common.process_error_response('OTZ503',"***************** Permission Denied *****************************\nRequest Details:"+ str(token_details))             
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   


'''
 * Lik permissions against role for busiiness id
 * @route POST /api/role/permissions/business_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 503 - Invalid Grant Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/role/permissions/{business_id}")
def link_permissions_against_role(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            required_field_chk = common.check_required_fields_and_types({"permissions": list,"role":str},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk 
            if token_details['user']['is_owner'] == 'Y' :
                db.update_record('permissions',{"business_id":int(business_id),"role":common.to_first_upper_case(token_details['request']['body']['role'])},token_details['request']['body'])
                return common.process_success_response(db.get_details_with_filter('permissions',{'business_id':int(business_id),'role':common.to_first_upper_case(token_details['request']['body']['role'])}))
            else :
                return common.process_error_response('OTZ503',"***************** Permission Denied *****************************\nRequest Details:"+ str(token_details))             
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   