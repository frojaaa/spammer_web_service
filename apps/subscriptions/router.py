from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from .service import SubscriptionsService
from .schemas import Subscription, SubscriptionCreate
from db import SessionLocal
from ..dependencies import common_parameters
from ..schemas import CommonParams

router = APIRouter(prefix='/subscriptions', tags=['subscriptions'], responses={404: {"description": "Not found"}})
CommonsDep = Annotated[CommonParams, Depends(common_parameters)]


def get_subscriptions_service() -> SubscriptionsService:
    db = SessionLocal()
    service = SubscriptionsService(db)
    try:
        yield service
    finally:
        db.close()


@router.get('/', response_model=list[Subscription])
def read_subscriptions(
        commons: CommonsDep,
        service: SubscriptionsService = Depends(get_subscriptions_service)
) -> list[Subscription]:
    subscriptions = service.get_subscriptions(commons.limit, commons.offset)
    return subscriptions


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(subscription: SubscriptionCreate,
                        service: SubscriptionsService = Depends(get_subscriptions_service)):
    service.delete_subscription(subscription)


@router.post('/create', response_model=list[Subscription], status_code=status.HTTP_201_CREATED)
def create_subscriptions(subscriptions: set[SubscriptionCreate],
                        service: SubscriptionsService = Depends(get_subscriptions_service)):
    return service.create_subscriptions(subscriptions)
