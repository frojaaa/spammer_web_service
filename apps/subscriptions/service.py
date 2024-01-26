from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .models import Subscription
from .schemas import SubscriptionCreate, SubscriptionBase
from ..dependencies import Singleton


class SubscriptionsService(metaclass=Singleton):
    def __init__(self, db: Session):
        self._db = db

    def get_subscription(self, subscription: SubscriptionBase) -> Subscription | None:
        return self._db.get(Subscription, (subscription.chat_id, subscription.project_id))

    def get_subscriptions(self, limit: int, offset: int) -> list[Subscription]:
        return self._db.query(Subscription).offset(offset).limit(limit).all()

    def create_subscriptions(self, subscriptions: set[SubscriptionCreate]) -> list[Subscription]:
        instances = [subscription.model_dump() for subscription in subscriptions]
        instances = self._db.scalars(insert(Subscription).on_conflict_do_nothing().returning(Subscription), instances)
        self._db.commit()
        return instances

    def delete_subscription(self, subscription: SubscriptionCreate) -> None:
        subscription_instance = self.get_subscription(subscription)
        if subscription_instance:
            self._db.delete(subscription_instance)
            self._db.commit()
