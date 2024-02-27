from fastapi import APIRouter,Depends
from utils import token,common,db,aws

#api call starts from here
router = APIRouter()

'''
 * Send Reset Password for verification from email 
 * @route POST /invite/owner
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.post("/invite/owner")
def send_invite_to_owner(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :       
            required_field_chk = common.check_required_fields_and_types({"email_id": str},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk            
            return common.process_success_response({'message':"Mail Sent Successfully"})    
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message']) 


'''
 * Send Invitation to user against business 
 * @route POST /invite/business_id/user
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.post("/invite/{business_id}/user")
def send_invite_to_user(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :       
            required_field_chk = common.check_required_fields_and_types({"email_id": str,"name":str,"role":str},token_details['request']['body']) 
            if isinstance(required_field_chk, dict) and 'status' in required_field_chk:
                return required_field_chk
            
            invitation_details = {}
                
            if len(db.get_details_with_filter('invitation',{'email_id':token_details['request']['body']['email_id']})) == 0 :
                #add invitation details
                invitation_details = {
                    "id": db.get_next_sequence_value("id"),
                    "business_id":business_id,
                    "name": common.to_camel_case(token_details['request']['body']['name']),
                    "email_id":token_details['request']['body']['email_id'],
                    "role": token_details['request']['body']['role'],
                    "reason":"add_user_against_business",
                    "status":"Pending",
                    "added_on": common.get_current_unix_timestamp(),
                    "last_updated_on":common.get_current_unix_timestamp()
                }                    
                db.insert_record('invitation',invitation_details)
            else :
                invitation_details = {
                    "status":"Pending",
                    "last_updated_on":common.get_current_unix_timestamp()
                }          
                db.update_record('invitation',{"email_id":token_details['request']['body']['email_id']},invitation_details)       
            if len(db.get_details_with_filter('authentications',{'user.email_id':token_details['request']['body']['email_id']})) > 0 :
                aws.send_email('tanvi.shah@otterz.co',token_details['request']['body']['email_id'],'Link User With Business','This is a test email sent using AWS SES.','')
                return common.process_success_response({'message':"Link Business Mail sent"})    
            else :
                aws.send_email('tanvi.shah@otterz.co',token_details['request']['body']['email_id'],'Signup User With Business','This is a test email sent using AWS SES.','')
                return common.process_success_response({'message':"Signup Mail sent"})                
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  


'''
 * Resend invitation
 * @route PUT /invite/invite_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.put("/invite/{invite_id}")
def resend_invite_from_id(invite_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) : 
            invitation_details = {}  
            invitation_details = {
                "status":"Pending",
                "last_updated_on":common.get_current_unix_timestamp()
            }          
            db.update_record('invitation',{"id":int(invite_id)},invitation_details)
            invitation_details = db.get_details_with_filter('invitation',{"id":int(invite_id)})  
            if len(invitation_details) > 0 :
                if len(db.get_details_with_filter('authentications',{'user.email_id':invitation_details[0]['email_id']})) > 0 :
                    aws.send_email('tanvi.shah@otterz.co',invitation_details[0]['email_id'],'Link User With Business','This is a test email sent using AWS SES.','')
                    return common.process_success_response({'message':"Link Business Mail sent"})    
                else :
                    aws.send_email('tanvi.shah@otterz.co',invitation_details[0]['email_id'],'Signup User With Business','This is a test email sent using AWS SES.','')
                    return common.process_success_response({'message':"Signup Mail sent"})  
            return common.process_error_response('OTZ4000',"***************** Invalid Invite ID *****************************\nRequest Details:"+ str(token_details))               
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  



'''
 * View all sent invitation against business
 * @route GET /invite/business_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.get("/invite/{business_id}")
def get_all_invites_against_business(business_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :       
            return common.process_success_response(db.get_details_with_filter('invitation',{'business_id':business_id}))                   
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  
   

'''
 * Delete invitation
 * @route DELETE /invite/invite_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 401 - Token Expired
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Unexpected Errors
'''
@router.delete("/invite/{invite_id}")
def delete_invite_from_id(invite_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) : 
            db.delete_record('invitation',{'id':int(invite_id)})      
            return common.process_success_response({'message':'Invite deleted successfully'})                   
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])  
   
    