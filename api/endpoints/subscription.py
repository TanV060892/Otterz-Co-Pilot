from fastapi import APIRouter,Depends
from utils import token,common,aws,db


#api call starts from here
router = APIRouter()

'''
 * Get subscriptions details
 * @route GET /api/subscription
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/subscription")
def get_subscription_details(token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
           secret_details = aws.get_secret_details()
           return common.process_success_response(secret_details['subscriptions'])
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   



'''
 * Get subscribed plan details
 * @route GET /api/subscription/otterz_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/subscription/{otterz_id}")
def get_subscription_details(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
           return common.process_success_response(db.get_details_with_filter('subscriptions',{'otterz_id':otterz_id}))
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   


'''
 * Upsert Subscription
 * @route PUT /api/subscription/otterz_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 500 - Internal server error
'''
@router.put("/subscription/{otterz_id}")
def update_subscription_details(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    try :
        if(token_details['status']) :
           return common.process_success_response(db.get_details_with_filter('subscriptions',{'otterz_id':otterz_id}))
    except Exception as e :
        return common.process_error_response(str(e),"***************** Exception Occured *****************************\nError Details : "+str(e) +"\nRequest Details:"+ str(token_details)) 
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   

