from pydantic import BaseModel
from typing import Optional
from utils import common

class AUser(BaseModel):
    first_name : Optional[str] = ""
    last_name : Optional[str] = ""
    phone_no : Optional[str] = ""
    uuid : Optional[str] = ""
    country : Optional[str] = ""
    last_updated_on : int =  common.get_current_unix_timestamp()
    is_owner : str = ""
    services : Optional[dict] = {'bookeeping_insights':'N','accept_payments' : 'N'}


class VUser(BaseModel):
    otterz_id : str = ''
    first_name : Optional[str] = ""
    last_name : Optional[str] = ""
    email_id : str = ''
    phone_no : Optional[str] = ""
    uuid : Optional[str] = ""
    country : Optional[str] = ""
    created_on : Optional[int] = ""
    last_updated_on : Optional[int] = ""
    is_owner : str = "N"
    verifications : dict = {'email':'N','phone':'N'}
    services : dict = {'bookeeping_insights':'N','accept_payments' : 'N'}





