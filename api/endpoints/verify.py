from fastapi import APIRouter,Depends
from utils import auth,token,common,db

#api call starts from here
router = APIRouter()

'''
 * Send Email for verification from token 
 * @route POST /verify/email
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
'''
@router.get("/verify/email")
def send_email_verification_link(token_details: dict = Depends(token.get_token_details)):
   if token_details['status'] :
      auth.send_verification_email(token_details['access_token'])
      return common.process_success_response({'message':"Mail sent successfully."})
   return common.process_error_response(token_details['error_code'],token_details['error_message']) 
    
   
'''
 * Send Reset Password for verification from email 
 * @route GET /verify/password
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
'''
@router.get("/verify/password")
def send_reset_password_link(email_id:str,token_details: dict = Depends(token.get_request_details)):
   if token_details['status'] :
      auth.send_reset_password_email(email_id)
      return common.process_success_response({'message':"Mail sent successfully."})
   return common.process_error_response(token_details['error_code'],token_details['error_message'])   
    
    
'''
 * Get verified user details from firebase
 * @route GET /api/verify/user
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/verify/user")
def get_verified_user_details(email_id:str,token_details: dict = Depends(token.get_request_details)):
   if token_details['status'] :
      auth.verify_user_details(email_id)
      return common.process_success_response(db.get_details_with_filter('users',{'email_id':email_id}))
   return common.process_error_response(token_details['error_code'],token_details['error_message'])   