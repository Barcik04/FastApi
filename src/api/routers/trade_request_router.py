from fastapi import APIRouter, Depends, Request, HTTPException, status

from src.api.schemas.TradeRequest import TradeRequest, TradeRequestIn
from src.api.services.TradeRequestService import TradeRequestService
from src.auth.utils.deps import get_current_user
from uuid import UUID


router = APIRouter(
    prefix="/trade_requests",
    tags=["trade_requests"],
    dependencies=[Depends(get_current_user)]
)

def get_trade_request_service(request: Request) -> TradeRequestService:
    return request.app.state.trade_request_service


def _extract_user_id(current_user) -> UUID:
    if hasattr(current_user, "id") and current_user.id:
        return UUID(str(current_user.id))
    if isinstance(current_user, dict):
        for k in ("id", "user_id", "uid", "sub"):
            if k in current_user and current_user[k]:
                return UUID(str(current_user[k]))
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid auth payload: missing user id")

@router.get("", response_model=list[TradeRequest])
async def show_user_requests(

    svc: TradeRequestService = Depends(get_trade_request_service),
    current_user = Depends(get_current_user),
):
    user_id = _extract_user_id(current_user)
    return await svc.show_user_requests(user_id)

@router.post("/send", response_model=str)
async def create_user_request(
        body: TradeRequestIn,
        svc: TradeRequestService = Depends(get_trade_request_service),
        current_user = Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return await svc.create_user_request(body, user_id)
