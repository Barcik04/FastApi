# src/user/portfolio_router.py
from fastapi import APIRouter, Depends, Request
from typing import List

from src.api.schemas.Portfolio import Portfolio
from src.api.services import PortfolioService
from src.auth.utils.deps import get_current_user


router = APIRouter(prefix="/portfolios", tags=["portfolios"], dependencies=[Depends(get_current_user)])

def get_portfolio_service(request: Request) -> PortfolioService:
    return request.app.state.portfolio_service

@router.get("", response_model=List[Portfolio])
async def list_portfolios(
    svc: PortfolioService = Depends(get_portfolio_service),
    current_user = Depends(get_current_user),
):
    user_id: UUID = current_user.id if hasattr(current_user, "id") else current_user["id"]
    return await svc.list_for_user(user_id)