from fastapi.responses import JSONResponse

'''
* name : process_error_response
* desc : function is specifically crafted to keep list of all possible errors and its specific messages need to responsd with
* input : error code -> string 
* return : error object -> json
'''
def process_error_response(error_code : str):
    if error_code == 'OTZ4000':
        return JSONResponse(status_code=400, content={"status": False, "errors": [{"message": "Sorry unable to find details stored with the system.","code":error_code}]}) 
    elif error_code == 'OTZ4001':
        return JSONResponse(status_code=400, content={"status": False, "errors": [{"message": "Invalid email address.","code":error_code}]}) 
    elif error_code == 'OTZ4002':
        return JSONResponse(status_code=400, content={"status": False, "errors": [{"message": "Invalid password.Password must be a string at least 6 characters long.","code":error_code}]})
    elif error_code == 'OTZ4003':
        return JSONResponse(status_code=400, content={"status": False, "errors": [{"message": "Email already registered.","code":error_code}]})
    elif error_code == 'OTZ422':
        return JSONResponse(status_code=422, content={"status": False, "errors": [{"message": "Unable to add details.Please contact admin.","code":error_code}]})
    elif error_code == 'OTZM422':
        return JSONResponse(status_code=422, content={"status": False, "errors": [{"message": "Sorry unable to send mail.Please contact admin.","code":error_code}]})
    elif error_code == 'OTZT401':
        return JSONResponse(status_code=401, content={"status": False, "errors": [{"message": "Token Expired.","code":error_code}]})
    elif error_code == 'OTZT422':
        return JSONResponse(status_code=422, content={"status": False, "errors": [{"message": "Invalid Token.","code":error_code}]})
    elif error_code == 'OTZ503':
        return JSONResponse(status_code=503, content={"status": False, "errors": [{"message": "Required permissions missing.","code":error_code}]})
    elif error_code == 'OTZ409':
        return JSONResponse(status_code=409, content={"status": False, "errors": [{"message": "Unable to insert as record already exists.","code":error_code}]})
    else : 
        return JSONResponse(status_code=500, content={"status": False, "errors": [{"message": "Sorry due to some technical issue unable to get response.","code":'OTZ500','reason':error_code}]})