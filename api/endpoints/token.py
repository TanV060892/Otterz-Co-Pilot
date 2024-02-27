from fastapi import APIRouter,Depends
from utils import auth,common,token

#api call starts from here
router = APIRouter()

'''
 * Get Firebase authentication and generate JWT Token 
 * @route POST /api/token/register
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/token/register")
def generate_token(token_details: dict = Depends(token.get_request_details)):
    required_field_chk = common.check_required_fields_and_types({"email_id": str, "password": str},token_details['request']['body']) 
    if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
        return required_field_chk
    return auth.get_firebase_auth_id(token_details['request']['body']['email_id'],token_details['request']['body']['password'])



'''
 * Get Firebase authentication and generate JWT Token 
 * @route POST /api/token/login
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.post("/token/login")
def get_token(token_details: dict = Depends(token.get_request_details)):
    required_field_chk = common.check_required_fields_and_types({"email_id": str, "password": str},token_details['request']['body']) 
    if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
        return required_field_chk
    return auth.get_token_for_registered_user(token_details['request']['body']['email_id'],token_details['request']['body']['password'])



