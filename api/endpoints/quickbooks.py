from fastapi import APIRouter,Request,Depends
from fastapi.responses import  RedirectResponse
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from utils import aws,db,common,token


#api call starts from here
router = APIRouter()

@router.get("/quickbooks/authorization")
def get_quickbooks_token(request: Request):
    code = request.query_params.get("code")
    realm_id = request.query_params.get("realmId")
    state = request.query_params.get("state")
    if code and realm_id and state:
        secret_details = aws.get_secret_details()
        auth_client = AuthClient(
            client_id=secret_details['quickbooks']['id'],
            client_secret=secret_details['quickbooks']['secret'],
            environment=secret_details['quickbooks']['environment'],
            redirect_uri="http://ec2-18-233-152-212.compute-1.amazonaws.com:8000/api/quickbooks/authorization",
        )
        auth_client.get_bearer_token(code)
        token_details = {}
        token_details = {
            "quickbooks":{
                "access_token":auth_client.access_token,
                "refresh_token":auth_client.refresh_token,
                "code":request.query_params.get("code"),
                "realmid":request.query_params.get("realmId"),
                "last_updated_on":common.get_current_unix_timestamp()
            }
        }
        db.update_record('authentications',{"otterz_id":request.query_params.get("state")},token_details)


'''
 * Get quickbooks token details 
 * @route GET /api/quickbooks/token/user_id
 * @group Onboarding APIs
 * @returns JSON Object 200 - Ok
 * @returns JSON Object 422 - Unprocessable Entity
 * @returns JSON Object 500 - Internal server error
'''
@router.get("/quickbooks/token/{otterz_id}")
async def get_quickbooks_authorization_url(otterz_id: str, token_details: dict = Depends(token.get_token_details)):
    try:
        if token_details['status']:
            quickboks_details = db.get_details_with_filter('authentications', {'otterz_id': otterz_id})
            if len(quickboks_details) > 0 and 'quickbooks' in quickboks_details[0]:
                return common.process_success_response(quickboks_details[0]['quickbooks'])
            else:
                secret_details = aws.get_secret_details()
                auth_client = AuthClient(
                    client_id=secret_details['quickbooks']['id'],
                    client_secret=secret_details['quickbooks']['secret'],
                    environment=secret_details['quickbooks']['environment'],
                    redirect_uri="http://ec2-18-233-152-212.compute-1.amazonaws.com:8000/api/quickbooks/authorization",
                )
                scopes = [Scopes.ACCOUNTING, Scopes.OPENID]
                auth_url = auth_client.get_authorization_url(scopes, otterz_id)
                return RedirectResponse(auth_url,status_code=307)
    except Exception as e:
        return common.process_error_response(str(e), "***************** Exception Occurred *****************************\nError Details: " + str(e) + "\nRequest Details: " + str(token_details))

    return common.process_error_response(token_details['error_code'], token_details['error_message'])
    

