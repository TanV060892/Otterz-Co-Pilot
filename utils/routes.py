from fastapi import APIRouter
from api.endpoints import token,verify,user,business,invite,onboarding,role,quickbooks,plaid,subscription
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def default_route():
    return JSONResponse(status_code=200, content={"message": "Welcome to Otterz Co-Pilot Bookeeping Platform"})

router.include_router(token.router, prefix="/api")
router.include_router(verify.router, prefix="/api")
router.include_router(user.router, prefix="/api")
router.include_router(business.router, prefix="/api")
router.include_router(invite.router, prefix="/api")
router.include_router(onboarding.router, prefix="/api")
router.include_router(role.router, prefix="/api")
router.include_router(quickbooks.router, prefix="/api")
router.include_router(plaid.router, prefix="/api")
router.include_router(subscription.router, prefix="/api")

@router.route("/{full_path:path}")
async def catch_all(full_path: str):
    return JSONResponse(status_code=404, content={"status": False, "errors": [{"message": "Please provide a valid URL"}]})