from fastapi import APIRouter,Depends
from utils import token,common,db

#api call starts from here
router = APIRouter()

'''
 * Update onboarding status for user
 * @route PUT /api/onboarding/otterz_id
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.put("/onboarding/{otterz_id}")
def add_onboarding_details(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    if(token_details['status']) :
        db.update_record('onboarding_details',{"otterz_id":otterz_id},token_details['request']['body'])
        return common.process_success_response(db.get_details_with_filter('onboarding_details',{'otterz_id':otterz_id}))
    return common.process_error_response(token_details['error_code'],token_details['error_message'])     


'''
 * Get onboarding status of user
 * @route GET /api/onboarding/otterz_id
 * @group Auth APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 400 - Bad Request/Specific Errors
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/onboarding/{otterz_id}")
def get_onboarding_detail(otterz_id : str,token_details: dict = Depends(token.get_token_details)):
    if(token_details['status']) :
        return common.process_success_response(db.get_details_with_filter('onboarding_details',{'otterz_id':otterz_id}))
    return common.process_error_response(token_details['error_code'],token_details['error_message'])   
