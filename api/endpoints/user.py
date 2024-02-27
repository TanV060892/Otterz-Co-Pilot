from models import AUser
from fastapi import APIRouter,Depends
from utils import token,common,db


#api call starts from here
router = APIRouter()

'''
 * Add user for otterz
 * @route PUT /api/user
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.put("/user/{otterz_id}")
def add_user_details(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    if(token_details['status']) :
        user_details = token.get_user_details(otterz_id)
        stored_details = AUser(**user_details).dict()
        input_details = AUser(**token_details['request']['body']).dict()
        merged_details = {key: input_details[key] if input_details[key] != '' else stored_details[key] for key in stored_details}
        db.update_record('users',{"otterz_id":otterz_id},merged_details)
        return common.process_success_response(token.get_user_details(otterz_id))
    return common.process_error_response(token_details['error_code'],token_details['error_message'])       


'''
 * Get registered user details 
 * @route GET /api/user
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/user")
def get_user_details(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
            return common.process_success_response(db.get_all_details('users'))               
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   


'''
 * Get registered user details of provided user_id 
 * @route GET /api/user/user_id
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/user/{otterz_id}")
def get_user_detail(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    if(token_details['status']) :
        return common.process_success_response(db.get_details_with_filter('users',{'otterz_id':otterz_id}))
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  



'''
 * Delete User
 * @route DELETE /user/{otterz_id}
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.delete("/user/{otterz_id}")
def delete_invite_from_id(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) : 
            db.delete_record('users',{'otterz_id':otterz_id})      
            return common.process_success_response({'message':'User deleted successfully'})                   
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  
   
    


